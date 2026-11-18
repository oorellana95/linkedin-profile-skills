# LinkedIn Profile, Optimized: Alex Rivera (EXAMPLE)

> **Fictional example.** Output of the three skills run on `profile_source.md`. Every figure traces to that file; nothing was added or rounded up. Replace with your own run.

**Title rule:** the official title is **Senior Backend Engineer**. No line below presents "Team Lead" or "Engineering Manager" as a title. Leadership scope is described as work done, with numbers.

Pipeline: `linkedin-interviewer` (facts into the source file) → `linkedin-profile-optimizer` (audit and rewrite) → `linkedin-humanizer` (strict scrub plus Pass 4) → credibility pass (title audit, §7).

---

## 1. Audit scorecard

| # | Section | Status | Main issue |
|---|---|---|---|
| 1 | Photo | Not scored | Not provided |
| 2 | Banner | Not scored | Not provided |
| 3 | Headline | Needs work | "(Team Lead)" in the title; no scope or metric |
| 4 | About | Needs work | Resume voice, "passionate", no numbers |
| 5 | Featured | Not scored | Not provided |
| 6 | Experience | Needs work | "(Team Lead)" in the title field; bullets without metrics |
| 7 | Skills | Needs work | Generic skills (Leadership, Automation); nothing people-related |
| 8 | Custom URL | Fail | Default hash (`-1a2b3c4d`) |
| 9 | Recommendations | Not scored | Not provided |

## 2. Priority fixes

1. Use the real title everywhere a title appears; let the scope prove the level.
2. Put the strongest team numbers in the first 265 characters of the About.
3. Split Experience at the promotion date (March 2023); both entries keep the real title.
4. Replace generic skills with standard LinkedIn skills tied to roles.
5. Claim a clean custom URL.

---

## 3. Headline (166 of 220 characters)

```
Senior Backend Engineer leading a team of 4 | 1:1s, performance reviews, delivery | Payment-provider integrations on AWS (Python, Go) | Release lead time: 21 days → 6
```

---

## 4. About (1853 of 2,600 characters)

```
I'm a Senior Backend Engineer at Acme Payments. Since March 2023 I've led a team of 4 engineers building integrations with card networks and bank APIs on AWS. Median cycle time is 3.2 days per ticket, and release lead time fell from 21 days to 6 after we automated our deploy pipeline.

The role covers people as well as code: I onboarded all four engineers, run their 1:1s, write their performance reviews with my manager, own delivery against team OKRs, and carry the on-call rotation. I stay hands-on in design and code review.

What the numbers say:
• ~180 tickets delivered per quarter; 90% estimated, 95% with acceptance criteria
• Production incidents: 3 a month in my first quarter on the team, 0 recurring now, after contract tests, a stricter Definition of Done and better alerting
• Provider timeouts down 40%: retries with backoff and a circuit breaker on the three busiest integrations
• 20 min median first response on support escalations; 92% resolved within one day

How I lead:
I coach each engineer on what they need. One now owns our reconciliation job and its dashboards. With another I wrote the contract-testing guide the other teams adopted. I ask everyone what a customer gets from a task before we build it.

Outside the team: I negotiate scope with Product, turn card-scheme rules into validation logic with Compliance, and decide which endpoints we expose to other teams given provider rate limits.

Stack: Python, Go, AWS (Lambda, SQS, EventBridge, DynamoDB, Terraform), Datadog, and integrations with card networks and bank APIs in Europe and Latin America.

Specialties: third-party integrations, people management, technical leadership, delivery and OKRs, incident management, observability, distributed systems, payments.

If you work on payment integrations or release engineering, I'm glad to compare notes. Message me.
```

Hook check: the first three sentences run to 285 characters, so the "see more" cut falls near the end of the release lead-time claim. Title, team size, start date and both delivery numbers sit above it.

---

## 5. Experience

Two entries, split at the promotion. The level (L2 to L3) goes in the description, not the title field.

### Acme Payments: Senior Backend Engineer | March 2023 – Present

Paste-ready description, 1495 of 2,000 characters (line breaks counted):

```
Promoted from Senior Engineer L2 to L3 in March 2023. I lead a team of 4 engineers on Acme Payments' provider-integration platform.

People and leadership
• Onboarded all four engineers; run their 1:1s and write their performance reviews with my manager.
• Coached one engineer into owning the reconciliation job and its dashboards; wrote the contract-testing guide with another, now used by three other teams.

Delivery
• ~180 tickets a quarter at a 3.2-day median cycle time; 90% estimated, 95% with acceptance criteria, tracked in Jira against team OKRs.
• Release lead time fell from 21 days to 6 after we automated the deploy pipeline (GitHub Actions, Terraform).

Reliability and quality
• Production incidents went from 3 a month to 0 recurring after I introduced contract tests, a stricter Definition of Done and Datadog alerts on every provider call.
• Provider timeouts fell 40% with retries, backoff and a circuit breaker on the three busiest integrations.
• Support: 20 min median first response, 92% of escalations resolved within a day.

Stakeholders
• Product: negotiate scope and lower-debt designs that ship the same value sooner.
• Compliance: turn card-scheme rules into validation logic with auditable records.
• Other teams: decide which endpoints we expose, within provider rate limits.

Architecture
• Led the move from a monolithic payments service to event-driven services on AWS (Lambda, SQS, EventBridge, DynamoDB).
• Apply multi-region failover for the checkout path.
```

### Acme Payments: Senior Backend Engineer | January 2021 – March 2023

```
• Built the provider-integration service on AWS Lambda and DynamoDB.
• Cut provider timeouts by adding retries with backoff on the first three integrations.
• Took on the team-lead duties for 4 engineers from late 2022, ahead of the L3 promotion.
```

### Orbit Retail: Backend Engineer | June 2018 – December 2020
Unchanged from `profile_source.md`.

---

## 6. Skills strategy (example: 30 to 40 standard skills)

Only add a skill if LinkedIn's autocomplete offers it; custom names do not match recruiter filters. Link each skill only to the role whose text shows it.

- **Pin (top 3):** Team Leadership, People Management, Third-Party Integrations
- **Add:** Performance Management, Engineering Management (listed, not pinned), Test Automation, Event-Driven Architecture
- **Remove:** Leadership and Automation (too generic; Team Leadership and Test Automation replace them)
- **Order on the current role:** Team Leadership · People Management · Third-Party Integrations · Technical Leadership · Performance Management, then the rest
- **Older roles:** a few skills each, matching that role's bullets

## 7. Credibility audit: lines that crossed into title inflation

| Where | Before | After |
|---|---|---|
| Headline | "Senior Backend Engineer (Team Lead)" | "Senior Backend Engineer leading a team of 4" |
| Experience title field | "Senior Backend Engineer (Team Lead)" | "Senior Backend Engineer", split at the promotion |
| About | "Passionate about … delivering results" | Dated, numbered facts |
| Skills pin | Engineering Management pinned | Listed, not pinned |
| Incidents bullet | "Reduced incidents" | "3 a month to 0 recurring after I introduced …" (names what the person did) |

## 8. Needs your confirmation before publishing

1. Promotion month (March 2023) matches the HR record.
2. "Write performance reviews with my manager": confirm the manager is the reviewer of record.
3. Incidents: "0 recurring" or literally zero of any kind?
4. Naming internal tools, teams or providers publicly is fine with the employer.
5. Each engineer mentioned in a coaching example is comfortable being referenced, even unnamed.
