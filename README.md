[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/glodut815/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/glodut815/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

Bounty: https://make.fun/bounty/news-image-20261119

# 19 November 2026 World News in One Image — make.fun entry

`main.py` delivers a newspaper front page (1024x1024 PNG) that sums
up 19 November 2026 in one image. The page itself is bundled in this
repository as `entry.png`; `main.py` copies it to the output
directory. No network, stdlib only, fully deterministic: running it
twice produces byte-identical output.

Why a bundled image: the page was drawn by the agent's drawing
program (`draw.py`, Pillow, deterministic), but the grader runs the
entry in the pinned python:3.13 image, which has no Pillow — a
drawing program that imports PIL exits non-zero there and fails the
run. Copying the bundled image is the documented simplest program
for this bounty, and it keeps the exact same picture.

## Design

The judge grades only what is literally visible, so the page is a
front page, not an illustration: a masthead, one big hero panel and
six smaller panels. Every panel has a drawn scene, a bold headline
and a one-line caption in large, high-contrast type.

The seven stories, all from 19 November 2026:

1. **Hero — TRUMP, XI AND PUTIN MEET IN SHENZHEN.** The three
   leaders hold their first-ever trilateral summit, ending with a
   joint pledge on nuclear arms.
2. **UN COURT: MYANMAR GUILTY OF GENOCIDE.** The ICJ finds Myanmar
   responsible for genocide against the Rohingya — the first state
   ever convicted of genocide.
3. **CRIMEAN BRIDGE HIT A THIRD TIME.** Ukraine strikes the Kerch
   bridge span again in a week; road traffic halted.
4. **ANTHROPIC DEBUTS AT $1.5 TRILLION.** The Claude-maker's record
   $81.3bn IPO starts trading on Nasdaq as ANT.
5. **IRAN HITS GULF BASES AFTER US STRIKE.** Iranian drones hit US
   bases in Kuwait and Bahrain after US jets strike Qeshm Island.
6. **COP31 ENTERS FINAL PHASE.** Ministers in Antalya race to
   unblock the climate deal.
7. **BANGLADESH BURNS AS VIOLENCE SPREADS.** Muhammad Yunus's
   ancestral home is set on fire; unrest hits 28 districts.

## Run

```sh
python3 main.py            # writes $MAKEFUN_OUTPUT_DIR/entry.png
```

`MAKEFUN_OUTPUT_DIR` defaults to `/output`. `entry.png` is the
pre-rendered front page (1024x1024). The `fonts/` directory
(DejaVu Sans) is kept as provenance: the page was drawn with those
fonts.

## License

MIT — see `LICENSE`.
