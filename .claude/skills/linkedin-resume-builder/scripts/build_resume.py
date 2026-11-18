#!/usr/bin/env python3
"""Build an ATS-friendly .docx resume from a JSON content file.

The Word template supplies the styles, bullet definitions, fonts, theme and page
setup; this script only writes a new word/document.xml (and the hyperlink
relationships) in the template's layout. Standard library only.

Usage:
  python3 -I build_resume.py CONTENT.json OUTPUT.docx \
      [--template resume/format_example.docx] [--facts profile/profile_optimized.md ...]

--facts lists files the resume's numbers must come from. Every number in the
resume that appears in none of them is printed, so an invented or mistyped figure
is caught before the file is uploaded.
"""
import argparse
import json
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

BLUE = "1155cc"
CENTER_TAB = 5097   # company / location column (twips)
RIGHT_TAB = 11058   # right-aligned dates (twips)
BULLET_JOBS, BULLET_LIST, BULLET_SKILLS = 4, 3, 1   # numIds defined in the template
SKILL_TAB = 2300
PAGE_LINES = 55     # rough lines per page at Calibri 11pt, used for the estimate only
LINE_CHARS = 98     # rough characters per bulleted line


def esc(text):
    return escape(text, {'"': "&quot;"})


def rpr(bold=False, size=None, underline=False):
    props = ""
    if bold:
        props += '<w:b w:val="1"/><w:bCs w:val="1"/>'
    if size:
        props += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
    if underline:
        props += '<w:u w:val="single"/>'
    return f"<w:rPr>{props}</w:rPr>" if props else ""


def run(text, bold=False, size=None, underline=False):
    return f'<w:r>{rpr(bold, size, underline)}<w:t xml:space="preserve">{esc(text)}</w:t></w:r>'


def tab(bold=False, size=None):
    return f"<w:r>{rpr(bold, size)}<w:tab/></w:r>"


def rich(text, bold=False, size=None):
    """Text with **bold** spans."""
    if text.count("**") % 2:
        raise ValueError(f"unbalanced ** in: {text[:60]}")
    out = []
    for i, part in enumerate(text.split("**")):
        if part:
            out.append(run(part, bold=bold or i % 2 == 1, size=size))
    return "".join(out)


def para(ppr, runs):
    return f"<w:p><w:pPr>{ppr}</w:pPr>{runs}</w:p>"


def heading(text):
    border = ('<w:pBdr><w:top w:space="0" w:sz="0" w:val="nil"/><w:left w:space="0" w:sz="0" w:val="nil"/>'
              f'<w:bottom w:color="{BLUE}" w:space="2" w:sz="8" w:val="single"/>'
              '<w:right w:space="0" w:sz="0" w:val="nil"/><w:between w:space="0" w:sz="0" w:val="nil"/></w:pBdr>')
    ppr = ('<w:pStyle w:val="Heading2"/><w:keepNext w:val="1"/><w:keepLines w:val="1"/>'
           '<w:pageBreakBefore w:val="0"/><w:widowControl w:val="1"/>' + border +
           '<w:shd w:fill="auto" w:val="clear"/><w:spacing w:after="0" w:before="360" w:line="276" w:lineRule="auto"/>'
           f'<w:ind w:left="0" w:right="0" w:firstLine="0"/><w:jc w:val="left"/><w:rPr><w:color w:val="{BLUE}"/></w:rPr>')
    return para(ppr, f'<w:r><w:rPr><w:color w:val="{BLUE}"/></w:rPr><w:t xml:space="preserve">{esc(text)}</w:t></w:r>')


def body_text(text):
    return para('<w:spacing w:line="240" w:lineRule="auto"/>', rich(text))


def bullet(text, num_id=BULLET_JOBS):
    ppr = (f'<w:numPr><w:ilvl w:val="0"/><w:numId w:val="{num_id}"/></w:numPr>'
           '<w:spacing w:line="240" w:lineRule="auto"/><w:ind w:left="720" w:hanging="360"/>')
    return para(ppr, rich(text))


def spacer():
    return para('<w:spacing w:after="0" w:line="240" w:lineRule="auto"/><w:rPr><w:sz w:val="16"/></w:rPr>', "")


def job_title_line(role, company, dates):
    ppr = (f'<w:keepNext w:val="1"/><w:tabs><w:tab w:val="center" w:pos="{CENTER_TAB}"/>'
           f'<w:tab w:val="right" w:pos="{RIGHT_TAB}"/></w:tabs><w:spacing w:after="0" w:line="240" w:lineRule="auto"/>')
    runs = run(role, bold=True, size=24) + tab(bold=True) + run(company, bold=True) + run("  ") + tab() + run(dates, bold=True)
    return para(ppr, runs)


def job_detail_line(left, right):
    ppr = (f'<w:keepNext w:val="1"/><w:tabs><w:tab w:val="center" w:pos="{CENTER_TAB}"/></w:tabs>'
           '<w:spacing w:after="0" w:line="240" w:lineRule="auto"/>')
    return para(ppr, run(left) + tab() + run(right))


