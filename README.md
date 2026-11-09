# DDCB Revival

A community mod/randomizer for *Digimon Digital Card Battle* (PS1). It patches your own copy of the game to rebalance card stats, randomize/customize starter decks (including a full **build-your-own-deck** mode), and optionally strengthen or hand-curate opponent decks.

**This tool does not include the game.** You must supply your own legally-owned disc image. Nothing here will work without it.

## What you need

1. **A legal copy of *Digimon Digital Card Battle* (PS1)**, dumped from your own disc as a raw `.bin`/`.cue` pair.
2. **Python 3** installed ([python.org](https://www.python.org/downloads/)) — needed to run the script. *(If you received a compiled `.exe` version instead, skip this — just double-click it.)*
3. A PS1 emulator. This mod has been tested with **[DuckStation](https://www.duckstation.org/)**.

## Setup

1. Place `DDCB Revival.py` in the same folder as your game's `.bin`/`.cue` files.
2. Rename your disc image files so the `.bin` is named exactly:
   ```
   Digimon Digital Card Battle.bin
   ```
   (The `.cue` file's name doesn't matter, but it must be pointed at that `.bin` filename inside it — see the `FILE "..."` line in your `.cue`.)

## Running it

Open a terminal in that folder and run:

```bash
python "DDCB Revival.py"
```

*(Or double-click it if you're on a build that doesn't need a visible terminal, or run the standalone `.exe` if you have that version instead.)*

You'll be walked through a series of prompts:

- **Stat mode** — Randomizer (fresh rolls every time), Semi-Randomizer (rolls around curated values), Hand-Altered (exact curated values, no randomness), or Untouched (vanilla stats, no changes at all).
- **Starter deck setup** — pick a partner (Veemon/Hawkmon/Armadillomon) to configure, then choose:
  - **Random deck** — pick a color (or two) and get a randomized deck within it, or
  - **Build your own** — pick any Ultimate-tier creature (including Elite-tier flagships like Omnimon) or one of the 6 Partner cards as your focus, then a power level (Low/Medium/High), and the script assembles a themed 30-card deck around it.

  The other two partners not configured this way get randomized colors automatically.
- **Opponent deck strength** — leave opponent decks as-is, randomize them by difficulty tier, or use a fixed hand-curated deck list per opponent.

When it finishes, it writes a new file:

```
Digimon Digital Card Battle - Revival.bin
```

This is your patched game — your original `.bin` is never modified.

## Loading the patched game

Make a `.cue` file for the new `.bin` (copy your original `.cue` and rename both it and the `FILE` line inside it to match), for example:

```
FILE "Digimon Digital Card Battle - Revival.bin" BINARY
  TRACK 01 MODE2/2352
    INDEX 01 00:00:00
```

Then load that `.cue` in your emulator like normal.

## Notes

- Re-running the script always starts fresh from your original `.bin` — nothing is cumulative between runs.
- If something looks wrong in-game, it's worth re-running with **Untouched** stat mode to confirm the base game is working before troubleshooting the mod itself.
- This is a fan-made, unofficial project with no affiliation to the original game's publisher or developer.
- If anyone plays it, the balance in the late game areas isn't the best for the hand-crafted setting, i did most of the decks in one sitting, and was kinda exhausted at the end. feel free to alter any if the decks in the .py file or any of the stats, i tried to make it simple to understand where things were in the .py file for people who want to change things :)

## License

The script and docs in this repository are released under the [MIT License](LICENSE). That covers this tool only — it does not include or grant any rights to the game itself, which remains the property of its respective owners.
