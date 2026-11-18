# linkedin-profile-skills

Build, audit and rewrite a LinkedIn profile with four Claude Code skills (`linkedin-profile-skills`). Markdown and Word only; the one script uses the Python standard library, so there is nothing to install.

## Layout

```
.claude/
  skills/
    linkedin-interviewer/        interviews you; fills the Story Bank
    linkedin-profile-optimizer/  audits and rewrites the profile (9-section scorecard)
    linkedin-humanizer/          removes AI tells from the final copy
    linkedin-resume-builder/     builds a .docx resume from the optimized profile (scripts/build_resume.py)
  references/
    story-bank.md                your numbers, dates and moments (shipped empty)
    voice-rules.md               short style rules shared by the skills
profile/
  profile_source.md              EXAMPLE: ground truth, your profile as it is today
  profile_optimized.md           EXAMPLE: the rewrite, with audit and open questions
  profile_optimized_es.md        EXAMPLE: Spanish version of the approved copy
  photo_audit.md                 EXAMPLE: photo checklist template
resume/
  format_example.docx            the Word template the resume follows
  example_content.json           EXAMPLE: fictional content file for the builder
  <name>_resume_en.docx/.json    your generated resume (git-ignored, holds contact details)
CLAUDE.md                        project rules Claude Code reads every session
```

## Use

1. Open the folder in Claude Code (`claude` from this directory).
2. Replace the example in `profile/profile_source.md` with your current profile.
3. Ask for each step by name, for example:
   - "Use linkedin-interviewer to interview me and fill the story bank."
   - "Use linkedin-profile-optimizer to audit profile/profile_source.md and write profile/profile_optimized.md."
   - "Run linkedin-humanizer on the final copy."
   - "Use linkedin-resume-builder to make an English resume .docx from profile/profile_optimized.md."
4. Review `profile_optimized.md`, answer its "needs your confirmation" list, then paste the copy into LinkedIn.

## Before you push

The files in `profile/` are fictional examples (Alex Rivera, Acme Payments). Once you replace them with your own profile they hold employer metrics and contact details, and the Story Bank can hold names and failures. Keep your real copy in a private repo or outside git.

## Credits

`linkedin-profile-optimizer`, `linkedin-humanizer` and `linkedin-interviewer` are adapted from [sergebulaev/linkedin-skills](https://github.com/sergebulaev/linkedin-skills) (MIT, see `LICENSE`), trimmed to the parts this workflow uses. `linkedin-resume-builder` is new here; that repo has no resume skill.

`resume/format_example.docx` is the template from *The Tech Resume Inside Out* (thetechresume.com). Check its terms before redistributing it, or swap in your own template: the builder reuses whatever styles, bullets and page setup the file has.