def education_line(item):
    """Degree, school and right-aligned dates on one line; a long entry puts the school on a second line."""
    ppr = (f'<w:numPr><w:ilvl w:val="0"/><w:numId w:val="{BULLET_LIST}"/></w:numPr>'
           f'<w:tabs><w:tab w:val="right" w:pos="{RIGHT_TAB}"/></w:tabs>'
           '<w:spacing w:after="0" w:line="240" w:lineRule="auto"/><w:ind w:left="720" w:hanging="360"/>')
    too_long = (width_pt(item["degree"], 11, True) + width_pt(", " + item["school"], 11)
                + width_pt(item["dates"], 11, True)) > 500
    if not too_long:
        return para(ppr, run(item["degree"], bold=True) + run(", " + item["school"]) + tab() + run(item["dates"], bold=True))
    second = para('<w:spacing w:after="0" w:line="240" w:lineRule="auto"/><w:ind w:left="720"/>', run(item["school"]))
    return para(ppr, run(item["degree"], bold=True) + tab() + run(item["dates"], bold=True)) + second


def skill_line(label, value):
    ppr = (f'<w:numPr><w:ilvl w:val="0"/><w:numId w:val="{BULLET_SKILLS}"/></w:numPr>'
           f'<w:tabs><w:tab w:val="left" w:pos="{SKILL_TAB}"/></w:tabs>'
           f'<w:spacing w:line="240" w:lineRule="auto"/><w:ind w:left="{SKILL_TAB}" w:hanging="{SKILL_TAB - 720}"/>')
    return para(ppr, run(label) + tab() + rich(value))


def link(rid, text):
    return f'<w:hyperlink r:id="{rid}"><w:r><w:rPr><w:u w:val="single"/></w:rPr><w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:hyperlink>'


def header_table(data, has_style):
    def cell(width, inner):
        return (f'<w:tc><w:tcPr><w:tcW w:w="{width}" w:type="dxa"/><w:shd w:fill="auto" w:val="clear"/>'
                '<w:tcMar><w:top w:w="100" w:type="dxa"/><w:left w:w="100" w:type="dxa"/>'
                '<w:bottom w:w="100" w:type="dxa"/><w:right w:w="100" w:type="dxa"/></w:tcMar>'
                f'<w:vAlign w:val="top"/></w:tcPr>{inner}</w:tc>')

    def cp(jc, runs):
        jc_xml = f'<w:jc w:val="{jc}"/>' if jc != "left" else ""
        return para('<w:spacing w:line="240" w:lineRule="auto"/>' + jc_xml, runs)

    br = '<w:r><w:br/></w:r>'
    left = br.join(run(line) for line in data["contact_left"])
    right = br.join(link(f"rIdLink{i + 1}", item["text"]) for i, item in enumerate(data["contact_right"]))
    widths = (3375, 3360, 4365)
    style = '<w:tblStyle w:val="Table1"/>' if has_style else ""
    return ('<w:tbl><w:tblPr>' + style + '<w:tblW w:w="11100" w:type="dxa"/><w:jc w:val="left"/>'
            '<w:tblLayout w:type="fixed"/><w:tblLook w:val="0600"/></w:tblPr><w:tblGrid>'
            + "".join(f'<w:gridCol w:w="{w}"/>' for w in widths) + '</w:tblGrid>'
            '<w:tr><w:trPr><w:cantSplit w:val="0"/><w:trHeight w:val="810" w:hRule="atLeast"/><w:tblHeader w:val="0"/></w:trPr>'
            + cell(widths[0], cp("left", left))
            + cell(widths[1], cp("center", run(data["name"], size=48)))
            + cell(widths[2], cp("right", right))
            + '</w:tr></w:tbl>')


def width_pt(text, size, bold=False):
    return len(text) * size * (0.52 if bold else 0.47)


def check_layout(job):
    """Warn when the role, centred company and right-aligned dates would collide."""
    role_end = width_pt(job["role"], 12, True) * 20
    comp = width_pt(job.get("company", ""), 11, True) * 20
    comp_start = CENTER_TAB - comp / 2
    dates = width_pt(job["dates"], 11, True) * 20
    if job.get("company") and role_end + 150 > comp_start:
        print(f"warning: role and company may overlap: {job['role']} / {job['company']}", file=sys.stderr)
    if job.get("company") and CENTER_TAB + comp / 2 + 150 > RIGHT_TAB - dates:
        print(f"warning: company and dates may overlap: {job['company']}", file=sys.stderr)
    if width_pt(job.get("detail_left", ""), 11) * 20 + 150 > CENTER_TAB - width_pt(job.get("detail_right", ""), 11) * 10:
        print(f"warning: detail line may overlap: {job.get('detail_left', '')[:40]}", file=sys.stderr)


