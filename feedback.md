# Tinker Feedback — Week 7

## Were you able to complete this week's Tinker? *
- [ ] Yes, fully
- [x] Yes, with workarounds
- [ ] No

### If you hit a blocker or used a workaround, what was it?
Docker wasn't installed, so I had to download Docker Desktop before `docker compose up -d` would work. Not a hard fix, but students will definitely hit this if they haven't used Docker before.

---

## Roughly how long did the Tinker take you?
- [ ] Under 30 min
- [ ] 30–60 min
- [ ] 1–2 hours
- [x] More than 2 hours

---

## How ready do you feel to unstick students on this Tinker? *
_Not ready (1) → Fully ready (5)_
- [ ] 1
- [ ] 2
- [ ] 3
- [x] 4
- [ ] 5

---

## Did you hit any errors, broken steps, or typos (activity or portal)?
- [ ] No
- [x] Yes

### If yes: describe the error/typo and where you found it
> `docs/SETUP.md` line 47 says to set `OPENROUTER_API_KEY` but `.env.example` actually uses `OPENAI_API_KEY` — the key name in the instructions is stale.

---

## What worked well?
The `make setup` flow was smooth once Docker was running, and the test accounts seeded automatically were a nice touch.

## What would you change?
Fix the `OPENROUTER_API_KEY` → `OPENAI_API_KEY` typo in SETUP.md, and maybe add a quick "is Docker running?" check at the top of the setup steps since that's likely the most common first blocker.

