# The Night Shift — Why Sleep Matters

Interactive English presentation, 16 slides, 3 speakers, no sound.
Includes a **live class survey**: phones scan a QR code and the answers appear on the screen in real time.

## Publish (needed for the live survey)
1. Push this folder to a GitHub repo.
2. share.streamlit.io → Create app → this repo, branch `main`, file `app.py` → Deploy.
3. Before the talk open `https://<app>.streamlit.app/?reset=nightshift` to clear old answers.

Phones open `https://<app>.streamlit.app/?vote=1` — the QR on slide 3 points there automatically.
Opened locally (`site.html`), the survey slides show clearly labelled demo data.

## Run locally
- Double-click `site.html`, or `streamlit run app.py`.

## Controls
- Dark start screen: **F** — full screen (screen stays), **click / space** — start
- `→` / space — next, `←` — back, moon phases at the bottom — jump to any slide
- Speaker names: in `site.html`, `const SPEAKERS = ['Speaker 1', 'Speaker 2', 'Speaker 3'];`

## Interactive parts
moon follows the mouse · age slider · live survey QR with live counter · sleep need by age · animated hypnogram ·
night-shift cards · hours-awake vs alcohol · drag-the-bars sleep-debt week with battery · flip-card myths ·
bedtime calculator · live class results dashboard · tip checklist with score · caffeine slider ·
lark-or-owl chronotype test · pledge picker · sunrise

Script: `SPEECH.md`.