def build_body(data, template_xml, styles_xml):
    has_style = 'w:styleId="Table1"' in styles_xml
    parts = ['<w:p><w:pPr><w:spacing w:line="240" w:lineRule="auto"/></w:pPr></w:p>', header_table(data, has_style)]
    est_lines = 6
    if data.get("summary"):   # the template puts the summary straight under the header, with no heading
        if data.get("summary_heading"):
            parts.append(heading(data["summary_heading"]))
            est_lines += 2
        parts.append(body_text(data["summary"]))
        est_lines += len(data["summary"]) // LINE_CHARS + 1
    parts.append(heading(data.get("experience_heading", "Work Experience")))
    est_lines += 2
    jobs = data["experience"]
    for i, job in enumerate(jobs):
        check_layout(job)
        parts.append(job_title_line(job["role"], job.get("company", ""), job["dates"]))
        parts.append(job_detail_line(job.get("detail_left", ""), job.get("detail_right", "")))
        est_lines += 2
        for text in job["bullets"]:
            parts.append(bullet(text))
            est_lines += len(re.sub(r"\*\*", "", text)) // LINE_CHARS + 1
        if i < len(jobs) - 1:
            parts.append(spacer())
            est_lines += 1
    education = data.get("education", [])
    certs = data.get("certifications", [])
    if education or certs:
        parts.append(heading(data.get("education_heading", "Education and Certifications")))
        est_lines += 2
        parts += [education_line(e) for e in education] + [bullet(c, BULLET_LIST) for c in certs]
        est_lines += len(education) + len(certs)
    if data.get("skills"):
        parts.append(heading(data.get("skills_heading", "Technologies and Languages")))
        est_lines += 2
        for s in data["skills"]:
            parts.append(skill_line(s["label"], s["value"]))
            est_lines += len(s["value"]) // 80 + 1
    for section in data.get("extra_sections", []):
        parts.append(heading(section["heading"]))
        parts += [bullet(b, BULLET_LIST) for b in section["bullets"]]
        est_lines += 2 + len(section["bullets"])
    sect = re.search(r"<w:sectPr\b.*?</w:sectPr>", template_xml, re.S).group(0)
    sect = re.sub(r'"(\d+)\.\d+"', lambda m: f'"{round(float(m.group(0).strip(chr(34))))}"', sect)
    if "w:gutter=" not in sect:   # Google Docs exports omit it; the schema requires it
        sect = sect.replace("<w:pgMar ", '<w:pgMar w:gutter="0" ', 1)
    root = re.search(r"<w:document\b[^>]*>", template_xml).group(0)
    xml = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' + root +
           "<w:body>" + "".join(parts) + sect + "</w:body></w:document>")
    return xml, est_lines


def build_rels(rels_xml, links):
    rels_xml = re.sub(r'<Relationship [^>]*relationships/hyperlink"[^>]*/>', "", rels_xml)
    extra = "".join(
        f'<Relationship Id="rIdLink{i + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" '
        f'Target="{esc(item["url"])}" TargetMode="External"/>' for i, item in enumerate(links))
    return rels_xml.replace("</Relationships>", extra + "</Relationships>")


def numbers(text):
    return set(re.findall(r"\d+(?:[.,]\d+)?", text))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("content")
    ap.add_argument("output")
    ap.add_argument("--template", default="resume/format_example.docx")
    ap.add_argument("--facts", nargs="*", default=[])
    args = ap.parse_args()

    with open(args.content, encoding="utf-8") as fh:
        data = json.load(fh)
    for key in ("name", "contact_left", "contact_right", "experience"):
        if key not in data:
            sys.exit(f"content file is missing '{key}'")

    with zipfile.ZipFile(args.template) as zin:
        names = [n for n in zin.namelist() if not n.endswith("/")]
        parts = {n: zin.read(n) for n in names}
    doc_xml, est_lines = build_body(data, parts["word/document.xml"].decode("utf-8"), parts["word/styles.xml"].decode("utf-8"))
    parts["word/document.xml"] = doc_xml.encode("utf-8")
    parts["word/_rels/document.xml.rels"] = build_rels(
        parts["word/_rels/document.xml.rels"].decode("utf-8"), data["contact_right"]).encode("utf-8")

    ET.fromstring(parts["word/document.xml"])          # must be well-formed
    ET.fromstring(parts["word/_rels/document.xml.rels"])

    order = ["[Content_Types].xml"] + [n for n in names if n != "[Content_Types].xml"]
    with zipfile.ZipFile(args.output, "w", zipfile.ZIP_DEFLATED) as zout:
        for n in order:
            zout.writestr(n, parts[n])

    print(f"wrote {args.output}: {len(data['experience'])} roles, about {est_lines} lines "
          f"(~{est_lines / PAGE_LINES:.1f} pages, rough estimate; open the file to confirm)")

    if args.facts:
        known = set()
        for path in args.facts:
            with open(path, encoding="utf-8") as fh:
                known |= numbers(fh.read())
        text = re.sub(r"<[^>]+>", " ", doc_xml)
        missing = sorted(n for n in numbers(text) if n not in known and n.replace(",", ".") not in known)
        if missing:
            print("numbers in the resume that appear in none of the --facts files: " + ", ".join(missing))
        else:
            print("every number in the resume appears in the --facts files")


if __name__ == "__main__":
    main()
