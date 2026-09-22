[README.md](https://github.com/user-attachments/files/32536671/README.md)
# Mathcade

Maths games I built. Every right answer pushes your Level up — one Level shared
across all the games.

**Play: https://theorumball123-blip.github.io/mathcade/**

## The games

| Game | What you do |
|---|---|
| **Mage Run** | Run, jump and blast monsters through 4 worlds, with a boss at the end of each |
| **Nitro Cup** | Race 16 tracks, drift round corners, and spend your winnings on new cars |
| **Tower Guard** | Build 9 kinds of tower to stop monsters reaching your castle |
| **Prism Rush** | Jump and fly through 8 levels. Dying is free |
| **Striker League '26** | Run a football club and win matches |

Maths turns up where it fits: a pit stop before a race, a supply wagon before a
tower defence level, questions at the end of a Mage Run level.

## How it's made

Plain HTML, CSS and JavaScript. No frameworks, no build step, no downloads —
every game is a single file you can open in a browser. The graphics are drawn
with code, and so is the music and every sound effect.

Your progress is saved in your browser. Online saves (so it follows you to
another computer) can be switched on with Firebase.

## The files

- `index.html` — the front page: your profile, trophies and the daily challenge
- `mage-run.html`, `nitro-cup.html`, `tower-guard.html`, `prism-rush.html`,
  `striker-league.html` — a game each
- `tools/check.py` — checks every page still works together
- `tools/make-mage-levels.py` — builds Mage Run's levels
- `PUT-IT-ONLINE.md` — how to put this on the internet with GitHub
- `SETUP-LOGINS.md` — how a grown-up switches on online saves

Built with [Claude Code](https://claude.com/claude-code).
