---
name: linkedin-resume-builder
description: "Build an ATS-friendly .docx resume from an optimized LinkedIn profile, using the Word template in resume/. Use when the user wants a resume or CV file to upload to LinkedIn (Jobs, Preferences, My qualifications, Resumes and application data) or to apply with. Not for rewriting the profile itself (use linkedin-profile-optimizer)."
---

# LinkedIn Resume Builder

Turns the approved profile copy into a one-to-two page `.docx` that follows the layout of `resume/format_example.docx` (header table, blue section rules, bold job lines with right-aligned dates, bullets). The profile stays the source of truth; the resume is a shorter, bullet-only view of it.

## Inputs

- `profile/profile_optimized.md`: approved headline, About, Experience and skills. Wording and figures come from here.
- `profile/profile_source.md`: roles, dates, education, certifications, languages and contact details that the optimized file does not repeat.
- `resume/format_example.docx`: the template. The builder reuses its styles, bullets, fonts and page setup.
- Goal or target role, if the user has one. Order and trim bullets for it; never add claims.

If the optimized file is missing, run `linkedin-profile-optimizer` first. Never write a resume from memory of the conversation.

## Steps

1. **Read the sources.** Read both profile files in full. Note the official title, the dated facts (promotion, start of team lead scope) and any open items in the "needs your confirmation" list.
2. **Write the content file** `resume/<first>_<last>_resume_en.json`, following the schema below and the rules in the next section.
3. **Build:**
   ```bash
   python3 -I .claude/skills/linkedin-resume-builder/scripts/build_resume.py \
     resume/<first>_<last>_resume_en.json resume/<first>_<last>_resume_en.docx \
     --template resume/format_example.docx \
     --facts profile/profile_optimized.md profile/profile_source.md
   ```
   The script prints warnings if a role, company and date line may collide, a rough page estimate, and every number in the resume that appears in none of the `--facts` files. Fix each of those before moving on.
4. **Check the file.** Open it (Word, Pages or Google Docs) and confirm: 2 pages at most, dates right-aligned, no stray empty bullets. Quick Look on macOS ignores custom tab stops, so it shows dates next to the company; that is the viewer, not the file.
5. **Report** what was included, what was left out (and why), the page count, and which open confirmations the resume's wording still depends on.

## Content file

```json
{
  "name": "Full Name",
  "contact_left": ["City, Country", "email@example.com"],
  "contact_right": [{"text": "linkedin.com/in/slug", "url": "https://www.linkedin.com/in/slug"}],
  "summary": "2 to 4 lines. No heading, like the template.",
  "experience": [
    {"role": "Official Title", "company": "Company", "dates": "Jan 2025–Present",
     "detail_left": "Team, or a dated fact such as a promotion", "detail_right": "Country",
     "bullets": ["Action verb + metric with its referent.", "**Bold** spans are allowed."]}
  ],
  "education": [{"degree": "Degree, Field", "school": "School", "dates": "2018–2022"}],
  "certifications": ["**Certifications:** ..."],
  "skills": [{"label": "Programming:", "value": "Python, SQL"}],
  "extra_sections": [{"heading": "Projects", "bullets": ["..."]}]
}
```

`company` may be empty (freelance). `summary_heading` adds a heading above the summary; leave it out to match the template. See `resume/example_content.json` for a complete fictional file.

## Resume rules

- **Official titles only.** The title in each role line is the one on the employer's HR record. A promotion or level goes in `detail_left` as a dated fact. Scope ("leads a team of 3") goes in bullets, never in the title.
- **Every figure comes from the profile files.** Do not round up, merge or add a number. A figure keeps its referent (what was measured, over what period).
- **Bullets, not prose.** Action verb first, no "I". One idea per bullet, usually under 2 lines. The most recent role gets the most bullets; roles older than about 8 years get one or two lines or are left out.
- **ATS-safe structure.** Standard headings (Work Experience, Education and Certifications, Technologies and Languages), reverse chronological order, dates as `Mon YYYY–Mon YYYY`, plain text, no images, no text boxes. The header table comes from the template and is the only table.
- **Keywords match the target.** Use the exact names LinkedIn and job posts use for tools and skills (AWS Lambda, Event-Driven Architecture), spelled consistently with the profile.
- **Tone.** Direct and specific. Apply `../linkedin-humanizer/SKILL.md` strict tier to the summary and bullets, and `../../references/voice-rules.md`.
- **Trim by dropping, not by compressing.** If the file runs past 2 pages, drop the oldest or least relevant roles and bullets before shortening a figure.
- **Leave out** what the profile does not support: no objective statement, no "references available", no photo, no personal data beyond name, city, email and links.

## Uploading to LinkedIn

Jobs, Preferences, My qualifications, Resumes and application data: upload the `.docx`. It is used for applications; it does not update the profile (paste profile sections by hand, per `linkedin-profile-optimizer`).

## Privacy

The generated `.docx` and its `.json` hold contact details. `.gitignore` excludes `resume/*_resume_*`. Keep it that way; share the file by upload, not by commit.

## Files

- `scripts/build_resume.py`: stdlib-only builder (no install step)
- `../../../resume/format_example.docx`: the template (not generated)
- `../../../resume/example_content.json`: fictional example of the content file

## Related skills

- `linkedin-profile-optimizer`: produces the profile copy this skill condenses
- `linkedin-humanizer`: final scrub for the summary and bullets
- `linkedin-interviewer`: fills the Story Bank when a role has no numbers yet
