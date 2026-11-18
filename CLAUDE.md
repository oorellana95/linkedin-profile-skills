# linkedin-profile-skills

A Markdown workspace for building and auditing one LinkedIn profile with Claude Code. No code to run. Skills live in `.claude/skills/` and Claude Code loads them automatically.

## Ground truth

- `profile/profile_source.md` is ground truth. Do not edit its original sections. Facts confirmed later go in its "Confirmed later" section, dated.
- `profile/profile_optimized.md` (and the `_es` translation) is the working copy. Every figure in it must trace to the source file or to an answer the user gave in a session. Never invent, round up or imply a number, date, client or result.

## Title integrity

- The official job title is the one on the employer's HR record. Never present "Tech Lead", "Engineering Manager" or any other title the user has not formally held as a title: not in the headline, banner, Experience title field or About.
- Describe scope as work done, with numbers ("leads a remote team of 3", "runs 1:1s"). Put promotions and levels in the description as dated facts, not in the title field.
- Skills like "Engineering Management" may be listed but not pinned. Link people-management skills only to the role where the evidence is.

## Workflow

1. `linkedin-interviewer`: fill `.claude/references/story-bank.md` with numbers, dates and moments. Press soft answers once.
2. `linkedin-profile-optimizer`: audit the pasted profile, then rewrite section by section.
3. `linkedin-humanizer`: strict-tier scrub plus the Pass 4 over-correction check on all final copy before it is called done.
4. Check LinkedIn limits before handing copy over: headline 220, About 2,600, each Experience description 2,000 (line breaks count). Count with a script, do not estimate.
5. `linkedin-resume-builder`: when asked for a resume, build the `.docx` from `profile/profile_optimized.md` with `scripts/build_resume.py`, follow `resume/format_example.docx`, and pass `--facts` so every number is checked against the profile files.

## Tone

Direct, first person, metric-driven. A number comes with its referent. No "passionate", "results-oriented", reveal bridges ("The result?"), staccato fragments or sincerity openers. Em dashes: about 1 per 100 words at most. Details: `.claude/references/voice-rules.md`.

## Privacy

- This repo is public. `profile/` ships fictional examples only. Real profile data (employer metrics, internal tool names, contact details) goes in a private copy, never in a commit to this repo.
- Do not commit a filled `.claude/references/story-bank.md` (check `filled:` at its top).
- Photos, banners and generated resumes (`resume/*_resume_*`) stay out of git (see `.gitignore`).
- Only add a skill or claim to a profile if the user confirmed it. Ask before naming employer-internal tools, teams or providers publicly.
