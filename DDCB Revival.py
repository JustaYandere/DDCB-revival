import random
import os
import struct
import zlib

# =============================================================================
# DDCB REVIVAL  (Digimon Digital Card Battle mod)
# =============================================================================
#
# HOW TO RUN THIS -- STEP BY STEP
# -----------------------------------------------------------------------
# You don't need to know anything about programming to use this. Just
# follow these steps in order:
#
#   1. Install Python (skip this if you already have it):
#        - Go to https://www.python.org/downloads/
#        - Download and run the installer for your operating system.
#        - On Windows: during install, make sure to check the box that
#          says "Add Python to PATH" before clicking Install.
#
#   2. Get your own copy of the game disc:
#        - You need a legally-owned disc image (.bin file) of the
#          original Digimon Digital Card Battle (US version). This mod
#          cannot be shared with the actual game included -- you have to
#          supply your own copy.
#
#   3. Rename your disc image:
#        - Rename your .bin file to exactly:  Digimon Digital Card Battle.bin
#        - Capitalization and spacing matter -- copy it exactly as shown.
#
#   4. Put both files in the same folder:
#        - This script (this .py file)
#        - Your renamed  Digimon Digital Card Battle.bin
#
#   5. Run the script:
#        - Windows: double-click this .py file. A black window will pop
#          up and walk you through some quick questions.
#        - If double-clicking doesn't open anything: open the Command
#          Prompt (search "cmd" in the Start menu), type `cd ` (with a
#          space after it), then drag the folder into the window and
#          press Enter. Then type `python "DDCB Revival.py"` and press
#          Enter.
#        - Mac/Linux: open Terminal, do the same `cd` step above, then
#          run `python3 "DDCB Revival.py"`.
#
#   6. Answer the questions it asks:
#        - It'll ask you to pick a stat mode, a starter deck color, and
#          an opponent deck mode. Just type the letter/number it asks for
#          and press Enter each time.
#
#   7. Get your finished game:
#        - When it's done, look in that same folder for a new file named
#          "Digimon Digital Card Battle - Revival.bin" -- that's your
#          finished, modded game. Load that file in your PS1 emulator
#          just like you would any other game.
#        - The window will say "Press Enter to exit..." when it's
#          completely finished -- that's normal, just press Enter to
#          close it.
#
#
# I felt a lot of disappointment over the years every time I looked for
# a mod of this game, but no more! I made my own. I hope that this mod
# revives this game. Hope you enjoy :)
#
# FEATURES IN THIS MOD
# -----------------------------------------------------------------------
#   - Updated stats for most cards
#   - All cards besides fusions are in packs now, even formerly
#     unobtainable ones
#   - Reworked opponent decks and increased difficulty, especially in the
#     post-game
#   - Opponent decks are now more focused on their star card -- usually
#     the Digimon the deck is themed around -- including Armor Digimon
#   - Three stat modes to choose from: a Randomizer mode that rerolls
#     every card's stats within reworked (generally higher) ranges, a
#     Semi-Randomizer that nudges around curated values, or Hand-Altered
#     stats with zero randomness
#   - Updated starter decks that let you choose which color(s) you'd
#     like, as well as adding some Ultimates to them
#   - Added Mega and Ultra stat differences, so if a Digimon is typically
#     a Mega in the lore, its stats are higher than the rest of the
#     Ultimates -- and the same goes for Ultras
#   - Changed the color identities a bit (mainly Rare) -- you can see
#     what they are below
#   - There are notes throughout this file if you want to alter any
#     values :)
#
# NOTES
# -----------------------------------------------------------------------
#   - If you have Armor Digimon in your deck, it can cause the last slot
#     on the post-duel EXP screen to display incorrectly. I've built in
#     a fix so the game no longer crashes from this, but I haven't been
#     able to fully resolve the display issue itself.
#   - I'd like to make the Digi-Jewels actually useful, but that requires
#     changing the effects on cards, which I don't feel too compelled to
#     try to break apart.
#   - Changing a Digimon's DP and +D doesn't seem too difficult, I just
#     haven't gotten around to it and I'm ok with the current DP and +D
#     on the Digimon.
#   - I was thinking of maybe reining in player power a bit, since with
#     the ability to have a deck of all Armor Digimon, Sevens, and
#     Download Digivolve, it would be hard to lose. So I was thinking of
#     having the max copies available of Sevens, Rosemon's Lure, and
#     Download Digivolve be 2 instead of 1.
#
# WHAT NEXT
# -----------------------------------------------------------------------
# If I get enough help:
#   - A real way to open up the game would be figuring out whether it's
#     possible to add more cards to the card pool -- that would be a
#     total breakthrough, allowing us to truly create a new game. The
#     same goes for adding more areas or enemies.
#   - Balancing the cards (specifically option cards) -- if you have any
#     feedback on certain cards being too strong or weak, let me know. I
#     was mostly just guessing on the numbers and trying to make most
#     cards usable, so some of them are probably unbalanced.
#   - Thematic decks -- if you have any ideas for the opponent decks,
#     that's also something I'd like. I just threw Sevens and other
#     broken cards into the decks of the late-game enemies, so I'm not
#     attached to any of them.
#   - "Hard mode" -- this one would need one of four things:
#       1. First, and much easier, would be updated enemy decklists that
#          are both more thematic and more difficult.
#       2. My second idea was higher enemy stats compared to player
#          stats -- for that, I'd need a way to increase just the
#          enemy's card stats specifically, but that seemed very
#          complicated, if not impossible.
#       3. Third would be a way to let the player open multiple packs at
#          the end of duels -- this would help so it doesn't feel like
#          you get hard-stuck on an encounter, and farming would be
#          easier.
#       4. Fourth, making the fusion shop allow fusion of all cards --
#          this would also help if the player gets stuck in one of the
#          early cities.
#
# WHAT THIS DOES
# -----------------------------------------------------------------------
# Takes a legally-owned copy of the original disc image and produces a
# modified version with:
#
#   1. Three original game bugs fixed (a duel-crash, a "Full Set"
#      collection bug, and a deck-building copy-limit bug) that all
#      stemmed from Armor Digimon never being properly wired into the
#      game's card systems.
#   2. Armor Digimon, Partner cards, Digi-Jewels, and Sevens made fully
#      pack-drawable, collectible, and deck-legal, landing in the
#      specific packs they're meant to (see "PACK PLACEMENT" below).
#   3. Reworked card stats: each color has its own stat identity, special
#      "Mega"/"Elite" tiers for flagship cards, Armor Digimon get a fixed
#      (non-random) stat formula, and a curated set of "exception" cards
#      have hand-picked or paired stats instead of the normal formula.
#   4. Opponent decks and starter decks updated to actually use Armor
#      Digimon and Partners where thematically appropriate.
#   5. Three selectable stat modes (see STAT_MODE below) so you can choose
#      between full randomization, a lighter random nudge around curated
#      values, or your exact curated values with no randomness at all.
#
# HOW TO CUSTOMIZE -- WHAT TO EDIT FOR COMMON CHANGES
# -----------------------------------------------------------------------
# (line numbers are approximate -- they'll drift as the file is edited;
#  search for the exact name shown if the line number is off)
#
#   Want to change...                       ...edit this:                          ~line
#   ---------------------------------------  ------------------------------------  -----
#   A color's normal stat ranges             STAT_RANGES                             263
#   Semi-Randomizer's roll width per tier     _SEMI_RANDOMIZER_WIDTH_BY_STAGE         331
#   Your own curated stats (semi/hand modes) USER_BASE_STATS                        335
#     Internal layout: one block per color (Fire, Ice, Nature, Darkness,
#     Rare, in that order), Ultimate-tier cards first in each block, then
#     Champion, then Rookie. Partner cards (Veemon, Hawkmon, etc.) and
#     Armor Digimon (Flamedramon, etc.) come after all 5 color blocks, at
#     the end of the dict. Search for a card's exact name to jump to it.
#   Which stat is "strongest" per color      ELEMENT_ATTACK_ORDER                    978
#   Which cards are Mega/Elite               MEGA_TIER_NAMES / ELITE_TIER_NAMES      986/990
#   Mega/Elite HP formula or spread          _build_flagship_ranges()                1007
#   Which cards are Armor Digimon             ARMOR_DIGIMON_ELEMENT,                 1073
#                                              ARMOR_DIGIMON_ORIGINAL_STATS          1081
#   The "all attacks equal" exception cards   FIXED_EQUAL_ATTACK_CARDS               1104
#   A specific hardcoded card pair            FIXED_STAT_PAIRS                       1116
#     (currently EMPTY -- Kuwagamon/Kabuterimon's old hardcoded override was
#      removed per your request; both now use USER_BASE_STATS like every
#      other card, in every stat mode including full Randomizer)
#   Recolor/counterpart card pairs            RECOLOR_PAIRS                          1124
#   Armor Digimon's fixed stat formula        armor_digimon_fixed_stats()            1338
#   Which packs Armor/Partners/Jewels/Sevens
#     are eligible for                        _ARMOR_SCORE, _PARTNER_SCORE,          2722/2723
#                                              _DIGI_JEWEL_SCORE, _SEVENS_SCORE       2757/2758
#   Opponent deck baseline data (used only
#     by the tier-strengthening randomizer)   _OPPONENT_DECK_DATA_JSON                3087
#   Opponent deck contents -- THE ONE YOU'VE
#     ACTUALLY BEEN HAND-EDITING              _HANDMADE_OPPONENT_DECKS_JSON           3430
#
#   -- Opponent deck LOGIC (the data above is what you edit; these are
#      the functions that actually apply it) --
#   The 0/1/2 prompt at setup                  prompt_opponent_deck_mode()             3455
#   Mode 2: writes _HANDMADE_OPPONENT_DECKS_
#     JSON to disc exactly as-is, no changes   apply_handmade_opponent_decks()         3433
#   Mode 1: randomizes decks by tier using
#     _OPPONENT_DECK_DATA_JSON as a starting
#     point                                    apply_opponent_deck_strengthening()     3467
#   Mode 1's actual per-deck strengthening
#     (swaps/adds cards based on tier)         strengthen_opponent_deck()              3324
#   Mode 1's option-card selection per pick     _pick_option()                          3311
#   Mode 1's option tiers (1-5) and per-deck-
#     tier weighting between them              _OPTION_TIERS,                          3251
#                                              _DECK_TIER_OPTION_WEIGHTS               3265
#   Mode 1's per-tier swap/add parameters
#     (swap_chance, max_rank_jump, etc.)        _OPPONENT_TIER_PARAMS                   3273
#   Starter deck color/table offsets          BDRV_TABLE_OFFSETS                     2874
#   Which Digivice matches which color, and
#     that Pink Digivice is excluded from
#     every deck's draw pool                  DIGIVICE_ELEMENT,                      1931
#                                              filter_digivices_for_colors()          1935
#
#   -- Build-your-own-deck (pick a focus card + power level for one
#      starter slot instead of a randomized deck) --
#   Evolution chains (Rookie->Champion->
#     Ultimate[s]) used to build a deck        _BYOD_CHAINS                           2178
#   Option-card tiers (Low/Medium/High)        _BYOD_OPTION_LOW / _MEDIUM / _HIGH      2284
#   Copy-count rules by power level x tier     _BYOD_NONELITE_COPY, _BYOD_ELITE_COPY  2305/2311
#   The actual deck-assembly logic             build_custom_starter_deck()            2445
#   The focus-card picker prompt (numbered,
#     grouped by color)                        prompt_focus_card()                    2586
#   The power-level picker prompt              prompt_deck_power_level()               2614
#
# COLOR IDENTITIES (normal, non-flagship cards)
# -----------------------------------------------------------------------
# Which attack type stands out per card (still the original design):
#   Fire     - Circle is the standout attack, notably ahead of the rest
#   Ice      - high HP tank; Triangle is the standout attack, other two lower
#   Nature   - all-arounder; Cross is the standout attack
#   Darkness - all-arounder, a notch stronger than Nature; Circle standout
#   Rare     - all three attacks are similar in range -- any of them can
#              end up strongest for a given card, sitting between Nature's
#              and Darkness's attack magnitude, HP a bit above Darkness's
#
# Overall power-level identity per color (HP vs. attack magnitude,
# reworked in USER_BASE_STATS -- this is the target design, not a fixed
# formula, so any single card can still land outside the trend):
#   Fire     - mid-range HP, highest attack of any color at every stage
#              (Rookie/Champion/Ultimate). Was previously the weakest
#              color across the board -- HP raised, attack raised at
#              Rookie/Champion specifically to reliably hit #1.
#   Ice      - highest HP of any color at every stage, lowest attack.
#              Untouched by the rebalance -- already matched this
#              identity exactly.
#   Nature   - mid-to-low HP and attack; intentionally unremarkable.
#   Darkness - progression by stage rather than a flat identity: weakest
#              color at Rookie, mid-tier at Champion, strongest overall
#              (highest combined HP+attack) at Ultimate. Only the
#              Ultimate tier was actually boosted -- Rookie/Champion
#              already sat where they needed to.
#   Rare     - the strongest color at Champion tier, and second-strongest
#              at Ultimate (behind Darkness).
# =============================================================================

FILE_PATH           = "Digimon Digital Card Battle.bin"
START_SEARCH_OFFSET = 0x02650000
END_SEARCH_OFFSET   = 0x02700000
MAX_SCAN_DISTANCE   = 350
MAX_CROSS_SCAN      = 80

STAT_RANGES = {
    "Fire": {
        "R":  {"HP": (730,  940),  "Circle": (280, 500),  "Triangle": (170, 390),  "Cross": (120, 340)},
        "C":  {"HP": (1040, 2030), "Circle": (490, 870),  "Triangle": (360, 680),  "Cross": (290, 550)},
        "U":  {"HP": (2000, 3500), "Circle": (940, 1500), "Triangle": (700, 1170), "Cross": (560, 940)},
        "RP": {"HP": (920,  1020), "Circle": (430, 480),  "Triangle": (320, 350),  "Cross": (250, 280)},
    },
    "Ice": {
        "R":  {"HP": (1070, 1370), "Circle": (100, 320), "Triangle": (230, 450),  "Cross": (170, 390)},
        "C":  {"HP": (1520, 2610), "Circle": (270, 400), "Triangle": (420, 640),  "Cross": (360, 540)},
        "U":  {"HP": (2920, 4500), "Circle": (520, 690), "Triangle": (810, 1100), "Cross": (690, 930)},
        "RP": {"HP": (1330, 1480), "Circle": (230, 260), "Triangle": (370, 410),  "Cross": (320, 350)},
    },
    "Nature": {
        "R":  {"HP": (870,  1110), "Circle": (270, 490), "Triangle": (170, 390), "Cross": (230, 450)},
        "C":  {"HP": (1230, 2200), "Circle": (480, 700), "Triangle": (360, 530), "Cross": (430, 640)},
        "U":  {"HP": (2360, 3800), "Circle": (920, 1200),"Triangle": (690, 920), "Cross": (830, 1110)},
        "RP": {"HP": (1080, 1200), "Circle": (410, 460), "Triangle": (320, 350), "Cross": (380, 420)},
    },
    "Darkness": {
        "R":  {"HP": (870,  1120), "Circle": (240, 460),  "Triangle": (200, 420),  "Cross": (200, 420)},
        "C":  {"HP": (1250, 2380), "Circle": (440, 750),  "Triangle": (390, 680),  "Cross": (390, 680)},
        "U":  {"HP": (2400, 4100), "Circle": (840, 1300), "Triangle": (750, 1170), "Cross": (750, 1170)},
        "RP": {"HP": (1090, 1210), "Circle": (390, 430),  "Triangle": (340, 380),  "Cross": (340, 380)},
    },
    "Rare": {
        # Rare's identity: all three attacks are similar in range (any of
        # Circle/Triangle/Cross can end up strongest for a given card),
        # sitting between Nature's and Darkness's attack magnitude. HP
        # sits a little above Darkness's.
        "R":  {"HP": (920,  1170), "Circle": (260, 480), "Triangle": (260, 480), "Cross": (260, 480)},
        "C":  {"HP": (1300, 2430), "Circle": (460, 730), "Triangle": (460, 730), "Cross": (460, 730)},
        "U":  {"HP": (2500, 4200), "Circle": (880, 1250), "Triangle": (880, 1250), "Cross": (880, 1250)},
        "RP": {"HP": (1120, 1240), "Circle": (400, 450), "Triangle": (400, 450), "Cross": (400, 450)},
    },
    "Armor": {
        # Uniform bucket across all colors — bridges Champion's high end and
        # Ultimate's low end. Widened from the original (2310-2400, a 90-point
        # spread) to give real card-to-card variance comparable to the other
        # tiers, while still sitting in the Champion-max/Ultimate-min overlap.
        "A":  {"HP": (2000, 3200), "Circle": (600, 900), "Triangle": (550, 850), "Cross": (550, 850)},
        "RP": {"HP": (900,  1500), "Circle": (350, 700), "Triangle": (300, 650), "Cross": (250, 550)},
    },
}

# card_id: decimal card number => prefix bytes [id] 00 00 before name in file
# card_id=None => use explicit "search" bytes instead
# =============================================================================
# THREE STAT MODES: Randomizer / Semi-Randomizer / Hand-Altered
# =============================================================================
# - "randomizer": the existing formula-based system (STAT_RANGES + the
#   weighted rolling logic), unchanged.
# - "semi": uses USER_BASE_STATS below as an anchor, then rolls within a
#   window around each value. Window width depends on tier (R/RP=100,
#   C=250, U=400, M(ega)=500, E(lite)=700 -- Mega/Elite are our own
#   invention, not in the original game).
# - "hand": writes USER_BASE_STATS exactly as given, no randomization.
#
# All three modes still enforce: minimum value 100, and the ones digit is
# always 0 (every value is a multiple of 10).
#
# This only applies to the ~170 "regular" cards using the normal
# STAT_RANGES formula -- Armor Digimon, the Exception 1 fixed-attack
# cards, the hardcoded Kuwagamon/Kabuterimon pair, and the dynamic recolor
# pairs all already have their own dedicated (effectively "hand-altered")
# stat logic and are unaffected by this setting.
STAT_MODE = "randomizer"  # change to "semi" or "hand" to switch modes

_SEMI_RANDOMIZER_WIDTH_BY_STAGE = {
    "R": 100, "RP": 100, "C": 250, "U": 400, "M": 500, "E": 700,
}

USER_BASE_STATS = {
    # Your curated stats -- used directly by "hand" mode, and as the
    # anchor point "semi" mode rolls around. Edit any card's numbers here
    # to change what those two modes produce for it.
    "Imperialdramon": {"HP": 5790, "Circle": 2220, "Triangle": 1730, "Cross": 0},
    "Omnimon I": {"HP": 6100, "Circle": 2000, "Triangle": 1800, "Cross": 0},
    "WarGreymon": {"HP": 4830, "Circle": 1730, "Triangle": 1330, "Cross": 1070},
    "Phoenixmon": {"HP": 4610, "Circle": 1740, "Triangle": 1440, "Cross": 910},
    "Paildramon": {"HP": 3330, "Circle": 1160, "Triangle": 950, "Cross": 830},
    "Gigadramon": {"HP": 3860, "Circle": 1550, "Triangle": 1200, "Cross": 840},
    "RealMetalGreymon": {"HP": 3950, "Circle": 1360, "Triangle": 1070, "Cross": 0},
    "Garudamon": {"HP": 3270, "Circle": 1040, "Triangle": 880, "Cross": 740},
    "MasterTyrannomon": {"HP": 3620, "Circle": 1430, "Triangle": 1310, "Cross": 770},
    "MetalGreymon": {"HP": 2950, "Circle": 960, "Triangle": 670, "Cross": 0},
    "Vermilimon": {"HP": 2960, "Circle": 1030, "Triangle": 800, "Cross": 0},
    "Meteormon": {"HP": 2820, "Circle": 1500, "Triangle": 760, "Cross": 370},
    "ExVeemon": {"HP": 2230, "Circle": 930, "Triangle": 730, "Cross": 0},
    "Aquilamon": {"HP": 1990, "Circle": 790, "Triangle": 610, "Cross": 610},
    "Greymon": {"HP": 2190, "Circle": 940, "Triangle": 720, "Cross": 0},
    "Apemon": {"HP": 2010, "Circle": 910, "Triangle": 630, "Cross": 0},
    "Tyrannomon": {"HP": 1840, "Circle": 810, "Triangle": 650, "Cross": 470},
    "Monochromon": {"HP": 2230, "Circle": 800, "Triangle": 660, "Cross": 610},
    "Meramon": {"HP": 1730, "Circle": 760, "Triangle": 600, "Cross": 510},
    "Centarumon": {"HP": 1870, "Circle": 840, "Triangle": 520, "Cross": 480},
    "Birdramon": {"HP": 1500, "Circle": 820, "Triangle": 540, "Cross": 650},
    "Tankmon": {"HP": 2410, "Circle": 660, "Triangle": 480, "Cross": 510},
    "RedVegiemon": {"HP": 1510, "Circle": 740, "Triangle": 620, "Cross": 820},
    "Piddomon": {"HP": 1770, "Circle": 770, "Triangle": 630, "Cross": 540},
    "Akatorimon": {"HP": 1400, "Circle": 610, "Triangle": 680, "Cross": 400},
    "BomberNanimon": {"HP": 1880, "Circle": 600, "Triangle": 520, "Cross": 0},
    "Flarerizamon": {"HP": 1470, "Circle": 630, "Triangle": 510, "Cross": 480},
    "Agumon": {"HP": 1100, "Circle": 570, "Triangle": 450, "Cross": 390},
    "Solarmon": {"HP": 1300, "Circle": 410, "Triangle": 340, "Cross": 0},
    "Biyomon": {"HP": 970, "Circle": 530, "Triangle": 430, "Cross": 370},
    "Muchomon": {"HP": 1000, "Circle": 470, "Triangle": 310, "Cross": 300},
    "Candlemon": {"HP": 950, "Circle": 600, "Triangle": 500, "Cross": 0},
    "D-Otamamon": {"HP": 990, "Circle": 470, "Triangle": 320, "Cross": 270},
    "Goburimon": {"HP": 1110, "Circle": 500, "Triangle": 500, "Cross": 500},
    "Vikemon": {"HP": 7330, "Circle": 1000, "Triangle": 1310, "Cross": 1210},
    "Omnimon II": {"HP": 7260, "Circle": 1240, "Triangle": 1440, "Cross": 0},
    "MetalSeadramon": {"HP": 6970, "Circle": 960, "Triangle": 1290, "Cross": 1180},
    "MetalGarurumon": {"HP": 5650, "Circle": 800, "Triangle": 1180, "Cross": 1010},
    "MarineAngemon": {"HP": 3810, "Circle": 620, "Triangle": 870, "Cross": 730},
    "WereGarurumon": {"HP": 3560, "Circle": 600, "Triangle": 980, "Cross": 0},
    "Zudomon": {"HP": 4430, "Circle": 600, "Triangle": 910, "Cross": 610},
    "Panjyamon": {"HP": 3450, "Circle": 820, "Triangle": 840, "Cross": 0},
    "MegaSeadramon": {"HP": 3970, "Circle": 540, "Triangle": 870, "Cross": 0},
    "WaruSeadramon": {"HP": 3970, "Circle": 540, "Triangle": 870, "Cross": 560},
    "Brachiomon": {"HP": 3900, "Circle": 300, "Triangle": 820, "Cross": 420},
    "BlueMeramon": {"HP": 3360, "Circle": 200, "Triangle": 840, "Cross": 670},
    "Garurumon": {"HP": 2290, "Circle": 360, "Triangle": 580, "Cross": 0},
    "Ikkakumon": {"HP": 2010, "Circle": 400, "Triangle": 620, "Cross": 510},
    "Dolphmon": {"HP": 2250, "Circle": 120, "Triangle": 540, "Cross": 540},
    "Whamon": {"HP": 2480, "Circle": 350, "Triangle": 610, "Cross": 320},
    "Seadramon": {"HP": 2350, "Circle": 360, "Triangle": 530, "Cross": 490},
    "Gesomon": {"HP": 1840, "Circle": 180, "Triangle": 470, "Cross": 480},
    "Frigimon": {"HP": 2180, "Circle": 310, "Triangle": 410, "Cross": 340},
    "Gekomon": {"HP": 1980, "Circle": 320, "Triangle": 420, "Cross": 420},
    "Coelamon": {"HP": 2420, "Circle": 0, "Triangle": 690, "Cross": 590},
    "Mojyamon": {"HP": 1830, "Circle": 320, "Triangle": 410, "Cross": 390},
    "Shellmon": {"HP": 2100, "Circle": 310, "Triangle": 390, "Cross": 310},
    "Sorcerimon": {"HP": 2220, "Circle": 220, "Triangle": 450, "Cross": 580},
    "IceDevimon": {"HP": 2070, "Circle": 370, "Triangle": 530, "Cross": 440},
    "Hyogamon": {"HP": 2560, "Circle": 500, "Triangle": 500, "Cross": 0},
    "Icemon": {"HP": 1740, "Circle": 280, "Triangle": 420, "Cross": 0},
    "Gomamon": {"HP": 1350, "Circle": 320, "Triangle": 400, "Cross": 360},
    "Gabumon": {"HP": 1360, "Circle": 320, "Triangle": 440, "Cross": 380},
    "Betamon": {"HP": 1360, "Circle": 310, "Triangle": 430, "Cross": 360},
    "Penguinmon": {"HP": 1130, "Circle": 300, "Triangle": 340, "Cross": 230},
    "Gizamon": {"HP": 1290, "Circle": 180, "Triangle": 360, "Cross": 300},
    "Otamamon": {"HP": 1090, "Circle": 100, "Triangle": 250, "Cross": 300},
    "SnowAgumon": {"HP": 1230, "Circle": 310, "Triangle": 360, "Cross": 410},
    "SnowGoburimon": {"HP": 1500, "Circle": 320, "Triangle": 320, "Cross": 320},
    "Valkyrimon": {"HP": 6090, "Circle": 1480, "Triangle": 1280, "Cross": 1780},
    "Seraphimon": {"HP": 7770, "Circle": 0, "Triangle": 0, "Cross": 1600},
    "Magnadramon": {"HP": 6120, "Circle": 1720, "Triangle": 1280, "Cross": 1420},
    "AeroVeedramon": {"HP": 5240, "Circle": 1260, "Triangle": 1200, "Cross": 1400},
    "Rosemon": {"HP": 5090, "Circle": 890, "Triangle": 1170, "Cross": 1320},
    "HerculesKabuterimon": {"HP": 4910, "Circle": 1330, "Triangle": 320, "Cross": 1330},
    "MagnaAngemon": {"HP": 4000, "Circle": 230, "Triangle": 230, "Cross": 900},
    "Sylphymon": {"HP": 3720, "Circle": 940, "Triangle": 830, "Cross": 990},
    "Angewomon": {"HP": 3800, "Circle": 790, "Triangle": 820, "Cross": 860},
    "Lillymon": {"HP": 2470, "Circle": 320, "Triangle": 840, "Cross": 500},
    "MegaKabuterimon": {"HP": 2710, "Circle": 500, "Triangle": 920, "Cross": 0},
    "Piximon": {"HP": 3330, "Circle": 660, "Triangle": 880, "Cross": 1110},
    "Veedramon": {"HP": 2070, "Circle": 340, "Triangle": 750, "Cross": 660},
    "Angemon": {"HP": 2270, "Circle": 380, "Triangle": 380, "Cross": 650},
    "R-Gatomon": {"HP": 1780, "Circle": 550, "Triangle": 580, "Cross": 640},
    "Togemon": {"HP": 1890, "Circle": 630, "Triangle": 510, "Cross": 610},
    "Leomon": {"HP": 2180, "Circle": 570, "Triangle": 750, "Cross": 750},
    "Kabuterimon": {"HP": 2270, "Circle": 520, "Triangle": 640, "Cross": 0},
    "Airdramon": {"HP": 1970, "Circle": 680, "Triangle": 480, "Cross": 540},
    "Unimon": {"HP": 2040, "Circle": 590, "Triangle": 480, "Cross": 700},
    "Ninjamon": {"HP": 1490, "Circle": 150, "Triangle": 570, "Cross": 610},
    "Kuwagamon": {"HP": 2070, "Circle": 670, "Triangle": 540, "Cross": 0},
    "Drimogemon": {"HP": 1810, "Circle": 650, "Triangle": 450, "Cross": 490},
    "Vegiemon": {"HP": 1540, "Circle": 590, "Triangle": 450, "Cross": 490},
    "Kokatorimon": {"HP": 1300, "Circle": 540, "Triangle": 420, "Cross": 480},
    "Yanmamon": {"HP": 1600, "Circle": 500, "Triangle": 420, "Cross": 510},
    "J-Mojyamon": {"HP": 1280, "Circle": 570, "Triangle": 410, "Cross": 500},
    "MoriShellmon": {"HP": 1750, "Circle": 660, "Triangle": 500, "Cross": 570},
    "Tentomon": {"HP": 1070, "Circle": 460, "Triangle": 370, "Cross": 410},
    "Palmon": {"HP": 1110, "Circle": 450, "Triangle": 350, "Cross": 300},
    "Salamon": {"HP": 1100, "Circle": 480, "Triangle": 350, "Cross": 0},
    "Elecmon": {"HP": 930, "Circle": 400, "Triangle": 300, "Cross": 360},
    "Gotsumon": {"HP": 1100, "Circle": 340, "Triangle": 170, "Cross": 330},
    "Kunemon": {"HP": 970, "Circle": 350, "Triangle": 260, "Cross": 290},
    "Apokarimon": {"HP": 7500, "Circle": 1650, "Triangle": 1590, "Cross": 0},
    "GranKuwagamon": {"HP": 6400, "Circle": 1650, "Triangle": 1550, "Cross": 1450},
    "Diaboromon": {"HP": 6660, "Circle": 0, "Triangle": 2000, "Cross": 0},
    "VenomMyotismon": {"HP": 6420, "Circle": 1600, "Triangle": 1560, "Cross": 1650},
    "Piedmon": {"HP": 5720, "Circle": 1520, "Triangle": 890, "Cross": 1470},
    "Machinedramon": {"HP": 6070, "Circle": 1420, "Triangle": 1420, "Cross": 0},
    "Infermon": {"HP": 3000, "Circle": 400, "Triangle": 1210, "Cross": 410},
    "LadyDevimon": {"HP": 4810, "Circle": 1120, "Triangle": 1430, "Cross": 1000},
    "Myotismon": {"HP": 4600, "Circle": 590, "Triangle": 770, "Cross": 1090},
    "Megadramon": {"HP": 4360, "Circle": 1170, "Triangle": 1090, "Cross": 1190},
    "SkullGreymon": {"HP": 5030, "Circle": 1170, "Triangle": 990, "Cross": 950},
    "Phantomon": {"HP": 3040, "Circle": 890, "Triangle": 690, "Cross": 590},
    "WaruMonzaemon": {"HP": 3840, "Circle": 1140, "Triangle": 1030, "Cross": 1040},
    "Andromon": {"HP": 4150, "Circle": 1080, "Triangle": 1030, "Cross": 1010},
    "Stingmon": {"HP": 2310, "Circle": 730, "Triangle": 660, "Cross": 500},
    "Wizardmon": {"HP": 2420, "Circle": 710, "Triangle": 680, "Cross": 690},
    "Devidramon": {"HP": 2840, "Circle": 860, "Triangle": 780, "Cross": 790},
    "Devimon": {"HP": 2170, "Circle": 570, "Triangle": 530, "Cross": 540},
    "Tuskmon": {"HP": 2310, "Circle": 790, "Triangle": 700, "Cross": 640},
    "Ogremon": {"HP": 1930, "Circle": 770, "Triangle": 770, "Cross": 770},
    "Bakemon": {"HP": 1800, "Circle": 660, "Triangle": 480, "Cross": 380},
    "Guardromon": {"HP": 2000, "Circle": 200, "Triangle": 200, "Cross": 0},
    "Tekkamon": {"HP": 1920, "Circle": 480, "Triangle": 500, "Cross": 0},
    "Gururumon": {"HP": 2190, "Circle": 560, "Triangle": 580, "Cross": 500},
    "Soulmon": {"HP": 1410, "Circle": 300, "Triangle": 800, "Cross": 450},
    "Fugamon": {"HP": 2400, "Circle": 580, "Triangle": 580, "Cross": 580},
    "Saberdramon": {"HP": 1410, "Circle": 620, "Triangle": 220, "Cross": 540},
    "Darkrizamon": {"HP": 1500, "Circle": 440, "Triangle": 660, "Cross": 60},
    "Zassomon": {"HP": 1090, "Circle": 300, "Triangle": 400, "Cross": 600},
    "DemiDevimon": {"HP": 1060, "Circle": 410, "Triangle": 400, "Cross": 370},
    "BKGatomon": {"HP": 1030, "Circle": 350, "Triangle": 340, "Cross": 300},
    "Kokuwamon": {"HP": 1060, "Circle": 440, "Triangle": 370, "Cross": 410},
    "Tsukaimon": {"HP": 1030, "Circle": 340, "Triangle": 330, "Cross": 300},
    "Dokunemmon": {"HP": 870, "Circle": 250, "Triangle": 260, "Cross": 290},
    "Aruraumon": {"HP": 1010, "Circle": 350, "Triangle": 350, "Cross": 220},
    "Sharmamon": {"HP": 1120, "Circle": 460, "Triangle": 460, "Cross": 460},
    "Puppetmon": {"HP": 6700, "Circle": 1550, "Triangle": 1550, "Cross": 1550},
    "SuperStarmon": {"HP": 6000, "Circle": 1800, "Triangle": 1580, "Cross": 1380},
    "MetalEtemon": {"HP": 6900, "Circle": 1000, "Triangle": 2000, "Cross": 0},
    "Shakkoumon": {"HP": 6450, "Circle": 1480, "Triangle": 1480, "Cross": 1380},
    "Jijimon": {"HP": 5340, "Circle": 1310, "Triangle": 1310, "Cross": 1310},
    "Digitamamon": {"HP": 5490, "Circle": 1180, "Triangle": 980, "Cross": 1200},
    "Vademon": {"HP": 4010, "Circle": 960, "Triangle": 1140, "Cross": 1040},
    "Giromon": {"HP": 4400, "Circle": 920, "Triangle": 1020, "Cross": 0},
    "Monzaemon": {"HP": 4310, "Circle": 1250, "Triangle": 1000, "Cross": 1110},
    "MetalMamemon": {"HP": 3380, "Circle": 990, "Triangle": 860, "Cross": 960},
    "Mamemon": {"HP": 3150, "Circle": 880, "Triangle": 870, "Cross": 0},
    "Etemon": {"HP": 3990, "Circle": 960, "Triangle": 900, "Cross": 10},
    "Ankylomon": {"HP": 2540, "Circle": 750, "Triangle": 710, "Cross": 740},
    "Starmon": {"HP": 2260, "Circle": 900, "Triangle": 740, "Cross": 720},
    "Thundermon": {"HP": 2230, "Circle": 690, "Triangle": 690, "Cross": 0},
    "PlatinumSukamon": {"HP": 3000, "Circle": 540, "Triangle": 540, "Cross": 540},
    "ShellNumemon": {"HP": 2050, "Circle": 670, "Triangle": 590, "Cross": 590},
    "Nanimon": {"HP": 1730, "Circle": 590, "Triangle": 570, "Cross": 0},
    "Numemon": {"HP": 1700, "Circle": 620, "Triangle": 540, "Cross": 610},
    "Sukamon": {"HP": 1750, "Circle": 600, "Triangle": 540, "Cross": 670},
    "Rockmon": {"HP": 2100, "Circle": 700, "Triangle": 200, "Cross": 670},
    "Geremon": {"HP": 1580, "Circle": 650, "Triangle": 650, "Cross": 610},
    "NiseDrimogemon": {"HP": 1560, "Circle": 630, "Triangle": 600, "Cross": 640},
    "ShimaUnimon": {"HP": 1790, "Circle": 550, "Triangle": 630, "Cross": 550},
    "MudFrigimon": {"HP": 1880, "Circle": 610, "Triangle": 560, "Cross": 550},
    "SandYanmamon": {"HP": 1250, "Circle": 0, "Triangle": 0, "Cross": 700},
    "L-ToyAgumon": {"HP": 1270, "Circle": 530, "Triangle": 200, "Cross": 0},
    "Hagurumon": {"HP": 1300, "Circle": 440, "Triangle": 470, "Cross": 0},
    "ToyAgumon": {"HP": 1230, "Circle": 400, "Triangle": 380, "Cross": 320},
    "ClearAgumon": {"HP": 1110, "Circle": 420, "Triangle": 370, "Cross": 360},
    "Vi-Elecmon": {"HP": 1030, "Circle": 400, "Triangle": 400, "Cross": 360},
    "Psychemon": {"HP": 1060, "Circle": 320, "Triangle": 340, "Cross": 380},
    "ModokiBetamon": {"HP": 1200, "Circle": 410, "Triangle": 330, "Cross": 360},
    "Flamedramon": {"HP": 2000, "Circle": 1200, "Triangle": 1150, "Cross": 0},
    "Magnamon": {"HP": 2350, "Circle": 1050, "Triangle": 600, "Cross": 600},
    "Baronmon": {"HP": 2000, "Circle": 1050, "Triangle": 850, "Cross": 250},
    "Veemon": {"HP": 1250, "Circle": 550, "Triangle": 350, "Cross": 450},
    "Submarimon": {"HP": 3000, "Circle": 400, "Triangle": 600, "Cross": 600},
    "Quetzalmon": {"HP": 2500, "Circle": 700, "Triangle": 750, "Cross": 0},
    "Tylomon": {"HP": 2800, "Circle": 450, "Triangle": 700, "Cross": 550},
    "Halsemon": {"HP": 2100, "Circle": 600, "Triangle": 500, "Cross": 750},
    "Pegasusmon": {"HP": 2250, "Circle": 600, "Triangle": 400, "Cross": 800},
    "Nefertimon": {"HP": 1950, "Circle": 600, "Triangle": 400, "Cross": 700},
    "Hawkmon": {"HP": 1200, "Circle": 400, "Triangle": 500, "Cross": 0},
    "Patamon": {"HP": 1430, "Circle": 470, "Triangle": 370, "Cross": 0},
    "Gatomon": {"HP": 1320, "Circle": 90, "Triangle": 590, "Cross": 0},
    "Raidramon": {"HP": 2500, "Circle": 700, "Triangle": 900, "Cross": 900},
    "Shadramon": {"HP": 2350, "Circle": 1000, "Triangle": 750, "Cross": 350},
    "Wormmon": {"HP": 1350, "Circle": 600, "Triangle": 500, "Cross": 500},
    "Shurimon": {"HP": 2100, "Circle": 670, "Triangle": 550, "Cross": 950},
    "Digmon": {"HP": 2600, "Circle": 800, "Triangle": 800, "Cross": 800},
    "Armadillomon": {"HP": 1500, "Circle": 380, "Triangle": 480, "Cross": 380},
}


def _apply_min_and_round(value):
    """Enforce the universal rule: minimum 100, always a multiple of 10."""
    value = max(100, value)
    return int(round(value / 10.0)) * 10


def semi_randomize_stat(base_value, stage):
    """Roll within a window around base_value, width determined by tier."""
    width = _SEMI_RANDOMIZER_WIDTH_BY_STAGE.get(stage, 250)
    lo = max(100, base_value - width // 2)
    hi = base_value + width // 2
    lo10 = ((lo + 9) // 10) * 10
    hi10 = (hi // 10) * 10
    if lo10 > hi10:
        return _apply_min_and_round(base_value)
    choices = list(range(lo10, hi10 + 1, 10))
    return random.choice(choices) if choices else _apply_min_and_round(base_value)


def hand_altered_stat(base_value):
    """Exact value as given -- no minimum-100 floor (these are the user's
    own deliberate hardcoded values, including intentional 0s or low
    numbers), just rounded to the nearest 10."""
    return int(round(base_value / 10.0)) * 10


CARD_DATABASE = [
    # FIRE ULTIMATES
    {"name": "Imperialdramon",   "card_id": 0,    "orig_hp": 1900, "orig_cir": 980,  "element": "Fire",    "stage": "U", "order": 11},
    {"name": "Omnimon I",        "card_id": 1,    "orig_hp": 1800, "orig_cir": 960,  "element": "Fire",    "stage": "U", "order": 10, "search": b"Omnimon \x2a\x65\x31"},
    {"name": "WarGreymon",       "card_id": 2,    "orig_hp": 1650, "orig_cir": 900,  "element": "Fire",    "stage": "U", "order": 9},
    {"name": "Phoenixmon",       "card_id": 3,    "orig_hp": 1320, "orig_cir": 750,  "element": "Fire",    "stage": "U", "order": 8},
    {"name": "Paildramon",       "card_id": 4,    "orig_hp": 1230, "orig_cir": 800,  "element": "Fire",    "stage": "U", "order": 7},
    {"name": "Gigadramon",       "card_id": 5,    "orig_hp": 1480, "orig_cir": 900,  "element": "Fire",    "stage": "U", "order": 6},
    {"name": "RealMetalGreymon", "card_id": 6,    "orig_hp": 1540, "orig_cir": 850,  "element": "Fire",    "stage": "U", "order": 5},
    {"name": "Garudamon",        "card_id": 7,    "orig_hp": 1320, "orig_cir": 730,  "element": "Fire",    "stage": "U", "order": 4},
    {"name": "MasterTyrannomon", "card_id": 8,    "orig_hp": 1280, "orig_cir": 850,  "element": "Fire",    "stage": "U", "order": 3},
    {"name": "MetalGreymon",     "card_id": 9,    "orig_hp": 1540, "orig_cir": 720,  "element": "Fire",    "stage": "U", "order": 2},
    {"name": "Vermilimon",       "card_id": 10,   "orig_hp": 1430, "orig_cir": 700,  "element": "Fire",    "stage": "U", "order": 1},
    {"name": "Meteormon",        "card_id": 11,   "orig_hp": 1150, "orig_cir": 750,  "element": "Fire",    "stage": "U", "order": 0},
    # FIRE CHAMPIONS
    {"name": "ExVeemon",         "card_id": 12,   "orig_hp": 810,  "orig_cir": 580,  "element": "Fire",    "stage": "C", "order": 14},
    {"name": "Aquilamon",        "card_id": 13,   "orig_hp": 670,  "orig_cir": 570,  "element": "Fire",    "stage": "C", "order": 13},
    {"name": "Greymon",          "card_id": 14,   "orig_hp": 850,  "orig_cir": 600,  "element": "Fire",    "stage": "C", "order": 12},
    {"name": "Apemon",           "card_id": 15,   "orig_hp": 830,  "orig_cir": 550,  "element": "Fire",    "stage": "C", "order": 11},
    {"name": "Tyrannomon",       "card_id": 16,   "orig_hp": 810,  "orig_cir": 520,  "element": "Fire",    "stage": "C", "order": 10},
    {"name": "Monochromon",      "card_id": 17,   "orig_hp": 950,  "orig_cir": 540,  "element": "Fire",    "stage": "C", "order": 9},
    {"name": "Meramon",          "card_id": 18,   "orig_hp": 740,  "orig_cir": 550,  "element": "Fire",    "stage": "C", "order": 8},
    {"name": "Centarumon",       "card_id": 19,   "orig_hp": 800,  "orig_cir": 450,  "element": "Fire",    "stage": "C", "order": 7},
    {"name": "Birdramon",        "card_id": 20,   "orig_hp": 710,  "orig_cir": 500,  "element": "Fire",    "stage": "C", "order": 6},
    {"name": "Tankmon",          "card_id": 21,   "orig_hp": 1000, "orig_cir": 400,  "element": "Fire",    "stage": "C", "order": 5},
    {"name": "RedVegiemon",      "card_id": 22,   "orig_hp": 850,  "orig_cir": 400,  "element": "Fire",    "stage": "C", "order": 4},
    {"name": "Piddomon",         "card_id": 23,   "orig_hp": 750,  "orig_cir": 450,  "element": "Fire",    "stage": "C", "order": 3},
    {"name": "Akatorimon",       "card_id": 24,   "orig_hp": 600,  "orig_cir": 400,  "element": "Fire",    "stage": "C", "order": 2},
    {"name": "BomberNanimon",    "card_id": 25,   "orig_hp": 650,  "orig_cir": 520,  "element": "Fire",    "stage": "C", "order": 1},
    {"name": "Flarerizamon",     "card_id": 26,   "orig_hp": 730,  "orig_cir": 550,  "element": "Fire",    "stage": "C", "order": 0},
    # FIRE ROOKIES
    {"name": "Agumon",           "card_id": 27,   "orig_hp": 570,  "orig_cir": 380,  "element": "Fire",    "stage": "R", "order": 6},
    {"name": "Solarmon",         "card_id": 28,   "orig_hp": 500,  "orig_cir": 350,  "element": "Fire",    "stage": "R", "order": 5},
    {"name": "Biyomon",          "card_id": 29,   "orig_hp": 510,  "orig_cir": 350,  "element": "Fire",    "stage": "R", "order": 4},
    {"name": "Muchomon",         "card_id": 30,   "orig_hp": 600,  "orig_cir": 320,  "element": "Fire",    "stage": "R", "order": 3},
    {"name": "Candlemon",        "card_id": 31,   "orig_hp": 480,  "orig_cir": 380,  "element": "Fire",    "stage": "R", "order": 2},
    {"name": "D-Otamamon",       "card_id": 32,   "orig_hp": 550,  "orig_cir": 300,  "element": "Fire",    "stage": "R", "order": 1},
    {"name": "Goburimon",        "card_id": 33,   "orig_hp": 500,  "orig_cir": 300,  "element": "Fire",    "stage": "R", "order": 0},
    # ICE ULTIMATES
    {"name": "Vikemon",          "card_id": 34,   "orig_hp": 2420, "orig_cir": 760,  "element": "Ice",     "stage": "U", "order": 11},
    {"name": "Omnimon II",       "card_id": 35,   "orig_hp": 2420, "orig_cir": 550,  "element": "Ice",     "stage": "U", "order": 10, "search": b"Omnimon \x2a\x65\x32"},
    {"name": "MetalSeadramon",   "card_id": 36,   "orig_hp": 2030, "orig_cir": 700,  "element": "Ice",     "stage": "U", "order": 9},
    {"name": "MetalGarurumon",   "card_id": 37,   "orig_hp": 2250, "orig_cir": 700,  "element": "Ice",     "stage": "U", "order": 8},
    {"name": "MarineAngemon",    "card_id": 38,   "orig_hp": 1540, "orig_cir": 630,  "element": "Ice",     "stage": "U", "order": 7},
    {"name": "WereGarurumon",    "card_id": 39,   "orig_hp": 1820, "orig_cir": 670,  "element": "Ice",     "stage": "U", "order": 6},
    {"name": "Zudomon",          "card_id": 40,   "orig_hp": 2090, "orig_cir": 700,  "element": "Ice",     "stage": "U", "order": 5},
    {"name": "Panjyamon",        "card_id": 41,   "orig_hp": 1800, "orig_cir": 620,  "element": "Ice",     "stage": "U", "order": 4},
    {"name": "MegaSeadramon",    "card_id": 42,   "orig_hp": 1870, "orig_cir": 650,  "element": "Ice",     "stage": "U", "order": 3},
    {"name": "WaruSeadramon",    "card_id": 43,   "orig_hp": 1760, "orig_cir": 650,  "element": "Ice",     "stage": "U", "order": 2},
    {"name": "Brachiomon",       "card_id": 44,   "orig_hp": 2300, "orig_cir": 600,  "element": "Ice",     "stage": "U", "order": 1},
    {"name": "BlueMeramon",      "card_id": 45,   "orig_hp": 1430, "orig_cir": 700,  "element": "Ice",     "stage": "U", "order": 0},
    # ICE CHAMPIONS
    {"name": "Garurumon",        "card_id": 46,   "orig_hp": 1100, "orig_cir": 350,  "element": "Ice",     "stage": "C", "order": 14},
    {"name": "Ikkakumon",        "card_id": 47,   "orig_hp": 1200, "orig_cir": 340,  "element": "Ice",     "stage": "C", "order": 13},
    {"name": "Dolphmon",         "card_id": 48,   "orig_hp": 1000, "orig_cir": 330,  "element": "Ice",     "stage": "C", "order": 12},
    {"name": "Whamon",           "card_id": 49,   "orig_hp": 1300, "orig_cir": 340,  "element": "Ice",     "stage": "C", "order": 11},
    {"name": "Seadramon",        "card_id": 50,   "orig_hp": 1150, "orig_cir": 360,  "element": "Ice",     "stage": "C", "order": 10},
    {"name": "Gesomon",          "card_id": 51,   "orig_hp": 1030, "orig_cir": 400,  "element": "Ice",     "stage": "C", "order": 9},
    {"name": "Frigimon",         "card_id": 52,   "orig_hp": 990,  "orig_cir": 350,  "element": "Ice",     "stage": "C", "order": 8},
    {"name": "Gekomon",          "card_id": 53,   "orig_hp": 960,  "orig_cir": 340,  "element": "Ice",     "stage": "C", "order": 7},
    {"name": "Coelamon",         "card_id": 54,   "orig_hp": 1270, "orig_cir": 400,  "element": "Ice",     "stage": "C", "order": 6},
    {"name": "Mojyamon",         "card_id": 55,   "orig_hp": 980,  "orig_cir": 370,  "element": "Ice",     "stage": "C", "order": 5},
    {"name": "Shellmon",         "card_id": 56,   "orig_hp": 1250, "orig_cir": 340,  "element": "Ice",     "stage": "C", "order": 4},
    {"name": "Sorcerimon",       "card_id": 57,   "orig_hp": 900,  "orig_cir": 440,  "element": "Ice",     "stage": "C", "order": 3},
    {"name": "IceDevimon",       "card_id": 58,   "orig_hp": 990,  "orig_cir": 390,  "element": "Ice",     "stage": "C", "order": 2},
    {"name": "Hyogamon",         "card_id": 59,   "orig_hp": 1200, "orig_cir": 460,  "element": "Ice",     "stage": "C", "order": 1},
    {"name": "Icemon",           "card_id": 60,   "orig_hp": 1140, "orig_cir": 370,  "element": "Ice",     "stage": "C", "order": 0},
    # ICE ROOKIES
    {"name": "Gomamon",          "card_id": 61,   "orig_hp": 700,  "orig_cir": 300,  "element": "Ice",     "stage": "R", "order": 7},
    {"name": "Gabumon",          "card_id": 62,   "orig_hp": 680,  "orig_cir": 350,  "element": "Ice",     "stage": "R", "order": 6},
    {"name": "Betamon",          "card_id": 63,   "orig_hp": 730,  "orig_cir": 300,  "element": "Ice",     "stage": "R", "order": 5},
    {"name": "Penguinmon",       "card_id": 64,   "orig_hp": 670,  "orig_cir": 320,  "element": "Ice",     "stage": "R", "order": 4},
    {"name": "Gizamon",          "card_id": 65,   "orig_hp": 650,  "orig_cir": 260,  "element": "Ice",     "stage": "R", "order": 3},
    {"name": "Otamamon",         "card_id": 66,   "orig_hp": 710,  "orig_cir": 330,  "element": "Ice",     "stage": "R", "order": 2},
    {"name": "SnowAgumon",       "card_id": 67,   "orig_hp": 720,  "orig_cir": 160,  "element": "Ice",     "stage": "R", "order": 1},
    {"name": "SnowGoburimon",    "card_id": 68,   "orig_hp": 770,  "orig_cir": 230,  "element": "Ice",     "stage": "R", "order": 0},
    # NATURE ULTIMATES
    {"name": "Valkyrimon",           "card_id": 69,  "orig_hp": 1590, "orig_cir": 840,  "element": "Nature",  "stage": "U", "order": 11},
    {"name": "Seraphimon",           "card_id": 70,  "orig_hp": 1650, "orig_cir": 900,  "element": "Nature",  "stage": "U", "order": 10},
    {"name": "Magnadramon",          "card_id": 71,  "orig_hp": 1870, "orig_cir": 800,  "element": "Nature",  "stage": "U", "order": 9},
    {"name": "AeroVeedramon",        "card_id": 72,  "orig_hp": 1430, "orig_cir": 750,  "element": "Nature",  "stage": "U", "order": 8},
    {"name": "Rosemon",              "card_id": 73,  "orig_hp": 1210, "orig_cir": 720,  "element": "Nature",  "stage": "U", "order": 7},
    {"name": "HerculesKabuterimon", "card_id": 74,  "orig_hp": 1700, "orig_cir": 790,  "element": "Nature",  "stage": "U", "order": 6},
    {"name": "MagnaAngemon",         "card_id": 75,  "orig_hp": 1320, "orig_cir": 770,  "element": "Nature",  "stage": "U", "order": 5},
    {"name": "Sylphymon",            "card_id": 76,  "orig_hp": 1540, "orig_cir": 680,  "element": "Nature",  "stage": "U", "order": 4, "search": b"\x4c\x00\x00Sylphymon\x00"},
    {"name": "Angewomon",            "card_id": 77,  "orig_hp": 1370, "orig_cir": 720,  "element": "Nature",  "stage": "U", "order": 3},
    {"name": "Lillymon",             "card_id": 78,  "orig_hp": 1100, "orig_cir": 650,  "element": "Nature",  "stage": "U", "order": 2},
    {"name": "MegaKabuterimon",      "card_id": 79,  "orig_hp": 1480, "orig_cir": 700,  "element": "Nature",  "stage": "U", "order": 1},
    {"name": "Piximon",              "card_id": 80,  "orig_hp": 1370, "orig_cir": 670,  "element": "Nature",  "stage": "U", "order": 0},
    # NATURE CHAMPIONS
    {"name": "Veedramon",            "card_id": 81,  "orig_hp": 880,  "orig_cir": 500,  "element": "Nature",  "stage": "C", "order": 15},
    {"name": "Angemon",              "card_id": 82,  "orig_hp": 940,  "orig_cir": 400,  "element": "Nature",  "stage": "C", "order": 14},
    {"name": "R-Gatomon",            "card_id": 83,  "orig_hp": 750,  "orig_cir": 410,  "element": "Nature",  "stage": "C", "order": 13},
    {"name": "Togemon",              "card_id": 84,  "orig_hp": 800,  "orig_cir": 380,  "element": "Nature",  "stage": "C", "order": 12},
    {"name": "Leomon",               "card_id": 85,  "orig_hp": 890,  "orig_cir": 430,  "element": "Nature",  "stage": "C", "order": 11},
    {"name": "Kabuterimon",          "card_id": 86,  "orig_hp": 950,  "orig_cir": 550,  "element": "Nature",  "stage": "C", "order": 10},
    {"name": "Airdramon",            "card_id": 87,  "orig_hp": 950,  "orig_cir": 430,  "element": "Nature",  "stage": "C", "order": 9},
    {"name": "Unimon",               "card_id": 88,  "orig_hp": 950,  "orig_cir": 390,  "element": "Nature",  "stage": "C", "order": 8},
    {"name": "Ninjamon",             "card_id": 89,  "orig_hp": 650,  "orig_cir": 440,  "element": "Nature",  "stage": "C", "order": 7},
    {"name": "Kuwagamon",            "card_id": 90,  "orig_hp": 900,  "orig_cir": 530,  "element": "Nature",  "stage": "C", "order": 6},
    {"name": "Drimogemon",           "card_id": 91,  "orig_hp": 850,  "orig_cir": 450,  "element": "Nature",  "stage": "C", "order": 5},
    {"name": "Vegiemon",             "card_id": 92,  "orig_hp": 810,  "orig_cir": 390,  "element": "Nature",  "stage": "C", "order": 4},
    {"name": "Kokatorimon",          "card_id": 93,  "orig_hp": 910,  "orig_cir": 350,  "element": "Nature",  "stage": "C", "order": 3},
    {"name": "Yanmamon",             "card_id": 94,  "orig_hp": 740,  "orig_cir": 400,  "element": "Nature",  "stage": "C", "order": 2},
    {"name": "J-Mojyamon",           "card_id": 95,  "orig_hp": 750,  "orig_cir": 280,  "element": "Nature",  "stage": "C", "order": 1},
    {"name": "MoriShellmon",         "card_id": 96,  "orig_hp": 910,  "orig_cir": 390,  "element": "Nature",  "stage": "C", "order": 0},
    # NATURE ROOKIES
    {"name": "Tentomon",             "card_id": 97,  "orig_hp": 670,  "orig_cir": 380,  "element": "Nature",  "stage": "R", "order": 5},
    {"name": "Palmon",               "card_id": 98,  "orig_hp": 500,  "orig_cir": 370,  "element": "Nature",  "stage": "R", "order": 4},
    {"name": "Salamon",              "card_id": 99,  "orig_hp": 600,  "orig_cir": 300,  "element": "Nature",  "stage": "R", "order": 3},
    {"name": "Elecmon",              "card_id": 100, "orig_hp": 650,  "orig_cir": 310,  "element": "Nature",  "stage": "R", "order": 2},
    {"name": "Gotsumon",             "card_id": 101, "orig_hp": 700,  "orig_cir": 290,  "element": "Nature",  "stage": "R", "order": 1},
    {"name": "Kunemon",              "card_id": 102, "orig_hp": 680,  "orig_cir": 350,  "element": "Nature",  "stage": "R", "order": 0},
    # DARKNESS ULTIMATES
    {"name": "Apokarimon",       "card_id": 103, "orig_hp": 2750, "orig_cir": 990,  "element": "Darkness","stage": "U", "order": 13},
    {"name": "GranKuwagamon",    "card_id": 104, "orig_hp": 1760, "orig_cir": 800,  "element": "Darkness","stage": "U", "order": 12},
    {"name": "Diaboromon",       "card_id": 105, "orig_hp": 2580, "orig_cir": 970,  "element": "Darkness","stage": "U", "order": 11},
    {"name": "VenomMyotismon",   "card_id": 106, "orig_hp": 2310, "orig_cir": 920,  "element": "Darkness","stage": "U", "order": 10},
    {"name": "Piedmon",          "card_id": 107, "orig_hp": 1650, "orig_cir": 800,  "element": "Darkness","stage": "U", "order": 9},
    {"name": "Machinedramon",    "card_id": 108, "orig_hp": 2400, "orig_cir": 980,  "element": "Darkness","stage": "U", "order": 8},
    {"name": "Infermon",         "card_id": 109, "orig_hp": 1100, "orig_cir": 610,  "element": "Darkness","stage": "U", "order": 7},
    {"name": "LadyDevimon",      "card_id": 110, "orig_hp": 1150, "orig_cir": 620,  "element": "Darkness","stage": "U", "order": 6},
    {"name": "Myotismon",        "card_id": 111, "orig_hp": 1100, "orig_cir": 650,  "element": "Darkness","stage": "U", "order": 5},
    {"name": "Megadramon",       "card_id": 112, "orig_hp": 1810, "orig_cir": 920,  "element": "Darkness","stage": "U", "order": 4},
    {"name": "SkullGreymon",     "card_id": 113, "orig_hp": 1700, "orig_cir": 960,  "element": "Darkness","stage": "U", "order": 3},
    {"name": "Phantomon",        "card_id": 114, "orig_hp": 1100, "orig_cir": 600,  "element": "Darkness","stage": "U", "order": 2},
    {"name": "WaruMonzaemon",    "card_id": 115, "orig_hp": 1590, "orig_cir": 700,  "element": "Darkness","stage": "U", "order": 1},
    {"name": "Andromon",         "card_id": 116, "orig_hp": 1700, "orig_cir": 690,  "element": "Darkness","stage": "U", "order": 0},
    # DARKNESS CHAMPIONS
    {"name": "Stingmon",         "card_id": 117, "orig_hp": 880,  "orig_cir": 530,  "element": "Darkness","stage": "C", "order": 14},
    {"name": "Wizardmon",        "card_id": 118, "orig_hp": 850,  "orig_cir": 540,  "element": "Darkness","stage": "C", "order": 13},
    {"name": "Devidramon",       "card_id": 119, "orig_hp": 1100, "orig_cir": 520,  "element": "Darkness","stage": "C", "order": 12},
    {"name": "Devimon",          "card_id": 120, "orig_hp": 960,  "orig_cir": 490,  "element": "Darkness","stage": "C", "order": 11},
    {"name": "Tuskmon",          "card_id": 121, "orig_hp": 1150, "orig_cir": 410,  "element": "Darkness","stage": "C", "order": 10},
    {"name": "Ogremon",          "card_id": 122, "orig_hp": 1050, "orig_cir": 530,  "element": "Darkness","stage": "C", "order": 9},
    {"name": "Bakemon",          "card_id": 123, "orig_hp": 860,  "orig_cir": 450,  "element": "Darkness","stage": "C", "order": 8},
    {"name": "Guardromon",       "card_id": 124, "orig_hp": 750,  "orig_cir": 430,  "element": "Darkness","stage": "C", "order": 7},
    {"name": "Tekkamon",         "card_id": 125, "orig_hp": 1100, "orig_cir": 350,  "element": "Darkness","stage": "C", "order": 6},
    {"name": "Gururumon",        "card_id": 126, "orig_hp": 1040, "orig_cir": 470,  "element": "Darkness","stage": "C", "order": 5},
    {"name": "Soulmon",          "card_id": 127, "orig_hp": 500,  "orig_cir": 330,  "element": "Darkness","stage": "C", "order": 4},
    {"name": "Fugamon",          "card_id": 128, "orig_hp": 940,  "orig_cir": 460,  "element": "Darkness","stage": "C", "order": 3},
    {"name": "Saberdramon",      "card_id": 129, "orig_hp": 670,  "orig_cir": 400,  "element": "Darkness","stage": "C", "order": 2},
    {"name": "Darkrizamon",      "card_id": 130, "orig_hp": 890,  "orig_cir": 330,  "element": "Darkness","stage": "C", "order": 1},
    {"name": "Zassomon",         "card_id": 131, "orig_hp": 600,  "orig_cir": 480,  "element": "Darkness","stage": "C", "order": 0},
    # DARKNESS ROOKIES
    {"name": "DemiDevimon",      "card_id": 132, "orig_hp": 490,  "orig_cir": 360,  "element": "Darkness","stage": "R", "order": 6},
    {"name": "BKGatomon",        "card_id": 133, "orig_hp": 520,  "orig_cir": 360,  "element": "Darkness","stage": "R", "order": 5},
    {"name": "Kokuwamon",        "card_id": 134, "orig_hp": 670,  "orig_cir": 270,  "element": "Darkness","stage": "R", "order": 4},
    {"name": "Tsukaimon",        "card_id": 135, "orig_hp": 630,  "orig_cir": 240,  "element": "Darkness","stage": "R", "order": 3},
    {"name": "Dokunemmon",       "card_id": 136, "orig_hp": 650,  "orig_cir": 280,  "element": "Darkness","stage": "R", "order": 2, "search": b"\x88\x00\x00Dokunemmon\x00"},
    {"name": "Aruraumon",        "card_id": 137, "orig_hp": 420,  "orig_cir": 340,  "element": "Darkness","stage": "R", "order": 1},
    {"name": "Sharmamon",        "card_id": 138, "orig_hp": 570,  "orig_cir": 350,  "element": "Darkness","stage": "R", "order": 0},
    # RARE ULTIMATES
    {"name": "Puppetmon",        "card_id": 139, "orig_hp": 1540, "orig_cir": 790,  "element": "Rare",    "stage": "U", "order": 11},
    {"name": "SuperStarmon",     "card_id": 140, "orig_hp": 1650, "orig_cir": 730,  "element": "Rare",    "stage": "U", "order": 10},
    {"name": "MetalEtemon",      "card_id": 141, "orig_hp": 1650, "orig_cir": 300,  "element": "Rare",    "stage": "U", "order": 9},
    {"name": "Shakkoumon",       "card_id": 142, "orig_hp": 1760, "orig_cir": 680,  "element": "Rare",    "stage": "U", "order": 8},
    {"name": "Jijimon",          "card_id": 143, "orig_hp": 1260, "orig_cir": 650,  "element": "Rare",    "stage": "U", "order": 7},
    {"name": "Digitamamon",      "card_id": 144, "orig_hp": 1810, "orig_cir": 800,  "element": "Rare",    "stage": "U", "order": 6},
    {"name": "Vademon",          "card_id": 145, "orig_hp": 1370, "orig_cir": 850,  "element": "Rare",    "stage": "U", "order": 5},
    {"name": "Giromon",          "card_id": 146, "orig_hp": 1900, "orig_cir": 720,  "element": "Rare",    "stage": "U", "order": 4},
    {"name": "Monzaemon",        "card_id": 147, "orig_hp": 2030, "orig_cir": 850,  "element": "Rare",    "stage": "U", "order": 3},
    {"name": "MetalMamemon",     "card_id": 148, "orig_hp": 1920, "orig_cir": 770,  "element": "Rare",    "stage": "U", "order": 2},
    {"name": "Mamemon",          "card_id": 149, "orig_hp": 1700, "orig_cir": 820,  "element": "Rare",    "stage": "U", "order": 1},
    {"name": "Etemon",           "card_id": 150, "orig_hp": 1480, "orig_cir": 700,  "element": "Rare",    "stage": "U", "order": 0},
    # RARE CHAMPIONS
    {"name": "Ankylomon",        "card_id": 151, "orig_hp": 1000, "orig_cir": 420,  "element": "Rare",    "stage": "C", "order": 13},
    {"name": "Starmon",          "card_id": 152, "orig_hp": 900,  "orig_cir": 470,  "element": "Rare",    "stage": "C", "order": 12},
    {"name": "Thundermon",       "card_id": 153, "orig_hp": 710,  "orig_cir": 350,  "element": "Rare",    "stage": "C", "order": 11},
    {"name": "PlatinumSukamon",  "card_id": 154, "orig_hp": 850,  "orig_cir": 240,  "element": "Rare",    "stage": "C", "order": 10},
    {"name": "ShellNumemon",     "card_id": 155, "orig_hp": 900,  "orig_cir": 250,  "element": "Rare",    "stage": "C", "order": 9},
    {"name": "Nanimon",          "card_id": 156, "orig_hp": 700,  "orig_cir": 390,  "element": "Rare",    "stage": "C", "order": 8},
    {"name": "Numemon",          "card_id": 157, "orig_hp": 700,  "orig_cir": 250,  "element": "Rare",    "stage": "C", "order": 7},
    {"name": "Sukamon",          "card_id": 158, "orig_hp": 600,  "orig_cir": 300,  "element": "Rare",    "stage": "C", "order": 6},
    {"name": "Rockmon",          "card_id": 159, "orig_hp": 700,  "orig_cir": 350,  "element": "Rare",    "stage": "C", "order": 5},
    {"name": "Geremon",          "card_id": 160, "orig_hp": 690,  "orig_cir": 280,  "element": "Rare",    "stage": "C", "order": 4},
    {"name": "NiseDrimogemon",   "card_id": 161, "orig_hp": 750,  "orig_cir": 400,  "element": "Rare",    "stage": "C", "order": 3},
    {"name": "ShimaUnimon",      "card_id": 162, "orig_hp": 800,  "orig_cir": 430,  "element": "Rare",    "stage": "C", "order": 2},
    {"name": "MudFrigimon",      "card_id": 163, "orig_hp": 930,  "orig_cir": 480,  "element": "Rare",    "stage": "C", "order": 1},
    {"name": "SandYanmamon",     "card_id": 164, "orig_hp": 600,  "orig_cir": 250,  "element": "Rare",    "stage": "C", "order": 0},
    # RARE ROOKIES
    {"name": "L-ToyAgumon",      "card_id": 165, "orig_hp": 590,  "orig_cir": 270,  "element": "Rare",    "stage": "R", "order": 6},
    {"name": "Hagurumon",        "card_id": 166, "orig_hp": 500,  "orig_cir": 240,  "element": "Rare",    "stage": "R", "order": 5},
    {"name": "ToyAgumon",        "card_id": 167, "orig_hp": 530,  "orig_cir": 280,  "element": "Rare",    "stage": "R", "order": 4},
    {"name": "ClearAgumon",      "card_id": 168, "orig_hp": 580,  "orig_cir": 270,  "element": "Rare",    "stage": "R", "order": 3},
    {"name": "Vi-Elecmon",       "card_id": 169, "orig_hp": 620,  "orig_cir": 260,  "element": "Rare",    "stage": "R", "order": 2},
    {"name": "Psychemon",        "card_id": 170, "orig_hp": 470,  "orig_cir": 250,  "element": "Rare",    "stage": "R", "order": 1},
    {"name": "ModokiBetamon",    "card_id": 171, "orig_hp": 550,  "orig_cir": 120,  "element": "Rare",    "stage": "R", "order": 0},
    # ARMOR / PARTNER (no card_id prefix, use orig_hp/orig_cir exact match)
    {"name": "Flamedramon",  "card_id": None, "orig_hp": 600,  "orig_cir": 500,  "element": "Armor", "stage": "A",  "order": 0, "flat_random": True},
    {"name": "Magnamon",     "card_id": None, "orig_hp": 650,  "orig_cir": 550,  "element": "Armor", "stage": "A",  "order": 0, "flat_random": True},
    {"name": "Baronmon",     "card_id": None, "orig_hp": 600,  "orig_cir": 550,  "element": "Armor", "stage": "A",  "order": 0, "flat_random": True},
    # Partners moved to their color elements so they randomize with their element's
    # RP tier (average Rookie stats for that color) rather than the generic Armor pool.
    {"name": "Veemon",       "card_id": None, "orig_hp": 550,  "orig_cir": 350,  "element": "Fire",    "stage": "RP", "order": 5, "flat_random": True},
    {"name": "Submarimon",   "card_id": None, "orig_hp": 850,  "orig_cir": 400,  "element": "Armor", "stage": "A",  "order": 0, "flat_random": True},
    {"name": "Quetzalmon",   "card_id": None, "orig_hp": 800,  "orig_cir": 400,  "element": "Armor", "stage": "A",  "order": 0, "flat_random": True},
    {"name": "Tylomon",      "card_id": None, "orig_hp": 900,  "orig_cir": 350,  "element": "Armor", "stage": "A",  "order": 0, "flat_random": True},
    {"name": "Halsemon",     "card_id": None, "orig_hp": 700,  "orig_cir": 400,  "element": "Armor", "stage": "A",  "order": 0, "flat_random": True},
    {"name": "Pegasusmon",   "card_id": None, "orig_hp": 750,  "orig_cir": 400,  "element": "Armor", "stage": "A",  "order": 0, "flat_random": True},
    {"name": "Nefertimon",   "card_id": None, "orig_hp": 650,  "orig_cir": 500,  "element": "Armor", "stage": "A",  "order": 0, "flat_random": True},
    {"name": "Hawkmon",      "card_id": None, "orig_hp": 600,  "orig_cir": 300,  "element": "Nature",  "stage": "RP", "order": 4, "flat_random": True},
    {"name": "Patamon",      "card_id": None, "orig_hp": 630,  "orig_cir": 370,  "element": "Nature",  "stage": "RP", "order": 3, "flat_random": True},
    {"name": "Gatomon",      "card_id": None, "orig_hp": 600,  "orig_cir": 290,  "element": "Nature",  "stage": "RP", "order": 2, "flat_random": True},
    {"name": "Raidramon",    "card_id": None, "orig_hp": 650,  "orig_cir": 300,  "element": "Armor", "stage": "A",  "order": 0, "flat_random": True},
    {"name": "Shadramon",    "card_id": None, "orig_hp": 650,  "orig_cir": 500,  "element": "Armor", "stage": "A",  "order": 0, "flat_random": True},
    {"name": "Wormmon",      "card_id": None, "orig_hp": 550,  "orig_cir": 300,  "element": "Darkness","stage": "RP", "order": 1, "flat_random": True},
    {"name": "Shurimon",     "card_id": None, "orig_hp": 600,  "orig_cir": 450,  "element": "Armor", "stage": "A",  "order": 0, "flat_random": True},
    {"name": "Digmon",       "card_id": None, "orig_hp": 800,  "orig_cir": 400,  "element": "Armor", "stage": "A",  "order": 0, "flat_random": True},
    {"name": "Armadillomon", "card_id": None, "orig_hp": 650,  "orig_cir": 280,  "element": "Rare",    "stage": "RP", "order": 0, "flat_random": True},
]


def read_le16(data, offset):
    return struct.unpack_from('<H', data, offset)[0]

def write_le16(data, offset, value):
    struct.pack_into('<H', data, offset, value)

def make_search_bytes(card):
    if "search" in card:
        return card["search"]
    card_id = card["card_id"]
    name_bytes = card["name"].encode("ascii") + b"\x00"
    if card_id is None:
        return name_bytes
    return bytes([card_id & 0xFF, 0x00, 0x00]) + name_bytes


def find_search_bytes_at_word_boundary(haystack, needle):
    """Like haystack.find(needle), but skips matches where the needle is
    actually a substring of a longer name (e.g. searching for 'Veemon\\x00'
    would otherwise match inside 'ExVeemon\\x00', or 'Gatomon\\x00' inside
    'R-Gatomon\\x00' — a hyphen is non-alphabetic but still not a real field
    boundary). A match only counts if the byte immediately before it is a
    NULL byte — the true separator between fields in this format — not just
    any non-letter character."""
    pos = 0
    while True:
        idx = haystack.find(needle, pos)
        if idx == -1:
            return -1
        preceding = haystack[idx - 1:idx]
        if not preceding or preceding == b'\x00':
            return idx
        pos = idx + 1

def find_hp(file_bytes, name_abs, name_len, orig_hp, orig_cir):
    scan_start = name_abs + name_len
    scan_end   = min(scan_start + MAX_SCAN_DISTANCE, len(file_bytes) - 34)
    # Pass 1: exact original stats, AND Triangle (at the normal +30 offset,
    # or the +334 shifted offset used by a handful of cards with an extra
    # data blob in their record) must look like a plausible stat too --
    # otherwise this is a false match (HP/Circle happen to coincide, but
    # the record layout for this card doesn't put Triangle where we
    # expect, which was silently corrupting a handful of cards downstream).
    for pos in range(scan_start, scan_end):
        if (read_le16(file_bytes, pos)     == orig_hp and
                read_le16(file_bytes, pos + 2) == orig_cir):
            if find_triangle_offset(file_bytes, pos) is not None:
                return pos
    # Pass 2: divisible-by-10 triple check with HP >= Circle
    for pos in range(scan_start, scan_end):
        hp  = read_le16(file_bytes, pos)
        cir = read_le16(file_bytes, pos + 2)
        tri = read_le16(file_bytes, pos + 30)
        if (hp % 10 == 0 and cir % 10 == 0 and tri % 10 == 0 and
                100 <= hp <= 9000 and 10 <= cir <= 3000 and
                0 <= tri <= 3000 and hp >= cir):
            return pos
    return None

def find_cross(file_bytes, triangle_off, hp_off=None):
    """Cross is at Triangle + 28 for the vast majority of cards. For a
    handful of cards (confirmed via live RAM inspection), Cross jumps to
    HP + 362 instead -- and this can happen independently of whether
    Triangle itself was shifted (Togemon/Magnadramon: Triangle stays at
    the normal +30, only Cross jumps to +362; LadyDevimon/Tentomon/
    Bakemon: both shift together, Triangle at +334 and Cross at +362,
    which is also HP+362). Tries Triangle+28 first, then HP+362 if
    hp_off is given, validating each with the same small-multiple-of-10
    sanity check. Returns None if neither checks out."""
    candidates = [triangle_off + 28]
    if hp_off is not None:
        candidates.append(hp_off + 362)
    for cross_off in candidates:
        if cross_off + 2 > len(file_bytes):
            continue
        val = read_le16(file_bytes, cross_off)
        if val % 10 == 0 and 0 <= val <= 3000:
            return cross_off
    return None


def find_triangle_offset(file_bytes, hp_off):
    """Triangle is at HP + 30 for the vast majority of cards. A handful of
    cards (confirmed via live RAM inspection: Magnadramon, Togemon,
    LadyDevimon, Tentomon, Bakemon) have a large extra data blob inserted
    earlier in the record (likely a longer/unique ability description),
    which pushes BOTH Triangle and Cross out to HP + 334 / HP + 362
    instead -- the same 28-byte Triangle-to-Cross gap, just shifted.
    Tries the normal offset first, then the shifted one, validating each
    with the same small-multiple-of-10 sanity check. Returns None if
    neither checks out."""
    for offset in (30, 334):
        pos = hp_off + offset
        if pos + 2 > len(file_bytes):
            continue
        val = read_le16(file_bytes, pos)
        if val % 10 == 0 and 0 <= val <= 3000:
            return pos
    return None

def weighted_rand_stat(lo, hi, order, max_order):
    """order=max -> top of range (strongest). order=0 -> bottom (weakest)."""
    if max_order == 0:
        choices = list(range(lo, hi + 1, 10))
        return random.choice(choices) if choices else lo
    span    = hi - lo
    bias    = order / max_order
    center  = lo + int(span * bias)
    half_w  = int(span * 0.40)
    eff_lo  = max(lo, center - half_w)
    eff_hi  = min(hi, center + half_w)
    if eff_lo > eff_hi:
        eff_lo = eff_hi
    lo10 = ((eff_lo + 9) // 10) * 10
    hi10 = (eff_hi  // 10) * 10
    if lo10 > hi10:
        lo10 = hi10
    choices = list(range(lo10, hi10 + 1, 10))
    return random.choice(choices) if choices else lo10

def flat_rand_stat(lo, hi):
    """
    Uniform random pick across the FULL range, multiples of 10.
    Used for card groups where every member should be equally strong
    (no order-based weighting) — e.g. Armor and Partner Rookie cards.
    """
    lo10 = (lo // 10) * 10
    hi10 = (hi // 10) * 10
    if lo10 < lo: lo10 += 10
    choices = list(range(lo10, hi10 + 1, 10))
    return random.choice(choices) if choices else lo10


# How far into the FULL stat range a "guaranteed strong" card's rolls are
# confined to (0.75 = always lands in the top 25% of the range).
GUARANTEED_STRONG_MIN_FRAC = 0.75

# How strongly a high roll on one stat suppresses the ceiling of the NEXT
# stat rolled for the same card (0 = no effect, 1 = would fully cancel the
# order-based window at max prior roll). Keeps a card from being top-tier
# across all four stats at once, without making it impossible.
ANTI_CORRELATION_STRENGTH = 0.35

# Cards whose Cross (Bx) attack is "Eat-up HP" per the official data — their
# Cross stat gets a penalty since that attack has its own built-in payoff.
# Full -200 for Champion/Ultimate tier; only -50 to -100 for Rookie tier
# (Palmon, Aruraumon), since a big penalty hurts more at that power level.
EAT_UP_HP_CROSS_CARDS = {
    "Phoenixmon", "Rosemon", "Lillymon", "Palmon", "Stingmon", "Bakemon",
    "Myotismon", "Soulmon", "Phantomon", "LadyDevimon", "Aruraumon",
}

DP_DATA = {
    "Imperialdramon": 60, "Omnimon I": 60, "WarGreymon": 50, "Phoenixmon": 40, "Paildramon": 30,
    "Gigadramon": 50, "RealMetalGreymon": 40, "Garudamon": 30, "MasterTyrannomon": 50, "MetalGreymon": 30,
    "Vermilimon": 30, "Meteormon": 30, "ExVeemon": 40, "Aquilamon": 30, "Greymon": 40, "Apemon": 40,
    "Tyrannomon": 30, "Monochromon": 40, "Meramon": 30, "Centarumon": 40, "Birdramon": 30, "Tankmon": 40,
    "RedVegiemon": 30, "Piddomon": 40, "Akatorimon": 30, "BomberNanimon": 30, "Flarerizamon": 20,
    "Agumon": 0, "Solarmon": 0, "Biyomon": 0, "Muchomon": 0, "Candlemon": 0, "D-Otamamon": 0, "Goburimon": 0,
    "Vikemon": 50, "Omnimon II": 60, "MetalSeadramon": 50, "MetalGarurumon": 50, "MarineAngemon": 30,
    "WereGarurumon": 30, "Zudomon": 40, "Panjyamon": 30, "MegaSeadramon": 40, "WaruSeadramon": 40,
    "Brachiomon": 30, "BlueMeramon": 30, "Garurumon": 30, "Ikkakumon": 40, "Dolphmon": 40, "Whamon": 40,
    "Seadramon": 40, "Gesomon": 30, "Frigimon": 30, "Gekomon": 30, "Coelamon": 50, "Mojyamon": 30,
    "Shellmon": 30, "Sorcerimon": 40, "IceDevimon": 40, "Hyogamon": 40, "Icemon": 30, "Gomamon": 0,
    "Gabumon": 0, "Betamon": 0, "Penguinmon": 0, "Gizamon": 0, "Otamamon": 0, "SnowAgumon": 0, "SnowGoburimon": 0,
    "Magnadramon": 50, "AeroVeedramon": 40, "Rosemon": 40, "HerculesKabuterimon": 40, "MagnaAngemon": 40,
    "Silphymon": 40, "Angewomon": 40, "Lillymon": 30, "MegaKabuterimon": 30, "Piximon": 40, "Veedramon": 40,
    "Angemon": 40, "R-Gatomon": 30, "Togemon": 30, "Leomon": 40, "Kabuterimon": 40, "Airdramon": 40,
    "Unimon": 40, "Ninjamon": 30, "Kuwagamon": 40, "Drimogemon": 30, "Vegiemon": 30, "Kokatorimon": 30,
    "Yanmamon": 20, "J-Mojyamon": 30, "MoriShellmon": 40, "Tentomon": 0, "Palmon": 0, "Salamon": 0,
    "Elecmon": 0, "Gotsumon": 0, "Kunemon": 0,
    "Apokarimon": 70, "GranKuwagamon": 50, "Diaboromon": 70, "VenomMyotismon": 60, "Piedmon": 50,
    "Machinedramon": 60, "Infermon": 20, "LadyDevimon": 40, "Myotismon": 50, "Megadramon": 50,
    "SkullGreymon": 50, "Phantomon": 30, "WaruMonzaemon": 40, "Andromon": 40, "Stingmon": 40,
    "Wizardmon": 40, "Devidramon": 50, "Devimon": 40, "Tuskmon": 40, "Ogremon": 40, "Bakemon": 30,
    "Guardromon": 20, "Tekkamon": 30, "Gururumon": 40, "Soulmon": 30, "Fugamon": 30, "Saberdramon": 30,
    "Darkrizamon": 30, "Zassomon": 20, "DemiDevimon": 0, "BKGatomon": 0, "Kokuwamon": 0, "Tsukaimon": 0,
    "Dokunemmon": 0, "Aruraumon": 0, "Sharmamon": 0,
    "Puppetmon": 50, "SuperStarmon": 40, "MetalEtemon": 50, "Shakkoumon": 40, "Jijimon": 40,
    "Digitamamon": 50, "Vademon": 40, "Giromon": 30, "Monzaemon": 50, "MetalMamemon": 30, "Mamemon": 30,
    "Etemon": 40, "Ankylomon": 40, "Starmon": 40, "Thundermon": 30, "PlatinumSukamon": 40, "ShellNumemon": 30,
    "Nanimon": 30, "Numemon": 30, "Sukamon": 30, "Rockmon": 40, "Geremon": 30, "NiseDrimogemon": 30,
    "ShimaUnimon": 30, "MudFrigimon": 30, "SandYanmamon": 20, "L-ToyAgumon": 0, "Hagurumon": 0,
    "ToyAgumon": 0, "ClearAgumon": 0, "Vi-Elecmon": 0, "Psychemon": 0, "ModokiBetamon": 0,
}


# Cards with no Cross ability at all (shown as "(none)" in-game — e.g.
# Goblimon, SnowGoblimon) only get 3 attack options instead of 4. This
# boosts their HP/Circle/Triangle range to compensate, so they aren't simply
# strictly worse than a same-tier card that does have a 4th attack.
NO_CROSS_STAT_BOOST = 0.12

# --- Mega / Elite flagship stat tiers ---
# "Cleanly above" means HP and each color's actual STRONGEST attack stat
# are fully non-overlapping between tiers. The other two attack stats are
# allowed to overlap (simple percentage boost on the normal U-tier range).
#
# Per-color strongest-attack order (typical, per the user):
#   Fire:     Circle > Cross > Triangle
#   Ice:      Triangle > Cross > Circle
#   Nature:   Cross > Circle > Triangle
#   Darkness: Circle > Triangle > Cross
#   Rare:     Cross > Triangle > Circle
import math as _math

ELEMENT_ATTACK_ORDER = {
    "Fire":     ["Circle", "Cross", "Triangle"],
    "Ice":      ["Triangle", "Cross", "Circle"],
    "Nature":   ["Cross", "Circle", "Triangle"],
    "Darkness": ["Circle", "Triangle", "Cross"],
    "Rare":     ["Cross", "Triangle", "Circle"],
}

MEGA_TIER_NAMES = {
    "WarGreymon", "Phoenixmon", "MetalGarurumon", "HerculesKabuterimon",
    "Piedmon", "Machinedramon", "Jijimon",
}
ELITE_TIER_NAMES = {
    "Imperialdramon", "Omnimon I", "Omnimon II", "Vikemon", "MetalSeadramon",
    "AeroVeedramon", "Magnadramon", "Seraphimon", "Valkyrimon", "Rosemon",
    "Apokarimon", "GranKuwagamon", "Diaboromon", "VenomMyotismon",
    "Puppetmon", "SuperStarmon", "MetalEtemon", "Shakkoumon",
}

# Boost for the two non-strongest attack stats (overlap allowed).
MEGA_MINOR_BOOST = 0.20
ELITE_MINOR_BOOST = 0.45


def _round10(n):
    """Round up to the nearest multiple of 10."""
    return int(_math.ceil(n / 10.0)) * 10


def _build_flagship_ranges():
    """Compute explicit, non-overlapping HP + attack ranges for Mega and
    Elite per element.

    HP (all colors): Mega = (U-tier max + 700, +1200). Elite = (Mega max +
    700, +1200). Always a clean 500-wide band, always clears the tier below.

    Attacks -- Rare is a special case: all three attacks (Circle/Triangle/
    Cross) share the SAME explicit range (so any of them can end up
    strongest for a given card, reflecting Rare's "all similar" identity),
    sitting between Nature's and Darkness's strongest-attack ranges. Every
    other color keeps one explicit "strongest" attack range (built the
    same way as before) with the other two attacks using the boosted,
    overlap-allowed treatment.
    """
    mega, elite = {}, {}

    # Pass 1: HP + strongest-attack ranges for every color except Rare.
    for elem, tiers in STAT_RANGES.items():
        if "U" not in tiers or elem == "Rare":
            continue
        u = tiers["U"]
        strongest_stat = ELEMENT_ATTACK_ORDER[elem][0]
        mega_hp = (u["HP"][1] + 700, u["HP"][1] + 1200)
        elite_hp = (mega_hp[1] + 700, mega_hp[1] + 1200)
        mega_atk = (_round10(u[strongest_stat][1] * 1.05), _round10(u[strongest_stat][1] * 1.12))
        elite_atk = (_round10(mega_atk[1] * 1.05), _round10(mega_atk[1] * 1.15))
        mega[elem] = {"HP": mega_hp, strongest_stat: mega_atk, "strongest_stat": strongest_stat}
        elite[elem] = {"HP": elite_hp, strongest_stat: elite_atk, "strongest_stat": strongest_stat}

    # Pass 2: Rare -- HP via the same universal formula, but attack range
    # interpolated between Nature's and Darkness's (already computed above).
    u_rare = STAT_RANGES["Rare"]["U"]
    mega_hp_rare = (u_rare["HP"][1] + 700, u_rare["HP"][1] + 1200)
    elite_hp_rare = (mega_hp_rare[1] + 700, mega_hp_rare[1] + 1200)

    nat_mega = mega["Nature"][ELEMENT_ATTACK_ORDER["Nature"][0]]
    dark_mega = mega["Darkness"][ELEMENT_ATTACK_ORDER["Darkness"][0]]
    nat_elite = elite["Nature"][ELEMENT_ATTACK_ORDER["Nature"][0]]
    dark_elite = elite["Darkness"][ELEMENT_ATTACK_ORDER["Darkness"][0]]
    mega_atk_rare = (_round10((nat_mega[0] + dark_mega[0]) / 2), _round10((nat_mega[1] + dark_mega[1]) / 2))
    elite_atk_rare = (_round10((nat_elite[0] + dark_elite[0]) / 2), _round10((nat_elite[1] + dark_elite[1]) / 2))

    mega["Rare"] = {"HP": mega_hp_rare, "all_attacks": mega_atk_rare, "strongest_stat": None}
    elite["Rare"] = {"HP": elite_hp_rare, "all_attacks": elite_atk_rare, "strongest_stat": None}

    return mega, elite


def flagship_tier_of(name):
    """Returns 'elite', 'mega', or None."""
    if name in ELITE_TIER_NAMES:
        return "elite"
    if name in MEGA_TIER_NAMES:
        return "mega"
    return None


MEGA_STAT_RANGES, ELITE_STAT_RANGES = _build_flagship_ranges()


# --- Armor Digimon: fixed (non-randomized) stats ---
# HP triples, all three attacks double (using each card's ORIGINAL values),
# then the three doubled numbers get re-sorted into Circle/Triangle/Cross
# according to the card's real color identity (not the generic "Armor"
# element the CARD_DATABASE stage system uses elsewhere).
ARMOR_DIGIMON_ELEMENT = {
    "Flamedramon": "Fire", "Magnamon": "Fire", "Baronmon": "Fire",
    "Submarimon": "Ice", "Quetzalmon": "Ice", "Tylomon": "Ice",
    "Halsemon": "Nature", "Pegasusmon": "Nature", "Nefertimon": "Nature",
    "Raidramon": "Darkness", "Shadramon": "Darkness",
    "Shurimon": "Rare", "Digmon": "Rare",
}
# Original (pre-mod) HP/Circle/Triangle/Cross, read directly from the disc.
ARMOR_DIGIMON_ORIGINAL_STATS = {
    "Flamedramon": (600, 500, 350, 0),
    "Magnamon":    (650, 550, 300, 200),
    "Baronmon":    (600, 550, 450, 150),
    "Submarimon":  (850, 400, 300, 200),
    "Quetzalmon":  (800, 400, 350, 0),
    "Tylomon":     (900, 350, 300, 250),
    "Halsemon":    (700, 400, 300, 250),
    "Pegasusmon":  (750, 400, 300, 200),
    "Nefertimon":  (650, 500, 300, 200),
    "Raidramon":   (650, 300, 300, 400),
    "Shadramon":   (650, 500, 350, 150),
    "Shurimon":    (600, 450, 350, 250),
    "Digmon":      (800, 400, 400, 400),
}


# --- Exception 1: "all attacks equal" cards, hardcoded (not derived from
# the normal per-element tier formula) ---
# Goburimon/SnowGoburimon/Sharmamon: high roll within their own tier.
# Ogremon/Fugamon/Hyogamon: a coordinated relative ranking (Hyogamon
# highest HP/lowest attack, Ogremon lowest HP/highest attack, Fugamon in
# the middle), each a flat-random pick within a 200-point-wide band.
FIXED_EQUAL_ATTACK_CARDS = {
    "Goburimon":     {"HP": (940, 940),   "attack": (500, 500)},
    "SnowGoburimon": {"HP": (1370, 1370), "attack": (450, 450)},
    "Sharmamon":     {"HP": (1120, 1120), "attack": (460, 460)},
    "Fugamon":       {"HP": (2200, 2400), "attack": (400, 600)},
    "Hyogamon":      {"HP": (2500, 2700), "attack": (300, 500)},
    "Ogremon":       {"HP": (1900, 2100), "attack": (500, 700)},
}

# Kuwagamon/Kabuterimon's hardcoded pair override has been removed --
# both now use normal stat logic (USER_BASE_STATS in semi/hand modes)
# like every other card.
FIXED_STAT_PAIRS = {}


# --- Exception 2: recolor pairs ---
# Original -> list of recolors. Each recolor shares its tens digit (per
# stat) with the original's ACTUAL rolled value that game, but draws its
# hundreds/thousands from its own element/tier range, and its own
# strongest-attack slot follows its own color identity.
RECOLOR_PAIRS = {
    "Agumon": ["SnowAgumon", "ToyAgumon"],
    "Vegiemon": ["RedVegiemon", "Zassomon"],
    "Hagurumon": ["Solarmon"],
    "Penguinmon": ["Muchomon"],
    "J-Mojyamon": ["Mojyamon"],
    "Betamon": ["ModokiBetamon"],
    "Shellmon": ["MoriShellmon"],
    "Otamamon": ["D-Otamamon"],
    "Angewomon": ["LadyDevimon"],
    "Airdramon": ["Seadramon"],
    "Unimon": ["ShimaUnimon"],
    "Drimogemon": ["NiseDrimogemon"],
    "Elecmon": ["Vi-Elecmon"],
    "Dokunemmon": ["Kunemon"],
    "MagnaAngemon": ["Myotismon"],
    "Gigadramon": ["Megadramon"],
    "Yanmamon": ["SandYanmamon"],
    # Exception 3 pairs, merged in here per the user's request -- handled
    # identically to every other recolor pair (tens-digit matched per
    # stat, own element/tier range, own color's strongest-attack order).
    "Angemon": ["Devimon", "Piddomon"],
    "Garurumon": ["Gururumon"],
    "Frigimon": ["MudFrigimon"],
    "Wizardmon": ["Sorcerimon"],
    "Devimon": ["IceDevimon"],
    "Palmon": ["Aruraumon"],
    "Birdramon": ["Saberdramon"],
    "Gatomon": ["BKGatomon"],
    "Patamon": ["Tsukaimon"],
    "Monzaemon": ["WaruMonzaemon"],
    "Gabumon": ["Psychemon"],
    # Kabuterimon/Kuwagamon handled separately via FIXED_STAT_PAIRS (both
    # hardcoded, not part of the dynamic recolor system).
}
RECOLOR_TO_ORIGINAL = {r: o for o, rs in RECOLOR_PAIRS.items() for r in rs}


def _locate_card(working, search_block, card):
    """Shared name-location logic used throughout stat randomization."""
    search = make_search_bytes(card)
    rel = find_search_bytes_at_word_boundary(search_block, search) \
        if card.get("card_id") is None else search_block.find(search)
    if rel == -1:
        return None, None
    name_abs = START_SEARCH_OFFSET + rel
    name_len = (len(card["name"]) + 1) if card.get("card_id") is not None else len(search)
    if card.get("card_id") is not None:
        name_abs += 3
    hp_off = find_hp(working, name_abs, name_len, card["orig_hp"], card["orig_cir"])
    return hp_off, name_len


def _tens_match(value, lo, hi):
    """Nearest value to the range midpoint that shares VALUE's tens digit
    and falls within [lo, hi] (with an effective floor of 100 -- nothing
    ever comes out below 100). If the exact tens digit doesn't fit
    anywhere in the range (can happen with narrow ranges), falls back to
    the closest available tens digit instead."""
    lo = max(lo, 100)
    target_mid = (lo + hi) / 2.0
    target_tens = (value // 10) % 10

    def best_for_tens(tens_digit):
        best, best_dist = None, None
        for hundreds in range(0, 10000, 100):
            candidate = hundreds + tens_digit * 10
            if lo <= candidate <= hi:
                dist = abs(candidate - target_mid)
                if best_dist is None or dist < best_dist:
                    best_dist, best = dist, candidate
        return best

    exact = best_for_tens(target_tens)
    if exact is not None:
        return exact
    # No candidate with the exact tens digit fits -- try progressively
    # further tens digits (both directions) until one fits.
    for offset in range(1, 10):
        for d in ((target_tens + offset) % 10, (target_tens - offset) % 10):
            candidate = best_for_tens(d)
            if candidate is not None:
                return candidate
    return lo


def apply_recolor_pairs(working, search_block, max_orders, dp_group_avg, guaranteed_strong_ids):
    """Roll every recolor-pair original normally, write it, then derive
    each recolor's stats (tens-digit matched per stat, own element/tier
    range, own strongest-attack order) and write those too.

    Handles chains correctly (e.g. Angemon -> Devimon -> IceDevimon,
    where Devimon is both a recolor AND an original for something else):
    stats are computed recursively and cached, so a card's own recolors
    are always derived from its FINAL stats, no matter which order the
    dict happens to iterate in.

    Returns the set of card names already handled, so the main loop
    skips them."""
    print("\n[*] Applying recolor pairs (Exception 2 + merged Exception 3) ...")
    by_name = {c["name"]: c for c in CARD_DATABASE}
    stats_cache = {}
    handled = set()

    def roll_and_write(card):
        """Roll a card normally (its own element/tier/order) and write it --
        or, in semi/hand mode, use USER_BASE_STATS instead. Either way, the
        recolor(s) derived from this card use whatever it ends up with."""
        name = card["name"]
        hp_off, _ = _locate_card(working, search_block, card)
        if hp_off is None:
            print(f"    [WARNING] Could not locate '{name}'.")
            return None
        triangle_off = find_triangle_offset(working, hp_off)
        if triangle_off is None:
            print(f"    [WARNING] '{name}': no reliable Triangle offset found.")
            return None
        cross_off = find_cross(working, triangle_off, hp_off)
        has_cross = cross_off is not None

        if STAT_MODE in ("semi", "hand") and name in USER_BASE_STATS:
            base = USER_BASE_STATS[name]
            if STAT_MODE == "semi":
                new_hp = semi_randomize_stat(base["HP"], card["stage"])
                new_circle = semi_randomize_stat(base["Circle"], card["stage"])
                new_triangle = semi_randomize_stat(base["Triangle"], card["stage"])
                new_cross = semi_randomize_stat(base["Cross"], card["stage"]) if has_cross else 0
            else:
                new_hp = hand_altered_stat(base["HP"])
                new_circle = hand_altered_stat(base["Circle"])
                new_triangle = hand_altered_stat(base["Triangle"])
                new_cross = hand_altered_stat(base["Cross"]) if has_cross else 0
            write_le16(working, hp_off, new_hp)
            write_le16(working, hp_off + 2, new_circle)
            write_le16(working, triangle_off, new_triangle)
            if has_cross and cross_off + 2 <= len(working):
                write_le16(working, cross_off, new_cross)
            return {"HP": new_hp, "Circle": new_circle, "Triangle": new_triangle, "Cross": new_cross}

        elem, stage, order = card["element"], card["stage"], card["order"]
        tier = STAT_RANGES[elem][stage]
        max_ord = max_orders[(elem, stage)]
        is_strong = card.get("card_id") in guaranteed_strong_ids
        boost = dp_secondary_factor(name, elem, stage, DP_DATA, dp_group_avg)
        hp_range = (int(tier["HP"][0] * boost), int(tier["HP"][1] * boost))
        circle_range = (int(tier["Circle"][0] * boost), int(tier["Circle"][1] * boost))
        triangle_range = (int(tier["Triangle"][0] * boost), int(tier["Triangle"][1] * boost))
        new_hp, frac_hp = weighted_rand_stat_v2(*hp_range, order, max_ord, 0.0, is_strong)
        new_circle, frac_c = weighted_rand_stat_v2(*circle_range, order, max_ord, frac_hp, is_strong)
        new_triangle, frac_t = weighted_rand_stat_v2(*triangle_range, order, max_ord, max(frac_hp, frac_c), is_strong)
        new_cross = 0
        if has_cross:
            cross_range = (int(tier["Cross"][0] * boost), int(tier["Cross"][1] * boost))
            prior = max(frac_hp, frac_c, frac_t)
            new_cross, _ = weighted_rand_stat_v2(*cross_range, order, max_ord, prior, is_strong)
        write_le16(working, hp_off, new_hp)
        write_le16(working, hp_off + 2, new_circle)
        write_le16(working, triangle_off, new_triangle)
        if cross_off is not None and cross_off + 2 <= len(working):
            write_le16(working, cross_off, new_cross)
        return {"HP": new_hp, "Circle": new_circle, "Triangle": new_triangle, "Cross": new_cross}

    def derive_and_write(card, source_stats):
        """Derive a recolor's stats from its source's FINAL stats and write them."""
        name = card["name"]
        hp_off, _ = _locate_card(working, search_block, card)
        if hp_off is None:
            print(f"    [WARNING] Could not locate '{name}'.")
            return None
        tier = STAT_RANGES[card["element"]][card["stage"]]
        r_hp = _tens_match(source_stats["HP"], *tier["HP"])
        r_circle = _tens_match(source_stats["Circle"], *tier["Circle"])
        r_triangle = _tens_match(source_stats["Triangle"], *tier["Triangle"])
        r_cross = _tens_match(source_stats["Cross"], *tier["Cross"])
        triangle_off = find_triangle_offset(working, hp_off)
        if triangle_off is None:
            print(f"    [WARNING] '{name}': no reliable Triangle offset found.")
            return None
        cross_off = find_cross(working, triangle_off, hp_off)
        write_le16(working, hp_off, r_hp)
        write_le16(working, hp_off + 2, r_circle)
        write_le16(working, triangle_off, r_triangle)
        if cross_off is not None and cross_off + 2 <= len(working):
            write_le16(working, cross_off, r_cross)
        return {"HP": r_hp, "Circle": r_circle, "Triangle": r_triangle, "Cross": r_cross}

    def get_final_stats(name):
        """Recursively resolve a card's final stats: if it's a recolor of
        something else, that source is resolved (and written) FIRST."""
        if name in stats_cache:
            return stats_cache[name]
        card = by_name.get(name)
        if card is None:
            print(f"    [WARNING] '{name}' not in CARD_DATABASE.")
            return None
        source_name = RECOLOR_TO_ORIGINAL.get(name)
        if source_name is not None:
            source_stats = get_final_stats(source_name)
            stats = derive_and_write(card, source_stats) if source_stats else None
        else:
            stats = roll_and_write(card)
        if stats is not None:
            stats_cache[name] = stats
            handled.add(name)
        return stats

    all_names = set(RECOLOR_PAIRS.keys()) | set(RECOLOR_TO_ORIGINAL.keys())
    for name in all_names:
        get_final_stats(name)

    print(f"    {len(handled)} cards handled via recolor pairs")
    return handled


def armor_digimon_fixed_stats(name):
    """Returns (hp, circle, triangle, cross) for an Armor Digimon: HP
    tripled, attacks doubled and re-sorted into strongest->weakest order
    per the card's real color identity.

    Exception: if the card's original Cross is 0 (Counter/Crash-type
    ability, never a real attack value), Cross is left untouched at its
    own doubled value (still 0) and is NOT part of the re-sort -- only
    Circle and Triangle get sorted against each other, per the color's
    order with Cross skipped."""
    hp, circle, triangle, cross = ARMOR_DIGIMON_ORIGINAL_STATS[name]
    elem = ARMOR_DIGIMON_ELEMENT[name]
    order = ELEMENT_ATTACK_ORDER[elem]  # e.g. ["Circle","Cross","Triangle"]

    if cross == 0:
        # Cross stays put (doubled, still 0); sort only Circle/Triangle
        # against each other, in the order the color's list gives them
        # (with Cross removed).
        remaining_order = [s for s in order if s != "Cross"]  # e.g. ["Circle","Triangle"]
        doubled_sorted = sorted([circle * 2, triangle * 2], reverse=True)
        slot_value = dict(zip(remaining_order, doubled_sorted))
        slot_value["Cross"] = 0
    else:
        doubled_sorted = sorted([circle * 2, triangle * 2, cross * 2], reverse=True)
        slot_value = dict(zip(order, doubled_sorted))

    return hp * 3, slot_value["Circle"], slot_value["Triangle"], slot_value["Cross"]

# Cards whose Cross (Bx) attack has "None" as its special ability tag (a
# plain attack with no bonus condition — e.g. "Goburi Rush (300), None"),
# per the official data. NOT the same as 0 power — Imperialdramon's Cross
# is "Shining Blade (0), B c Counter" and correctly does NOT qualify, since
# it has a real ability, just 0 base power.
NO_ABILITY_CROSS_CARDS = {
    "Gigadramon", "RedVegiemon", "Flarerizamon", "Goburimon", "Mojyamon",
    "SnowGoburimon", "Piximon", "Leomon", "Drimogemon", "J-Mojyamon",
    "GranKuwagamon", "Andromon", "Devidramon", "Tuskmon", "Fugamon",
    "Zassomon", "Geremon", "MudFrigimon", "L-ToyAgumon",
}


def weighted_rand_stat_v2(lo, hi, order, max_order, prior_frac=0.0, guaranteed_strong=False):
    """Order-weighted stat roll that also returns how high (0-1) the result
    landed within the FULL [lo, hi] range, so callers can chain multiple
    stat rolls for the same card with anti-correlation.

    guaranteed_strong: card is among the top-order cards for its color+stage
    (e.g. Omnimon, Vikemon) — always rolls in the top band of the range,
    every stat, no anti-correlation penalty.
    """
    span = hi - lo
    if span <= 0:
        return lo, 0.0

    if guaranteed_strong:
        band_lo = lo + int(span * GUARANTEED_STRONG_MIN_FRAC)
        band_hi = hi
    else:
        if max_order == 0:
            band_lo, band_hi = lo, hi
        else:
            bias    = order / max_order
            center  = lo + int(span * bias)
            half_w  = int(span * 0.40)
            band_lo = max(lo, center - half_w)
            band_hi = min(hi, center + half_w)
        if prior_frac > 0:
            shrink  = int((band_hi - band_lo) * prior_frac * ANTI_CORRELATION_STRENGTH)
            band_hi = max(band_lo, band_hi - shrink)

    if band_lo > band_hi:
        band_lo = band_hi
    lo10 = ((band_lo + 9) // 10) * 10
    hi10 = (band_hi // 10) * 10
    if lo10 > hi10:
        lo10 = hi10
    choices = list(range(lo10, hi10 + 1, 10))
    val = random.choice(choices) if choices else lo10
    frac = (val - lo) / span
    return val, frac


def compute_guaranteed_strong_ids(db):
    """Top 3 highest-`order` cards in each (element, stage) group — the
    'only obtained late-game' flagship cards (Omnimon, Vikemon, etc.) —
    always roll strong on every stat."""
    from collections import defaultdict
    groups = defaultdict(list)
    for c in db:
        if c.get("card_id") is None:
            continue
        groups[(c["element"], c["stage"])].append(c)
    strong_ids = set()
    for key, cards in groups.items():
        top3 = sorted(cards, key=lambda c: c["order"], reverse=True)[:3]
        for c in top3:
            strong_ids.add(c["card_id"])
    return strong_ids


def build_max_orders(db):
    maxes = {}
    for card in db:
        key = (card["element"], card["stage"])
        maxes[key] = max(maxes.get(key, 0), card["order"])
    return maxes


def build_dp_group_averages(db, dp_data):
    """Average DP per (element, stage) group, for cards we have DP data on."""
    sums, counts = {}, {}
    for card in db:
        dp = dp_data.get(card["name"])
        if dp is None:
            continue
        key = (card["element"], card["stage"])
        sums[key] = sums.get(key, 0) + dp
        counts[key] = counts.get(key, 0) + 1
    return {k: sums[k] / counts[k] for k in sums}


def dp_secondary_factor(card_name, element, stage, dp_data, dp_group_avg):
    """Small secondary multiplier (order remains primary) — a card with
    notably lower DP than its group average gets its roll range nudged
    down a bit; higher DP nudges up a bit. Capped to a modest +/-10%."""
    dp = dp_data.get(card_name)
    key = (element, stage)
    avg = dp_group_avg.get(key)
    if dp is None or avg is None or avg == 0:
        return 1.0
    ratio = dp / avg
    # clamp the influence so this stays clearly secondary to order
    adjustment = max(-0.10, min(0.10, (ratio - 1.0) * 0.20))
    return 1.0 + adjustment


import re
import struct

# =============================================================================
# OPTION CARD SECTION — complete rewrite
# =============================================================================
#
# KEY FINDINGS FROM HEX ANALYSIS:
#
# 1. Game reads ASCII text for all option card values — NOT binary header.
# 2. Values appear in these formats:
#    a) "+NNN." or "+NNN," — most cards
#    b) "NNN " (plain digits + space) — Digi-Aquamarine ("100 HP.")
#    c) "NNN\x00" (plain digits + null) — Digi-Amethyst ("Recover own\x00100\x00")
# 3. Scanner must be IDEMPOTENT — works on both fresh and pre-modified files
#    by searching for ANY +digits. pattern, not a specific original value.
# 4. Card boundary: next card starts with XX XX 01 [Letter][Letter][Letter|space]
#    where XX XX is non-zero card ID. Text fragments starting "00 00 01" are
#    rejected since card IDs are never 00 00.
# 5. Level Manager has no card ID bytes — comes right after encrypted block.
#    Located by footer pattern "03 50 48 02" before "01 Level Manager\x00".
#
# =============================================================================



# =============================================================================
# OPTION CARD SECTION - Complete rewrite based on confirmed binary structure
# =============================================================================
#
# CONFIRMED: The game reads binary LE16 values for gameplay effects.
# ASCII text is display only. Both must be updated.
#
# Binary value structure (always consistent):
#   01 [opcode_a] 00 00 00 00 [opcode_b] 00 00 00 [VALUE_LE16] 00 00 00 00
#   VALUE is always at opcode_start + 10 bytes
#
# Opcode pairs confirmed:
#   0A/0B = attack power boost
#   02/03 = HP recovery
#   30/xx = special (Aquamarine revive)
#
# Premium Steak has TWO binary value blocks (own HP + foe HP).
# =============================================================================

OPTION_SEARCH_OFFSET = 0x02650000
OPTION_SEARCH_END    = 0x02700000
OPTION_SCAN_WINDOW   = 400
OPTION_ID_MIN        = 191
OPTION_ID_MAX        = 300


def option_weighted(lo, hi, card_id):
    """Lower card_id = stronger = top of range. Values are multiples of 100."""
    span   = hi - lo
    bias   = 1.0 - (card_id - OPTION_ID_MIN) / (OPTION_ID_MAX - OPTION_ID_MIN)
    center = lo + int(span * bias)
    half_w = int(span * 0.25)
    eff_lo = max(lo, center - half_w)
    eff_hi = min(hi, center + half_w)
    if eff_lo > eff_hi:
        eff_lo = eff_hi
    lo100 = int(round(eff_lo / 100)) * 100
    hi100 = int(round(eff_hi / 100)) * 100
    if lo100 < lo: lo100 += 100
    if hi100 > hi: hi100 -= 100
    if lo100 > hi100: lo100 = hi100
    choices = list(range(lo100, hi100 + 1, 100))
    return random.choice(choices) if choices else lo100


def find_binary_value(file_bytes, name_abs, name_len, orig_val, scan_window=400):
    """
    Find the binary LE16 value block after the card name.
    Pattern: 01 XX 00 00 00 00 YY 00 00 00 [VALUE] 00 00 00 00
    VALUE is at opcode_start + 10.
    Returns offset of VALUE or None.
    """
    scan_start = name_abs + name_len
    scan_end   = min(scan_start + scan_window, len(file_bytes) - 12)
    orig_bytes = struct.pack('<H', orig_val)

    for pos in range(scan_start, scan_end):
        # Look for: 01 XX 00 00 00 00 YY 00 00 00 [VALUE] 00 00
        if (file_bytes[pos] == 0x01 and
                file_bytes[pos + 2] == 0x00 and
                file_bytes[pos + 3] == 0x00 and
                file_bytes[pos + 4] == 0x00 and
                file_bytes[pos + 5] == 0x00 and
                file_bytes[pos + 7] == 0x00 and
                file_bytes[pos + 8] == 0x00 and
                file_bytes[pos + 9] == 0x00 and
                file_bytes[pos + 10:pos + 12] == orig_bytes and
                file_bytes[pos + 12] == 0x00 and
                file_bytes[pos + 13] == 0x00):
            return pos + 10
    return None


def find_all_binary_values(file_bytes, name_abs, name_len, orig_val, scan_window=400):
    """Find ALL binary value blocks with orig_val (for multi-value cards like Premium Steak)."""
    results = []
    scan_start = name_abs + name_len
    scan_end   = min(scan_start + scan_window, len(file_bytes) - 12)
    orig_bytes = struct.pack('<H', orig_val)

    for pos in range(scan_start, scan_end):
        if (file_bytes[pos] == 0x01 and
                file_bytes[pos + 2] == 0x00 and
                file_bytes[pos + 3] == 0x00 and
                file_bytes[pos + 4] == 0x00 and
                file_bytes[pos + 5] == 0x00 and
                file_bytes[pos + 7] == 0x00 and
                file_bytes[pos + 8] == 0x00 and
                file_bytes[pos + 9] == 0x00 and
                file_bytes[pos + 10:pos + 12] == orig_bytes and
                file_bytes[pos + 12] == 0x00 and
                file_bytes[pos + 13] == 0x00):
            results.append(pos + 10)
    return results


def update_ascii_value(file_bytes, name_abs, name_len, old_val, new_val, scan_window=600):
    """
    Update ASCII +NNN. / +NNN, display text and plain NNN\x00 text.
    Returns count of replacements.
    """
    old_digits = str(old_val).encode('ascii')
    new_digits = str(new_val).encode('ascii')
    extra      = len(new_digits) - len(old_digits)
    scan_start = name_abs + name_len
    scan_end   = min(scan_start + scan_window, len(file_bytes))
    count      = 0

    for term in [b'.', b',']:
        old_str = b'+' + old_digits + term
        new_str = b'+' + new_digits + term
        pos = scan_start
        end = min(scan_end, len(file_bytes) - len(new_str) - 1)
        while pos < end:
            if file_bytes[pos:pos + len(old_str)] == old_str:
                if extra > 0:
                    if file_bytes[pos + len(old_str)] != 0x00:
                        pos += 1
                        continue
                    file_bytes[pos:pos + len(new_str)] = new_str
                    file_bytes[pos + len(new_str)] = 0x00
                    orphan = pos + len(new_str) + 1
                    if orphan < len(file_bytes) and 0x30 <= file_bytes[orphan] <= 0x39:
                        file_bytes[orphan] = 0x00
                elif extra < 0:
                    file_bytes[pos:pos + len(new_str)] = new_str
                    for i in range(len(new_str), len(old_str)):
                        file_bytes[pos + i] = 0x00
                    file_bytes[pos + len(new_str)] = term[0]
                else:
                    file_bytes[pos:pos + len(new_str)] = new_str
                count += 1
                pos += len(new_str)
            else:
                pos += 1

    # Also update plain NNN. (no + prefix, Holy Sevens style)
    old_nodot = old_digits + b'.'
    new_nodot = new_digits + b'.'
    pos = scan_start
    end = min(scan_end, len(file_bytes) - len(new_nodot) - 1)
    while pos < end:
        if file_bytes[pos:pos + len(old_nodot)] == old_nodot:
            prev = file_bytes[pos - 1] if pos > 0 else 0
            if prev != ord('+') and not (0x30 <= prev <= 0x39):
                file_bytes[pos:pos + len(new_nodot)] = new_nodot
                if extra < 0:
                    for i in range(len(new_nodot), len(old_nodot)):
                        file_bytes[pos + i] = 0x00
                count += 1
                pos += len(new_nodot)
                continue
        pos += 1

    # Also update plain NNN + null (Amethyst style)
    old_plain = old_digits + bytes([0x00])
    new_plain = new_digits + bytes([0x00])
    pos = scan_start
    end = min(scan_end, len(file_bytes) - len(new_plain) - 1)
    while pos < end:
        if file_bytes[pos:pos + len(old_plain)] == old_plain:
            prev = file_bytes[pos - 1] if pos > 0 else 0
            if prev != ord('+') and not (0x30 <= prev <= 0x39):
                if extra > 0 and file_bytes[pos + len(old_plain)] != 0x00:
                    pos += 1
                    continue
                file_bytes[pos:pos + len(new_plain)] = new_plain
                if extra < 0:
                    for i in range(len(new_plain), len(old_plain)):
                        file_bytes[pos + i] = 0x00
                count += 1
                pos += len(new_plain)
                continue
        pos += 1

    # Also update plain NNN + space (Aquamarine style)
    old_space = old_digits + bytes([0x20])
    new_space = new_digits + bytes([0x20])
    pos = scan_start
    end = min(scan_end, len(file_bytes) - len(new_space) - 1)
    while pos < end:
        if file_bytes[pos:pos + len(old_space)] == old_space:
            prev = file_bytes[pos - 1] if pos > 0 else 0
            if prev != ord('+') and not (0x30 <= prev <= 0x39):
                file_bytes[pos:pos + len(new_space)] = new_space
                count += 1
                pos += len(new_space)
                continue
        pos += 1

    return count


def make_option_search(card):
    """Build search bytes for an option card."""
    if "search" in card:
        return card["search"]
    card_id = card["card_id"]
    name    = card["name"]
    id_low  = card_id & 0xFF
    id_high = (card_id >> 8) & 0xFF
    return bytes([id_low, id_high, 0x01]) + name.encode("ascii") + b"\x00"


def resolve_paired_hp(card_id):
    """For multi-value 'own + foe' HP cards (currently only Premium Steak).

    BUG FIX (was): both slots called resolve_option_value('hp', card_id)
    independently, so the 'foe' roll and the 'own' roll came from the same
    600-2000 range with no relationship — roughly half the time the foe
    would randomly end up healthier than the player, inverting the card's
    intent (verified against ROM bytes: own-HP block is written first,
    opcode 02/03, value 500; foe-HP block second, opcode 03/04, value 200;
    ASCII text confirms "Recover own HP by +500. Recover foe's HP by
    +200." — own is always meant to be larger).

    Fix: roll 'own' first from the normal hp range, then derive 'foe' as a
    smaller fraction of it (30%-50%, same ballpark as the original 500:200
    = 40% ratio), rounded to the nearest 100, minimum 100. Own > foe is
    guaranteed every time.
    """
    own = option_weighted(600, 2000, card_id)
    foe = int(round((own * random.uniform(0.30, 0.50)) / 100)) * 100
    foe = max(100, foe)
    if foe >= own:
        foe = max(100, own - 100)
    return own, foe


def resolve_option_value(val_type, card_id):
    if val_type is None:
        return None
    if val_type.startswith("fixed_"):
        return int(val_type.split("_")[1])
    if val_type == "atk":
        return option_weighted(300, 900, card_id)
    if val_type == "hp":
        return option_weighted(600, 2000, card_id)
    if val_type == "atk_digivice":
        return option_weighted(500, 1000, card_id)
    if val_type == "hp_digivice":
        return option_weighted(800, 1200, card_id)
    if val_type == "atk_digivice_pink":
        return option_weighted(1000, 2000, card_id)
    if val_type == "hp_digivice_pink":
        return option_weighted(1600, 2400, card_id)
    return None


# Database: (orig_val, type)
# orig_val: original binary value the game stores
# type: determines new value range
OPTION_DATABASE = [
    {"name": "Devil's Chip",     "card_id": 192, "values": [(600,  "fixed_1200")]},
    {"name": "Mega Rec. Floppy", "card_id": 197, "values": [(1000, "fixed_3000")]},
    {"name": "Mega Attack Chip", "card_id": 198, "values": [(500,  "fixed_1500")]},
    {"name": "Dark Lord's Cape", "card_id": 199, "values": [(400,  "fixed_800")]},
    {"name": "Beetle Diamond",   "card_id": 204, "values": [(100,  "fixed_600")]},
    {"name": "Red Digivice",     "card_id": 206, "values": [(100,  "fixed_400"), (200, "fixed_800")]},
    {"name": "Blue Digivice",    "card_id": 207, "values": [(100,  "fixed_400"), (200, "fixed_800")]},
    {"name": "Green Digivice",   "card_id": 208, "values": [(100,  "fixed_400"), (200, "fixed_800")]},
    {"name": "Black Digivice",   "card_id": 209, "values": [(100,  "fixed_400"), (200, "fixed_800")]},
    {"name": "Yellow Digivice",  "card_id": 210, "values": [(100,  "fixed_400"), (200, "fixed_800")]},
    {"name": "Pink Digivice",    "card_id": 211, "values": [(200,  "fixed_800"), (400, "fixed_1600")]},
    {"name": "Coliseum",         "card_id": 215, "values": [(100,  "fixed_700")]},
    {"name": "Sup. Rec. Floppy", "card_id": 221, "values": [(700,  "fixed_1500")]},
    {"name": "Mega Def. Disk O", "card_id": 222, "values": [(100,  "fixed_900")],
     "search": b"\xde\x00\x01Mega Def. Disk \x2a\x62\x30"},
    {"name": "Mega Def. Disk T", "card_id": 223, "values": [(100,  "fixed_900")],
     "search": b"\xdf\x00\x01Mega Def. Disk \x2a\x62\x31"},
    {"name": "Mega Def. Disk X", "card_id": 224, "values": [(100,  "fixed_900")],
     "search": b"\xe0\x00\x01Mega Def. Disk \x2a\x62\x32"},
    {"name": "Level Balancer",   "card_id": 231, "values": [(400,  "fixed_1000")]},
    {"name": "Level Manager",    "card_id": 232, "values": [(400,  "fixed_1000")],
     "search": b"\x03\x50\x48\x02\x00\x00\x08\x00\x00\x00\x08\x00\x01Level Manager\x00",
     "name_offset": 12},
    {"name": "Level Booster",    "card_id": 233, "values": [(400,  "fixed_1000")]},
    {"name": "Miracle Ruby",     "card_id": 239, "values": [(1000, "fixed_2000")], "ascii_only": True},
    {"name": "Deluxe Mushroom",  "card_id": 242, "values": [(700,  "fixed_1200")]},
    {"name": "Lucky Mushroom",   "card_id": 243, "values": [(500,  "fixed_1500")]},
    # Premium Steak: two separate binary blocks, own HP + foe HP.
    # Fixed (not randomized) per balance pass: own +1200, foe +400.
    {"name": "Premium Steak",    "card_id": 244, "values": [(500,  "fixed_1200"), (200, "fixed_400")],
     "multi_binary": True, "name_pad": 21},
    {"name": "Med. Rec. Floppy", "card_id": 246, "values": [(500,  "fixed_1100")]},
    {"name": "Training Manual",  "card_id": 248, "values": [(100,  "fixed_1000")]},
    {"name": "Circle Hitter",    "card_id": 249, "values": [(500,  "fixed_800")]},
    {"name": "Triangle Hitter",  "card_id": 250, "values": [(500,  "fixed_800")]},
    {"name": "Cross Hitter",     "card_id": 251, "values": [(500,  "fixed_800")]},
    {"name": "Fire Spot",        "card_id": 258, "values": [(200,  "fixed_800")]},
    {"name": "Ice Crystal",      "card_id": 259, "values": [(200,  "fixed_1300")]},
    {"name": "Attack Chip",      "card_id": 264, "values": [(300,  "fixed_500")]},
    {"name": "Recovery Floppy",  "card_id": 266, "values": [(300,  "fixed_700")]},
    {"name": "Holy Sevens",      "card_id": 286, "values": [(1000, "fixed_4000")]},
    {"name": "Speed Sevens",     "card_id": 290, "values": [(200,  "fixed_1000")]},
]


def run_option_randomizer(file_bytes):
    search_block = file_bytes[OPTION_SEARCH_OFFSET:OPTION_SEARCH_END]
    print(f"[*] Altering option cards ({len(OPTION_DATABASE)} cards) ...")

    ok = 0; not_found = 0; skipped = 0

    for card in OPTION_DATABASE:
        name        = card["name"]
        card_id     = card["card_id"]
        values      = card["values"]
        name_offset = card.get("name_offset", 0)
        multi       = card.get("multi_binary", False)

        if not values:
            skipped += 1
            continue

        search = make_option_search(card)
        rel    = search_block.find(search)

        if rel == -1:
            not_found += 1
            continue

        name_abs   = OPTION_SEARCH_OFFSET + rel + name_offset
        name_pad   = card.get("name_pad", 0)
        ascii_only = card.get("ascii_only", False)
        name_len   = len(search) - name_offset + name_pad
        results    = []
        all_ok     = True

        if multi:
            # Premium Steak: find all binary blocks then assign new values.
            # values[0] = own HP block (found first), values[1] = foe HP
            # block (found second) — confirmed by ROM byte trace.
            type_a, type_b = values[0][1], values[1][1]
            if type_a == "hp" and type_b == "hp":
                # Both random — use the paired resolver so own always rolls
                # higher than foe (see resolve_paired_hp() docstring).
                new_500, new_200 = resolve_paired_hp(card_id)
            else:
                # Fixed (or otherwise independent) values — resolve directly.
                new_500 = resolve_option_value(type_a, card_id)
                new_200 = resolve_option_value(type_b, card_id)

            # Use single-match find for 500 (avoids grabbing Lucky Mushroom's +500)
            off_500 = find_binary_value(
                file_bytes, name_abs, name_len, 500, scan_window=600)
            off_200 = find_binary_value(
                file_bytes, name_abs, name_len, 200, scan_window=600)

            bin_count = 0
            if off_500 is not None:
                struct.pack_into('<H', file_bytes, off_500, new_500)
                bin_count += 1
            if off_200 is not None:
                struct.pack_into('<H', file_bytes, off_200, new_200)
                bin_count += 1

            asc_500 = update_ascii_value(
                file_bytes, name_abs, name_len, 500, new_500, scan_window=600)
            asc_200 = update_ascii_value(
                file_bytes, name_abs, name_len, 200, new_200, scan_window=600)

            if bin_count > 0:
                found_500 = "OK" if off_500 else "NOT FOUND"
                found_200 = "OK" if off_200 else "NOT FOUND"
                results.append(
                    f"500->{new_500} (bin {found_500}, ascii x{asc_500}), "
                    f"200->{new_200} (bin {found_200}, ascii x{asc_200})")
            else:
                all_ok = False
                results.append("no binary values found")
        else:
            for orig_val, val_type in values:
                new_val = resolve_option_value(val_type, card_id)
                if new_val is None:
                    continue

                if ascii_only:
                    # Card uses non-standard binary format - update display only
                    asc_count = update_ascii_value(
                        file_bytes, name_abs, name_len, orig_val, new_val)
                    results.append(f"{orig_val}->{new_val} (ascii-only x{asc_count})")
                else:
                    # Find and replace binary value
                    bin_off = find_binary_value(
                        file_bytes, name_abs, name_len, orig_val)
                    if bin_off is None:
                        all_ok = False
                        results.append(f"{orig_val}->{new_val} (binary not found)")
                        continue

                    struct.pack_into('<H', file_bytes, bin_off, new_val)

                    # Update ASCII display text
                    asc_count = update_ascii_value(
                        file_bytes, name_abs, name_len, orig_val, new_val)

                    results.append(
                        f"{orig_val}->{new_val} (bin+ascii x{asc_count})")

        if all_ok:
            ok += 1
        else:
            not_found += 1

    print(f"    options: {ok} modified, {not_found} not found, {skipped} skipped")







# --- Card tier system, by in-game rank within each color+stage ---
# Rank 1 = strongest (matches the game's own Card Menu numbering: lowest
# displayed number = strongest, highest = weakest).

# Ultimates: HARD exclusion — ranks 1..N never appear in a randomized deck
# at all (reserved as pure "flagship" cards, only found/earned late-game).
ULTIMATE_EXCLUDED_TOP_RANKS = 6

# Rookies/Champions: SOFT dampening instead of hard exclusion — the top N
# ranks can still appear (you can get "the strongest Rookie"), just rarely.
ROOKIE_CHAMP_DAMPEN_TOP_RANKS = 3
ROOKIE_CHAMP_DAMPEN_MULT = 0.15

# Max copies of any single card allowed in a randomized deck.
MAX_CARD_COPIES = 2

# A Digivice can only be drawn into a deck of its own matching color; Pink
# Digivice (211) is excluded from every deck's draw pool entirely.
DIGIVICE_ELEMENT = {206: 'Fire', 207: 'Ice', 208: 'Nature', 209: 'Darkness', 210: 'Rare'}
PINK_DIGIVICE_ID = 211


def filter_digivices_for_colors(pool, colors):
    """Drop Pink Digivice and any Digivice that doesn't match one of the
    deck's own colors from an option-card pool. Non-Digivice cards pass
    through untouched."""
    colors = set(colors) if colors else set()
    out = []
    for cid in pool:
        if cid == PINK_DIGIVICE_ID:
            continue
        card_color = DIGIVICE_ELEMENT.get(cid)
        if card_color is not None and card_color not in colors:
            continue
        out.append(cid)
    return out


# Option card random pool for the 5 free slots
OPTION_RANDOM_POOL = [
    249,  # Circle Hitter
    250,  # Triangle Hitter
    251,  # Cross Hitter
    258,  # Fire Spot
    259,  # Ice Crystal
    264,  # Attack Chip       (duplicate possible)
    266,  # Recovery Floppy   (duplicate possible)
    267,  # Attack Disk O
    248,  # Training Manual
    242,  # Deluxe Mushroom
    243,  # Lucky Mushroom
]

# ---- internal constants (do not change) ------------------------------------

_MCR_SAVE_BASE   = {'A': 0x4000, 'B': 0x8000, 'C': 0xC000}
_SAVE_SIZE       = 0x4000
_DECK_REL        = 0x2650
_PLAYER_NAME_REL = 0x0200
_DECK_NAME_REL   = 0x2639
_ENTRY_SIZE      = 8
_NUM_SLOTS       = 30

_PARTNER_IDS = {
    'Fire':     175,   # Veemon       (0xAF)  — confirmed
    'Nature':   182,   # Hawkmon      (0xB6)  — confirmed
    'Rare':     190,   # Armadillomon (0xBE)  — confirmed
    'Ice':      None,  # Patamon — ROM scan pending
    'Darkness': None,  # Wormmon  — ROM scan pending
}

_PARTNER_ELEMENTS = {
    'V': 'Fire',
    'H': 'Nature',
    'A': 'Rare',
}

_TEMPLATE_PATHS = {
    'Fire':    None,
    'Nature':  None,
    'Rare':    None,
}

_COLOR_MENU = {
    '1': 'Fire',
    '2': 'Ice',
    '3': 'Nature',
    '4': 'Darkness',
    '5': 'Rare',
}

_DECK_NAMES = {
    'Fire':     'Red',
    'Ice':      'Blue',
    'Nature':   'Green',
    'Darkness': 'Black',
    'Rare':     'Yellow',
}

_OPTION_SPECIAL_BYTES = {
    295: bytes([0x02, 0x02, 0x27, 0x01]),  # Special Digivolve (derived — verify in-game)
    299: bytes([0x02, 0x06, 0x2b, 0x01]),  # Speed Digivolve
    293: bytes([0x02, 0x00, 0x25, 0x01]),  # Download Digivolve (corrected label — was mislabeled Coliseum)
    # Coliseum = 215, no longer needs a special entry: 215 <= 255, so the
    # standard _card_id_to_id_bytes() formula already handles it correctly.
    #
    # Wild/Holy/Dark/Grand/Mystic/Speed/Reverse Sevens = 285-291 (confirmed
    # real card IDs via direct text search) — NOT yet added here. Their
    # deck-array 4-byte encoding hasn't been verified against a real save,
    # unlike Special/Speed Digivolve above which were confirmed via live-save
    # diffing. Don't trust the standard high/low formula for these until
    # tested — verify before using them in an actual deck patch.
}


def _card_id_to_id_bytes(card_id):
    """Convert a numeric card ID to the 4 id_bytes stored in each deck entry."""
    if card_id in _OPTION_SPECIAL_BYTES:
        return _OPTION_SPECIAL_BYTES[card_id]
    if card_id <= 255:
        return bytes([0x00, card_id & 0xFF, card_id & 0xFF, 0x00])
    high = (card_id >> 8) & 0xFF
    low  = card_id & 0xFF
    return bytes([high, (low + 0x41) & 0xFF, low, high])


def _build_element_pools():
    """Return dict: element -> {stage -> list of (order, card_id)}."""
    pools = {}
    for card in CARD_DATABASE:
        cid   = card.get("card_id")
        elem  = card.get("element", "")
        stage = card.get("stage", "")
        order = card.get("order", 0)
        if cid is None or elem not in ("Fire", "Ice", "Nature", "Darkness", "Rare"):
            continue
        pools.setdefault(elem, {}).setdefault(stage, []).append((order, cid))
    return pools


def _rank_sorted_unique(pool_with_order):
    """Sort a color+stage pool strongest-to-weakest by order, dedup, and
    return [(rank, order, card_id), ...] with rank 1 = strongest. This rank
    is what matches the in-game Card Menu's own numbering (lowest number =
    strongest, highest number = weakest)."""
    sorted_desc = sorted(pool_with_order, key=lambda x: -x[0])
    seen, out = set(), []
    for order, cid in sorted_desc:
        if cid in seen:
            continue
        seen.add(cid)
        out.append((len(out) + 1, order, cid))
    return out


def eligible_pool_excluding_top_ranks(pool_with_order, excluded_top_ranks):
    """Hard exclusion: drop the top N strongest ranks entirely. Used for
    Ultimates — these should never appear in a randomized starter deck."""
    ranked = _rank_sorted_unique(pool_with_order)
    return [(order, cid) for rank, order, cid in ranked if rank > excluded_top_ranks]


def _weighted_pick(pool_with_order, n, unique=True, max_copies=None,
                    dampen_top_ranks=0, dampen_mult=1.0):
    """Pick n cards biased toward lower-ordered (weaker) cards. Optionally:
      - max_copies: cap how many times the same card can be picked (None = no cap)
      - dampen_top_ranks / dampen_mult: multiply the selection weight of the
        top N strongest ranks by dampen_mult (<1), making them rare without
        making them impossible — used for Rookies/Champions.
    """
    if not pool_with_order:
        return []
    ranked = _rank_sorted_unique(pool_with_order)
    max_ord = max(o for _, o, _ in ranked) or 1
    weighted = []
    for rank, order, cid in ranked:
        w = max_ord - order + 1
        if rank <= dampen_top_ranks:
            w *= dampen_mult
        weighted.append([w, cid])

    picked, counts, attempts = [], {}, 0
    while len(picked) < n and attempts < 5000:
        attempts += 1
        total = sum(w for w, _ in weighted)
        if total <= 0:
            break
        r = random.uniform(0, total)
        cumulative = 0
        for w, cid in weighted:
            cumulative += w
            if r <= cumulative:
                cur = counts.get(cid, 0)
                if unique and cur >= 1:
                    break
                if max_copies is not None and cur >= max_copies:
                    break
                picked.append(cid)
                counts[cid] = cur + 1
                break
    return picked


def build_deck(partner_element, primary_color, secondary_color=None):
    """Build a 30-card deck.

    partner_element : element whose partner card goes in slot 21
    primary_color   : element for Ultimates + majority of Rookies/Champs
    secondary_color : optional second element; Rookies/Champs split 50/50

    Tier rules:
      Ultimates      — top ULTIMATE_EXCLUDED_TOP_RANKS strongest per color
                        are HARD-excluded (never appear); picks come from
                        the remaining, weaker ranks.
      Rookies/Champs — top ROOKIE_CHAMP_DAMPEN_TOP_RANKS strongest per color
                        are still eligible, just heavily down-weighted (soft
                        exclusion) — "the strongest Rookie" can still show up.
      All tiers      — max MAX_CARD_COPIES of any single card.
    """
    partner_id = _PARTNER_IDS[partner_element]
    pools      = _build_element_pools()
    pp         = pools.get(primary_color, {})

    def ult_pick(color_pool, n):
        eligible = eligible_pool_excluding_top_ranks(color_pool.get("U", []), ULTIMATE_EXCLUDED_TOP_RANKS)
        return _weighted_pick(eligible, n, unique=True)

    def rc_pick(color_pool, stage, n):
        return _weighted_pick(color_pool.get(stage, []), n, unique=False,
                               max_copies=MAX_CARD_COPIES,
                               dampen_top_ranks=ROOKIE_CHAMP_DAMPEN_TOP_RANKS,
                               dampen_mult=ROOKIE_CHAMP_DAMPEN_MULT)

    if secondary_color:
        sec_p = pools.get(secondary_color, {})
        ultimates = ult_pick(pp, 2) + ult_pick(sec_p, 2)
        # Rookies 5+5, Champions 3+4
        rookies = rc_pick(pp, "R", 5) + rc_pick(sec_p, "R", 5)
        champs  = rc_pick(pp, "C", 3) + rc_pick(sec_p, "C", 4)
        # Dual-color: replace Speed Digivolve + 1 random with 2x Special Digivolve
        # Special Digivolve (295) lets you digivolve regardless of Specialty,
        # which suits a mixed deck better than Speed Digivolve (299).
        options = [295, 295, 266, 264, 265] + random.choices(OPTION_RANDOM_POOL, k=3)
    else:
        ultimates = ult_pick(pp, 4)
        rookies   = rc_pick(pp, "R", 10)
        champs    = rc_pick(pp, "C", 7)
        options   = [299, 266, 264, 265] + random.choices(OPTION_RANDOM_POOL, k=4)

    deck = ultimates + rookies + champs + [partner_id] + options
    while len(deck) < _NUM_SLOTS:
        deck.append(partner_id)
    return deck[:_NUM_SLOTS]


# =============================================================================
# BUILD-YOUR-OWN-DECK — player picks a focus card + a power level, and the
# script assembles a themed 30-card starter deck around that card's own
# evolution chain (or, for a Partner card, around its canon evolution +
# a random Ultimate spread + its Armor forms).
# =============================================================================

# Rookie -> Champion -> Ultimate(s), in order. A chain with more than one
# Ultimate entry represents a stacked-evolution line (e.g. Agumon's line
# has RealMetalGreymon then WarGreymon then the Elite-tier Omnimon I).
_BYOD_CHAINS = [
    ["Agumon", "Greymon", "RealMetalGreymon", "WarGreymon", "Omnimon I"],
    ["Biyomon", "Birdramon", "Garudamon", "Phoenixmon"],
    ["Biyomon", "Aquilamon", "Garudamon", "Phoenixmon"],
    ["Solarmon", "Tyrannomon", "MasterTyrannomon"],
    ["Goburimon", "Monochromon", "Vermilimon"],
    ["Veemon", "ExVeemon", "Paildramon", "Imperialdramon"],
    ["Candlemon", "Meramon", "Meteormon"],
    ["Candlemon", "Akatorimon", "Vermilimon"],
    ["Muchomon", "Apemon", "MasterTyrannomon"],
    ["Muchomon", "RedVegiemon", "Meteormon"],
    ["D-Otamamon", "Piddomon", "Gigadramon"],
    ["D-Otamamon", "BomberNanimon", "MetalGreymon"],
    ["Solarmon", "Centarumon", "MetalGreymon"],
    ["Solarmon", "Flarerizamon", "RealMetalGreymon"],
    ["Goburimon", "Tankmon", "Gigadramon"],
    ["Gabumon", "Garurumon", "WereGarurumon", "MetalGarurumon", "Omnimon II"],
    ["Gomamon", "Ikkakumon", "Zudomon", "Vikemon"],
    ["Betamon", "Seadramon", "WaruSeadramon", "MetalSeadramon"],
    ["Betamon", "Seadramon", "MegaSeadramon", "MetalSeadramon"],
    ["Otamamon", "Gekomon", "WaruSeadramon"],
    ["Gabumon", "IceDevimon", "WaruSeadramon"],
    ["Betamon", "Coelamon", "MegaSeadramon"],
    ["Penguinmon", "Whamon", "Brachiomon"],
    ["Penguinmon", "Hyogamon", "WaruSeadramon"],
    ["Gizamon", "Dolphmon", "BlueMeramon"],
    ["Gizamon", "Mojyamon", "Panjyamon"],
    ["Otamamon", "Gesomon", "MarineAngemon"],
    ["Otamamon", "Shellmon", "Brachiomon"],
    ["SnowAgumon", "Frigimon", "Zudomon"],
    ["SnowAgumon", "Sorcerimon", "MarineAngemon"],
    ["SnowGoburimon", "Icemon"],
    ["Patamon", "Angemon", "MagnaAngemon", "Seraphimon"],
    ["Salamon", "R-Gatomon", "Angewomon", "Magnadramon"],
    ["Tentomon", "Kabuterimon", "MegaKabuterimon", "HerculesKabuterimon"],
    ["Palmon", "Togemon", "Lillymon", "Rosemon"],
    ["Hawkmon", "Airdramon", "Sylphymon", "Valkyrimon"],
    ["Hawkmon", "Veedramon", "AeroVeedramon"],
    ["Tentomon", "Airdramon", "Piximon"],
    ["Tentomon", "Yanmamon"],
    ["Tentomon", "Kuwagamon"],
    ["Elecmon", "Drimogemon", "Piximon"],
    ["Elecmon", "Unimon", "Angewomon"],
    ["Elecmon", "Leomon"],
    ["Gotsumon", "Vegiemon"],
    ["Gotsumon", "Kokatorimon"],
    ["Kunemon", "Ninjamon", "Sylphymon"],
    ["Kunemon", "J-Mojyamon"],
    ["Kunemon", "MoriShellmon"],
    ["DemiDevimon", "Devimon", "Myotismon", "VenomMyotismon"],
    ["DemiDevimon", "Devidramon", "Infermon", "Diaboromon"],
    ["Wormmon", "Stingmon", "GranKuwagamon"],
    ["Kokuwamon", "Guardromon", "Machinedramon"],
    ["Sharmamon", "Ogremon", "SkullGreymon"],
    ["Kokuwamon", "Tekkamon", "Megadramon"],
    ["Kokuwamon", "Devidramon", "Piedmon", "Apokarimon"],
    ["BKGatomon", "Wizardmon", "LadyDevimon"],
    ["Tsukaimon", "Tuskmon", "Andromon"],
    ["Dokunemmon", "Gururumon", "Megadramon"],
    ["Dokunemmon", "Soulmon", "Phantomon"],
    ["Aruraumon", "Zassomon", "WaruMonzaemon"],
    ["Aruraumon", "Saberdramon", "WaruMonzaemon"],
    ["Sharmamon", "Darkrizamon", "Piedmon"],
    ["Sharmamon", "Zassomon"],
    ["Sharmamon", "Fugamon", "Apokarimon"],
    ["Dokunemmon", "Bakemon", "Phantomon"],
    ["Armadillomon", "Ankylomon", "Shakkoumon"],
    ["Hagurumon", "Starmon", "Puppetmon"],
    ["Hagurumon", "Starmon", "SuperStarmon"],
    ["L-ToyAgumon", "Rockmon", "Mamemon"],
    ["L-ToyAgumon", "Geremon", "MetalMamemon"],
    ["ToyAgumon", "Thundermon", "Giromon"],
    ["ToyAgumon", "NiseDrimogemon"],
    ["ClearAgumon", "PlatinumSukamon", "Monzaemon"],
    ["ClearAgumon", "ShimaUnimon", "Jijimon"],
    ["Vi-Elecmon", "ShellNumemon", "Digitamamon"],
    ["Vi-Elecmon", "MudFrigimon", "Etemon", "MetalEtemon"],
    ["Psychemon", "Nanimon", "Vademon"],
    ["Psychemon", "SandYanmamon"],
    ["ModokiBetamon", "Numemon", "Etemon", "MetalEtemon"],
    ["ModokiBetamon", "Sukamon", "Etemon", "MetalEtemon"],
]

_BYOD_PARTNER_CHAIN = {
    "Veemon": ["Veemon", "ExVeemon"],
    "Hawkmon": ["Hawkmon", "Airdramon"],
    "Patamon": ["Patamon", "Angemon"],
    "Gatomon": ["Gatomon", "R-Gatomon"],
    "Wormmon": ["Wormmon", "Stingmon"],
    "Armadillomon": ["Armadillomon", "Ankylomon"],
}
_BYOD_PARTNER_TO_ARMORS = {
    "Veemon": ["Flamedramon", "Raidramon", "Magnamon"],
    "Hawkmon": ["Halsemon", "Shurimon"],
    "Armadillomon": ["Digmon", "Submarimon"],
    "Patamon": ["Pegasusmon", "Baronmon"],
    "Gatomon": ["Nefertimon", "Tylomon"],
    "Wormmon": ["Shadramon", "Quetzalmon"],
}
_BYOD_PARTNER_ELEMENT = {
    "Veemon": "Fire", "Hawkmon": "Nature", "Patamon": "Nature",
    "Gatomon": "Nature", "Wormmon": "Darkness", "Armadillomon": "Rare",
}

# Option-card tiers (Low/Medium/High), collapsed from _OPTION_TIERS per the
# user-edited option_card_tiers_draft.txt.
_BYOD_OPTION_LOW = [270, 271, 272, 249, 250, 251, 300, 298, 263, 262, 261, 260,
    259, 258, 257, 247, 240, 239, 236, 238, 237, 234, 225, 216, 217, 218, 219,
    220, 295, 299, 296, 297, 264, 266, 267, 268, 269, 227, 226, 244, 246, 242,
    243, 233, 231]
_BYOD_OPTION_MEDIUM = [265, 256, 255, 254, 252, 248, 245, 235, 230, 222, 223,
    224, 221, 215, 214, 212, 202, 201, 194]
_BYOD_OPTION_HIGH = [198, 197, 253, 229, 228, 208, 206, 211, 210, 209, 205,
    204, 203, 213, 199, 196, 195, 193, 192, 191]
_BYOD_OPTION_POOL_FOR_POWER = {
    'Low': _BYOD_OPTION_LOW, 'Medium': _BYOD_OPTION_MEDIUM, 'High': _BYOD_OPTION_HIGH,
}

def _byod_option_pool_for_color(power_level, elem):
    pool = _BYOD_OPTION_POOL_FOR_POWER[power_level]
    return filter_digivices_for_colors(pool, [elem])

# Copy count of the focus card's own Rookie/Champion/Ultimate, keyed by
# [power level][focus card's own creature tier]. Weak cards get MORE copies
# to compensate for being weak; Strong cards get fewer since they don't
# need the help. "High" power is the deliberately aggressive/handicap-free
# setting (biggest numbers across the board).
_BYOD_NONELITE_COPY = {
    'Low':    {'Weak': 3, 'OK': 2, 'Strong': 1},
    'Medium': {'Weak': 4, 'OK': 3, 'Strong': 2},
    'High':   {'Weak': 4, 'OK': 4, 'Strong': 3},
}
# Copies of the focus card itself, when the focus card is Elite-tier.
_BYOD_ELITE_COPY = {'Low': 1, 'Medium': 1, 'High': 2}
# Which creature tier random external Ultimate top-up cards are drawn from,
# keyed by power level (used only when the focus chain itself can't supply
# all 4 required Ultimate-tier slots).
_BYOD_POWER_TO_CREATURE_TIER = {'Low': 'Weak', 'Medium': 'OK', 'High': 'Strong'}

# Fixed deck composition (always sums to exactly _NUM_SLOTS = 30), inclusive
# of the focus card's own evo-line copies -- not on top of them.
_BYOD_ROOKIE_SLOTS = 10
_BYOD_CHAMPION_SLOTS = 8
_BYOD_U_SLOTS = 4
_BYOD_OPTION_COUNT = 8

# Always included, 1 copy each, in every build-your-own-deck regardless of
# power level.
_BYOD_SPEED_DIGIVOLVE_ID = 299
_BYOD_WARP_DIGIVOLVE_ID = 297


_BYOD_NAME_TO_ID = None
_BYOD_ID_TO_CARD = None


def _byod_lookups():
    """Lazily build (and cache) the name->card_id and card_id->card maps
    used throughout build-your-own-deck. Built lazily rather than at
    module scope because it depends on _PARTNER_CARDS, which is defined
    later in the file."""
    global _BYOD_NAME_TO_ID, _BYOD_ID_TO_CARD
    if _BYOD_NAME_TO_ID is None:
        _BYOD_NAME_TO_ID = {c['name']: c['card_id'] for c in CARD_DATABASE if c.get('card_id') is not None}
        _BYOD_NAME_TO_ID.update({v: k for k, v in _PARTNER_CARDS.items()})
        _BYOD_ID_TO_CARD = {c['card_id']: c for c in CARD_DATABASE if c.get('card_id') is not None}
        # Partner cards (Veemon, Hawkmon, etc.) have card_id: None in
        # CARD_DATABASE itself -- their real ID only lives in _PARTNER_CARDS.
        # Without this, any chain whose Rookie is a Partner name (e.g. the
        # Fire chain "Veemon -> ExVeemon -> Paildramon -> Imperialdramon")
        # would crash creature-tier lookups for every OTHER card in that
        # chain, since the Rookie's tier couldn't be resolved.
        by_name = {c['name']: c for c in CARD_DATABASE}
        for partner_id, partner_name in _PARTNER_CARDS.items():
            if partner_name in by_name:
                _BYOD_ID_TO_CARD[partner_id] = by_name[partner_name]
    return _BYOD_NAME_TO_ID, _BYOD_ID_TO_CARD


def _byod_creature_tier(name):
    """Weak/OK/Strong/Elite classification for a Rookie/Champion/Ultimate
    card, split from CARD_DATABASE's per-element-per-stage 'order' field
    (matching creature_tiers_draft.txt). Elite/Mega flagship cards use
    ELITE_TIER_NAMES / MEGA_TIER_NAMES directly."""
    if name in ELITE_TIER_NAMES:
        return 'Elite'
    if name in MEGA_TIER_NAMES:
        return 'Strong'
    name_to_id, id_to_card = _byod_lookups()
    cid = name_to_id.get(name)
    card = id_to_card.get(cid)
    if not card:
        return None
    elem, stage = card['element'], card['stage']
    pool = sorted(
        [c for c in CARD_DATABASE if c.get('element') == elem and c.get('stage') == stage
         and c.get('card_id') is not None and c['name'] not in ELITE_TIER_NAMES],
        key=lambda c: -c.get('order', 0))
    n = len(pool)
    hi_n = -(-n // 3)
    mid_n = n - hi_n - (n // 3)
    names = [c['name'] for c in pool]
    if name in names[:hi_n]:
        return 'Strong'
    if name in names[hi_n:hi_n + mid_n]:
        return 'OK'
    return 'Weak'


def _byod_find_chain(focus_name):
    for chain in _BYOD_CHAINS:
        if focus_name in chain:
            return chain
    return None


def _byod_fill_stage(elem, stage, exclude_ids, need, max_copy=4):
    """Randomly fill `need` slots from same-color same-`stage` cards not in
    exclude_ids. If the distinct-card pool is smaller than `need`, cycles
    back through it adding extra copies (up to max_copy each) rather than
    silently coming up short."""
    result = {}
    if need <= 0:
        return result
    pool = [c['card_id'] for c in CARD_DATABASE if c.get('element') == elem
            and c.get('stage') == stage and c.get('card_id') is not None
            and c['card_id'] not in exclude_ids and c['name'] not in ELITE_TIER_NAMES]
    if not pool:
        return result
    random.shuffle(pool)
    i = 0
    guard = 0
    while need > 0 and guard < len(pool) * max_copy + 10:
        cid = pool[i % len(pool)]
        if result.get(cid, 0) < max_copy:
            result[cid] = result.get(cid, 0) + 1
            need -= 1
        i += 1
        guard += 1
    return result


def _byod_fill_ultimates(elem, preferred_tier, exclude_ids, need):
    """Fill `need` Ultimate-tier slots, preferring `preferred_tier` first
    and falling back to the other tiers (never Elite) if that tier alone
    doesn't have enough distinct cards to cover the gap."""
    result = {}
    if need <= 0:
        return result
    tier_order = [preferred_tier] + [t for t in ('Weak', 'OK', 'Strong') if t != preferred_tier]
    exclude = set(exclude_ids)
    for tier in tier_order:
        if need <= 0:
            break
        pool = [c['card_id'] for c in CARD_DATABASE if c.get('element') == elem and c.get('stage') == 'U'
                and c.get('card_id') is not None and c['card_id'] not in exclude
                and _byod_creature_tier(c['name']) == tier]
        random.shuffle(pool)
        for cid in pool:
            if need <= 0:
                break
            result[cid] = 1
            exclude.add(cid)
            need -= 1
    return result


def build_custom_starter_deck(focus_name, power_level, is_partner=False):
    """Build a 30-card starter deck centered on a player-chosen focus card
    (any Ultimate/Elite/Mega creature, or a Partner card) at a player-chosen
    power level (Low/Medium/High). Composition is always exactly 10 Rookie
    + 8 Champion + 4 Ultimate + 8 Option cards, inclusive of the focus
    card's own evo-line copies."""
    name_to_id, id_to_card = _byod_lookups()
    armor_id_lookup = {v: k for k, v in _ARMOR_CARDS.items()}

    rookie_targets, champ_targets, u_targets = {}, {}, {}

    if is_partner:
        chain = _BYOD_PARTNER_CHAIN[focus_name]
        rookie, champ = chain[0], chain[1]
        rookie_id, champ_id = name_to_id[rookie], name_to_id[champ]
        elem = _BYOD_PARTNER_ELEMENT[focus_name]

        rookie_targets[rookie_id] = 4
        champ_targets[champ_id] = 4

        armor_ids = [armor_id_lookup[a] for a in _BYOD_PARTNER_TO_ARMORS[focus_name]]
        # 1 armor -> Champion slot, 1 -> Ultimate slot; a 3rd (Veemon only)
        # -> Rookie slot. Partners with only 2 armors just use Champion+Ultimate.
        champ_targets[armor_ids[0]] = champ_targets.get(armor_ids[0], 0) + 1
        u_targets[armor_ids[1]] = u_targets.get(armor_ids[1], 0) + 1
        if len(armor_ids) == 3:
            rookie_targets[armor_ids[2]] = rookie_targets.get(armor_ids[2], 0) + 1
    else:
        chain = _byod_find_chain(focus_name)
        rookie, champ = chain[0], chain[1]
        rookie_id, champ_id, focus_id = name_to_id[rookie], name_to_id[champ], name_to_id[focus_name]
        tier = _byod_creature_tier(focus_name)
        elem = id_to_card[focus_id]['element']

        r_cap = _BYOD_NONELITE_COPY[power_level][_byod_creature_tier(rookie)]
        c_cap = _BYOD_NONELITE_COPY[power_level][_byod_creature_tier(champ)]
        focus_copy = (_BYOD_ELITE_COPY[power_level] if tier == 'Elite'
                      else _BYOD_NONELITE_COPY[power_level][tier])

        # Only add Rookie/Champion separately if they aren't literally the
        # same card as the focus (guards against malformed/short chain data).
        if rookie_id != focus_id:
            rookie_targets[rookie_id] = r_cap
        if champ_id != focus_id and champ_id != rookie_id:
            champ_targets[champ_id] = c_cap

        u_targets[focus_id] = focus_copy
        for u in chain[2:]:
            if u == focus_name or u in ELITE_TIER_NAMES:
                continue
            uid = name_to_id[u]
            if uid not in u_targets:
                u_targets[uid] = 1

        # Hard cap at exactly _BYOD_U_SLOTS: trim the chain's OTHER
        # Ultimates first, then the focus card's own copies as a last
        # resort, if the natural chain math supplies more than the budget.
        u_total = sum(u_targets.values())
        if u_total > _BYOD_U_SLOTS:
            trim_order = [uid for uid in u_targets if uid != focus_id]
            i = 0
            while u_total > _BYOD_U_SLOTS and i < len(trim_order):
                uid = trim_order[i]
                if u_targets[uid] > 0:
                    u_targets[uid] -= 1
                    u_total -= 1
                else:
                    i += 1
            while u_total > _BYOD_U_SLOTS and u_targets[focus_id] > 1:
                u_targets[focus_id] -= 1
                u_total -= 1
            u_targets = {uid: cnt for uid, cnt in u_targets.items() if cnt > 0}

    u_need = _BYOD_U_SLOTS - sum(u_targets.values())
    if u_need > 0:
        u_targets.update(_byod_fill_ultimates(elem, _BYOD_POWER_TO_CREATURE_TIER[power_level],
                                               set(u_targets), u_need))

    exclude = set(rookie_targets) | set(champ_targets) | set(u_targets)
    rookie_need = _BYOD_ROOKIE_SLOTS - sum(rookie_targets.values())
    champ_need = _BYOD_CHAMPION_SLOTS - sum(champ_targets.values())
    for cid, cnt in _byod_fill_stage(elem, 'R', exclude, rookie_need).items():
        rookie_targets[cid] = rookie_targets.get(cid, 0) + cnt
    for cid, cnt in _byod_fill_stage(elem, 'C', exclude, champ_need).items():
        champ_targets[cid] = champ_targets.get(cid, 0) + cnt

    # Every build-your-own deck always includes 1 Warp Digivolve; Speed
    # Digivolve is also always included, except at Low power. The remaining
    # option slots are randomly filled as usual.
    options = [_BYOD_WARP_DIGIVOLVE_ID]
    if power_level != 'Low':
        options.append(_BYOD_SPEED_DIGIVOLVE_ID)
    opt_pool = _byod_option_pool_for_color(power_level, elem)
    if power_level == 'Low':
        opt_pool = [cid for cid in opt_pool if cid != _BYOD_SPEED_DIGIVOLVE_ID]
    pool_cycle = opt_pool[:]
    random.shuffle(pool_cycle)
    remaining_opts = _BYOD_OPTION_COUNT - len(options)
    options += [pool_cycle[i % len(pool_cycle)] for i in range(remaining_opts)]

    deck = []
    for d in (rookie_targets, champ_targets, u_targets):
        for cid, cnt in d.items():
            deck.extend([cid] * cnt)
    deck.extend(options)
    assert len(deck) == _NUM_SLOTS, f"BYOD deck size mismatch: {len(deck)}"
    return deck


_BYOD_TIER_SORT_ORDER = {'Elite': 0, 'Strong': 1, 'OK': 2, 'Weak': 3}
_BYOD_COLOR_ORDER = ['Fire', 'Ice', 'Nature', 'Darkness', 'Rare']


def _byod_focus_card_menu():
    """Build the numbered, color-grouped focus-card menu. Returns a list of
    (number, name, is_partner) in display order, grouped by color and, within
    each color, Elite first then Strong/OK/Weak, Partners listed last in
    their color group."""
    by_color = {c: [] for c in _BYOD_COLOR_ORDER}
    for c in CARD_DATABASE:
        name = c['name']
        if not (c.get('stage') == 'U' or name in MEGA_TIER_NAMES or name in ELITE_TIER_NAMES):
            continue
        elem = c.get('element')
        if elem not in by_color:
            continue
        by_color[elem].append((name, False))
    for partner_name, elem in _BYOD_PARTNER_ELEMENT.items():
        by_color[elem].append((partner_name, True))

    entries = []
    num = 1
    for color in _BYOD_COLOR_ORDER:
        cards = by_color[color]
        cards.sort(key=lambda t: (t[1], _BYOD_TIER_SORT_ORDER.get(_byod_creature_tier(t[0]), 9), t[0]))
        for name, is_partner in cards:
            entries.append((num, color, name, is_partner))
            num += 1
    return entries


def prompt_focus_card():
    print("\n" + "=" * 64)
    print("  BUILD YOUR OWN DECK — FOCUS CARD")
    print("=" * 64)
    print("  Pick a number below, or type the card's name directly.\n")
    entries = _byod_focus_card_menu()
    by_number = {}
    by_name = {}
    current_color = None
    for num, color, name, is_partner in entries:
        if color != current_color:
            print(f"\n  -- {color} --")
            current_color = color
        print(f"  {num:>3}  {name}")
        by_number[str(num)] = (name, is_partner)
        by_name[name.lower()] = (name, is_partner)
    print()

    while True:
        ans = input("  Focus card (number or name): ").strip()
        if ans in by_number:
            return by_number[ans]
        match = by_name.get(ans.lower())
        if match:
            return match
        print("    (not a recognized number or Ultimate/Elite/Mega creature/Partner name — try again)")


def prompt_deck_power_level():
    print("\n" + "=" * 64)
    print("  BUILD YOUR OWN DECK — POWER LEVEL")
    print("=" * 64)
    print("  1 = Low")
    print("  2 = Medium")
    print("  3 = High\n")
    choice = _prompt("  Choice (1/2/3): ", valid=['1', '2', '3'])
    return {'1': 'Low', '2': 'Medium', '3': 'High'}[choice]




_BDRV_SIZE = 25077760
_BDRV_SIGNATURE = bytes.fromhex("800000000100000000000000282f3f3a43415244000000000000000000000000800000009003000000000000242f3f3a4d415443480000000000000000000000")

# =============================================================================
# ENGINE FIXES (SLUS_013.28 + P.DRV) — Armor Digimon / Digi-Jewel support
# =============================================================================
# Three independent bugs found via live debugging (DuckStation) while making
# Armor Digimon (card IDs 172-190) fully pack-drawable, collectible, and
# deck-legal instead of Digi-Egg-only items:
#
#   1. CRASH FIX: a duel-side rank-calculation routine (SLUS 0x80048230)
#      never got a valid per-slot data pointer for Armor Digimon, and
#      dereferencing the garbage pointer crashed the game the instant an
#      Armor Digimon was actually played in a duel. Fix: a small guard
#      routine (in previously-unused, empirically-verified-safe SLUS space)
#      checks the loaded pointer and substitutes a safe address if it's
#      garbage, instead of crashing.
#
#   2. COLLECTION FIX: the pack-grant/"add to collection" routine (SLUS
#      0x80045B18) had an explicit ID-range guard (172-190) that rejected
#      Armor Digimon early, which is why they showed "FULL SET!" and never
#      appeared in the collection (and separately caused the post-duel
#      EXP/reward screen to hang, since a "populate reward display" code
#      block downstream was only reached on the success path). Fix: make
#      that guard branch unconditionally take the normal/success path.
#
#   3. DECK-LIMIT FIX: a P.DRV routine that computes per-card deck-copy
#      data already correctly special-cases the *Partner* cards that share
#      the Armor ID range (175, 182, 183, 184, 187, 190) by giving them
#      full normal processing — but every other Armor ID either returns 0
#      early or gets diverted to an unrelated code path, which is why they
#      were stuck capped at 0 copies in the deck builder. Fix: make all
#      the sub-range guards in that routine fall through to the same
#      normal-processing path the Partner cards already use.
#
# All three fixes are pure instruction patches (no new code space needed
# beyond one small, empirically-verified-unused 32-byte gap for fix #1) and
# have been tested end-to-end: pack draws, collection screen, deck
# building (up to 4 copies), and full duels with Armor Digimon in play.

_SLUS_SIZE = 428032
_SLUS_SIGNATURE = bytes.fromhex(
    "50532d582045584500000000000000007062058000000000000001800080060000"
    "000000000000000000000000000000f0ff1f80000000000000000000000000"
)
_PDRV_SIZE = 610304
_PDRV_SIGNATURE = bytes.fromhex(
    "0142494e01000000642e000058d6ef3a454e44534547000000000000000000000"
    "142494e07000000747a010058d6ef3a45564f53454700000000000000000000"
)

# (file-relative offset -> replacement 4-byte little-endian instruction word)
_SLUS_FIXES = {
    0x38ac8: bytes.fromhex("5dbd0108"),  # crash-fix hook (was a nop)
    0x5fd74: bytes.fromhex(
        "020e040080ff21240300201000000000801f043c80008434b420010800000000"
    ),  # crash-fix guard routine (was 32 bytes of verified-unused padding)
    0x36340: bytes.fromhex("03000010"),  # collection fix (pack-grant Armor guard)
    0x5eb6b: bytes.fromhex("0f"),  # Basic Pack option-tier threshold: 0 -> 15 (admits Digi-Jewels)
}
_PDRV_FIXES = {
    0x7b798: bytes.fromhex("23000014"),  # deck-fix: sub-range guard #1
    0x7b7a8: bytes.fromhex("03000010"),  # deck-fix: sub-range guard #2
    0x7b7bc: bytes.fromhex("1a000014"),  # deck-fix: sub-range guard #3
    0x7b7c8: bytes.fromhex("00000000"),  # deck-fix: ID-188 special case, nop'd
    0x7b7d0: bytes.fromhex("00000000"),  # deck-fix: ID-189 special case, nop'd
}


# =============================================================================
# PACK ELIGIBILITY: Armor Digimon + Partners
# =============================================================================
# Each card's pack-eligibility "score" byte lives at record_base + 0x19
# (record_base = the byte right before the [id_lo, id_hi, 0x00] + name
# prefix). A card passes a given pack's per-element threshold if its score
# is <= that pack's threshold for its element nibble (record_base + 0x1A,
# high nibble) -- confirmed via live debugging. Score 0 is a hard sentinel
# that excludes a card from every pack regardless of threshold, which is
# why these cards never appeared anywhere before.
#
# The two shared score values below were chosen so the *existing* pack
# thresholds sort each group into exactly the intended packs with zero
# changes to the threshold table itself:
#
#   Armor Digimon (score 28): passes Great Pack, Super Pack, and their own
#   color's S-pack (all have thresholds >= 28 for every element) while
#   failing Basic, Hyper, the regular color packs, and Option packs (all
#   have thresholds < 28).
#
#   Partners (score 24): passes their own color pack, Hyper, Super, Great,
#   and their own color's S-pack (all >= 24), while failing only Basic
#   (< 24). Structurally, no shared score can pass Super without also
#   passing that color's S-pack (S-pack thresholds are always >= Super's
#   for the same element), so Partners land in S-packs too as a
#   consequence -- accepted tradeoff, confirmed with the user.
_ARMOR_SCORE = 28
_PARTNER_SCORE = 24

_ARMOR_CARDS = {
    172: "Flamedramon", 173: "Magnamon", 174: "Baronmon", 176: "Submarimon",
    177: "Quetzalmon", 178: "Tylomon", 179: "Halsemon", 180: "Pegasusmon",
    181: "Nefertimon", 185: "Raidramon", 186: "Shadramon", 188: "Shurimon",
    189: "Digmon",
}
_PARTNER_CARDS = {
    175: "Veemon", 182: "Hawkmon", 183: "Patamon", 184: "Gatomon",
    187: "Wormmon", 190: "Armadillomon",
}

# Digi-Jewels and Sevens are option-tier cards (header byte 3 == 1, not 0
# like monster/Armor records), and their pack-eligibility field lives at
# record_base + 0x1C -- 3 bytes further in than the monster-card score
# field, confirmed by diffing the user's own working test disc against the
# original. Option-tier eligibility is a single flat threshold per pack
# (table bytes 15-17), not per-element like monster cards.
#
#   Digi-Jewels (score 15): passes Option Pack (threshold 15). As an
#   unavoidable side effect of the same "higher-tier thresholds admit
#   lower scores too" structure seen with Partners, this also lands them
#   in Great Pack (threshold 99) and S-Option Pack (threshold 29).
#
#   Sevens (score 20): sits in the gap between Option/Super's thresholds
#   (15/10) and S-Option's (29), landing them in S-Option Pack and Great
#   Pack only -- cleanly excluded from everywhere else.
#
# Basic Pack's option-tier threshold is also raised from 0 to 15 (matching
# the Digi-Jewel score) so they're drawable there too, as requested. This
# only affects option-tier eligibility for Basic Pack -- monster cards use
# a completely separate part of the same table row (bytes 0-14) and are
# untouched by this change.
_DIGI_JEWEL_SCORE = 15
_SEVENS_SCORE = 20
_BASIC_PACK_OPTION_THRESHOLD_OFFSET = 0x5EB5C + 0 * 18 + 15  # Basic = row 0, byte 15

_DIGI_JEWEL_CARDS = {
    273: "Digi-Garnet", 274: "Digi-Amethyst", 275: "Digi-Aquamarine",
    276: "Digi-Diamond", 277: "Digi-Emerald", 278: "Digi-Pearl",
    279: "Digi-Ruby", 280: "Digi-Sardnyx", 281: "Digi-Sapphire",
    282: "Digi-Opal", 283: "Digi-Topaz", 284: "Digi-Turquoise",
}
_SEVENS_CARDS = {
    285: "Wild Sevens", 286: "Holy Sevens", 287: "Dark Sevens", 288: "Grand Sevens",
    289: "Mystic Sevens", 290: "Speed Sevens", 291: "Reverse Sevens",
}


def _set_card_score(bin_data, card_id, name, score):
    """Locate a card record by its unique [id_lo, id_hi, 0x00] + name prefix
    (avoids substring collisions like 'Veemon' inside 'ExVeemon') and set
    its pack-eligibility score byte at record_base + 0x19."""
    pattern = bytes([card_id & 0xFF, (card_id >> 8) & 0xFF, 0]) + name.encode()
    idx = bin_data.find(pattern)
    if idx == -1:
        print(f"    [WARNING] Could not find {name} (id {card_id}) -- score not set.")
        return False
    record_base = idx - 3
    bin_data[record_base + 0x19] = score
    return True


def _set_option_card_score(bin_data, card_id, name, score):
    """Same idea as _set_card_score, but for option-tier cards (Digi-Jewels,
    Sevens): header byte is 1 instead of 0, and the eligibility score sits
    at record_base + 0x1C instead of + 0x19."""
    pattern = bytes([card_id & 0xFF, (card_id >> 8) & 0xFF, 1]) + name.encode()
    idx = bin_data.find(pattern)
    if idx == -1:
        print(f"    [WARNING] Could not find {name} (id {card_id}) -- score not set.")
        return False
    record_base = idx - 3
    bin_data[record_base + 0x1C] = score
    return True


def apply_pack_eligibility_fixes(bin_data):
    """Set pack-eligibility scores for Armor Digimon, Partner cards,
    Digi-Jewels, and Sevens so they land in their intended packs (see
    module notes above)."""
    print("\n[*] Applying pack-eligibility fixes (Armor / Partners / Digi-Jewels / Sevens) ...")
    ok = 0
    for card_id, name in _ARMOR_CARDS.items():
        if _set_card_score(bin_data, card_id, name, _ARMOR_SCORE):
            ok += 1
    for card_id, name in _PARTNER_CARDS.items():
        if _set_card_score(bin_data, card_id, name, _PARTNER_SCORE):
            ok += 1
    for card_id, name in _DIGI_JEWEL_CARDS.items():
        if _set_option_card_score(bin_data, card_id, name, _DIGI_JEWEL_SCORE):
            ok += 1
    for card_id, name in _SEVENS_CARDS.items():
        if _set_option_card_score(bin_data, card_id, name, _SEVENS_SCORE):
            ok += 1
    total = (len(_ARMOR_CARDS) + len(_PARTNER_CARDS)
             + len(_DIGI_JEWEL_CARDS) + len(_SEVENS_CARDS))
    print(f"    {ok}/{total} cards patched "
          f"({len(_ARMOR_CARDS)} Armor @ {_ARMOR_SCORE}, "
          f"{len(_PARTNER_CARDS)} Partners @ {_PARTNER_SCORE}, "
          f"{len(_DIGI_JEWEL_CARDS)} Digi-Jewels @ {_DIGI_JEWEL_SCORE}, "
          f"{len(_SEVENS_CARDS)} Sevens @ {_SEVENS_SCORE})")


def apply_executable_fixes(bin_data):
    """Locate SLUS_013.28 and P.DRV inside the .bin and patch in the three
    Armor Digimon engine fixes described above. Modifies bin_data in place
    (bytearray). Prints a warning (does not raise) if either file can't be
    found, so a bad disc image fails loudly rather than silently shipping
    without the fixes."""
    print("\n[*] Applying engine fixes (crash / collection / deck-limit) ...")

    slus_lba = find_file_lba(bytes(bin_data), _SLUS_SIGNATURE)
    if slus_lba is None:
        print("    [WARNING] Could not locate SLUS_013.28 — engine fixes NOT applied.")
    else:
        slus = bytearray(extract_file_from_bin(bin_data, slus_lba, _SLUS_SIZE))
        for off, new_bytes in _SLUS_FIXES.items():
            slus[off:off + len(new_bytes)] = new_bytes
        write_file_into_bin(bin_data, slus_lba, bytes(slus))
        print(f"    SLUS_013.28: {len(_SLUS_FIXES)} patches applied (crash fix + collection fix)")

    pdrv_lba = find_file_lba(bytes(bin_data), _PDRV_SIGNATURE)
    if pdrv_lba is None:
        print("    [WARNING] Could not locate P.DRV — deck-limit fix NOT applied.")
    else:
        pdrv = bytearray(extract_file_from_bin(bin_data, pdrv_lba, _PDRV_SIZE))
        for off, new_bytes in _PDRV_FIXES.items():
            pdrv[off:off + len(new_bytes)] = new_bytes
        write_file_into_bin(bin_data, pdrv_lba, bytes(pdrv))
        print(f"    P.DRV: {len(_PDRV_FIXES)} patches applied (deck-limit fix)")


OUTPUT_BIN_PATH = "Digimon Digital Card Battle - Revival.bin"

# =============================================================================
# STARTER DECK RANDOMIZER  (patches B.DRV, in place inside the .bin)
# =============================================================================
#
# All three starter decks are stored as plain, unpadded 2-byte-LE card ID
# lists (30 entries each) inside B.DRV, immediately followed by their default
# deck-name string ("Red\0", "Green\0", "Yellow\0"). Confirmed by exact byte
# match against real card compositions and live-tested through the game's own
# new-game creation — since the GAME writes the resulting save itself, it
# passes its own checksum/validation correctly, unlike direct .mcr editing.
#
# Table offsets are relative to the start of B.DRV's own data (i.e. as if
# B.DRV were extracted standalone) — see BDRV_DECK_TABLES below.
# =============================================================================

BDRV_TABLE_OFFSETS = {
    'Fire':   (0x1690d0c, 'Red (Veemon)'),
    'Nature': (0x1690d7a, 'Green (Hawkmon)'),
    'Rare':   (0x1690de8, 'Yellow (Armadillomon)'),
}

_PARTNER_NAMES = {'Fire': 'Veemon', 'Nature': 'Hawkmon', 'Rare': 'Armadillomon'}
_COLOR_NAMES   = ['Fire', 'Ice', 'Nature', 'Darkness', 'Rare']


def print_intro_summary():
    print("=" * 64)
    print("  DDCB REVIVAL")
    print("=" * 64)
    print("""
I felt a lot of disappointment over the years every time I looked for a
mod of this game, but no more! I made my own. I hope that this mod
revives this game. Hope you enjoy :)
""")


def prompt_stat_mode():
    """Ask the player which of the three stat systems to use, instead of
    requiring them to edit STAT_MODE in the source directly."""
    print("\n" + "=" * 64)
    print("  STAT MODE")
    print("=" * 64)
    print("  1 = Randomizer      -- every card's stats are freshly rolled")
    print("                         within reworked (generally higher) ranges")
    print("  2 = Semi-Randomizer -- rolls within a range around a curated")
    print("                         base value for each card")
    print("  3 = Hand-Altered    -- every card uses its exact curated value,")
    print("                         no randomization at all")
    print("  4 = Untouched       -- every card keeps its exact original")
    print("                         vanilla value -- no stat changes at all\n")
    choice = _prompt("  Choice: ", valid=['1', '2', '3', '4'])
    return {"1": "randomizer", "2": "semi", "3": "hand", "4": "untouched"}[choice]


def prompt_starter_deck_choice():
    """Ask the player which partner they want to build a specific deck for,
    then whether that deck should be randomized (pick colors) or built
    around a chosen focus card. The other two partners' decks get fully
    randomized colors (see random_other_partner_colors).

    Returns (partner_elem, mode, data):
      mode == 'random' -> data = (primary_color, secondary_color)
      mode == 'custom' -> data = (focus_name, power_level, is_partner)
    """
    print("\n" + "=" * 64)
    print("  STARTER DECK SETUP")
    print("=" * 64)
    print("  Pick a partner to build a SPECIFIC deck for — the other two")
    print("  partners' decks will each get a randomized color combo.\n")
    print("  V = Veemon   H = Hawkmon   A = Armadillomon")
    partner_key = _prompt("  Partner: ", valid=['V', 'H', 'A'])
    partner_elem = _PARTNER_ELEMENTS[partner_key]

    print("\n  1 = Random deck    -- pick colors, deck is randomized within them")
    print("  2 = Build your own -- pick a focus card + power level")
    mode_choice = _prompt("  Choice (1/2): ", valid=['1', '2'])

    if mode_choice == '1':
        print("\n  1=Fire  2=Ice  3=Nature  4=Darkness  5=Rare")
        primary_key = _prompt("  Primary color: ", valid=['1', '2', '3', '4', '5'])
        primary_color = _COLOR_MENU[primary_key]

        secondary_key = _prompt("  Secondary color (optional, Enter to skip): ",
                                 valid=['1', '2', '3', '4', '5'], allow_empty=True)
        secondary_color = _COLOR_MENU.get(secondary_key) if secondary_key else None
        return partner_elem, 'random', (primary_color, secondary_color)

    focus_name, is_partner = prompt_focus_card()
    power_level = prompt_deck_power_level()
    return partner_elem, 'custom', (focus_name, power_level, is_partner)


def random_other_partner_colors(chosen_partner_elem, chosen_primary, chosen_secondary):
    """For the two partners NOT specifically configured, randomly assign
    color combos drawn WITHOUT overlap from whatever colors the chosen
    partner's deck didn't use — so no color appears in more than one deck.
    With 5 colors and 3 decks, if the chosen deck used 2 colors, only 3
    remain for the other two (one deck gets 2, the other gets 1)."""
    used = {chosen_primary}
    if chosen_secondary:
        used.add(chosen_secondary)
    remaining = [c for c in _COLOR_NAMES if c not in used]
    random.shuffle(remaining)

    configs = {}
    other_elems = [e for e in BDRV_TABLE_OFFSETS if e != chosen_partner_elem]
    for elem in other_elems:
        if not remaining:
            # Shouldn't normally happen (5 colors, max 2+2+1 needed across 3
            # decks), but guard against running out just in case.
            primary, secondary = random.choice(_COLOR_NAMES), None
        else:
            want_dual = random.random() < 0.4 and len(remaining) >= 2
            primary = remaining.pop()
            secondary = remaining.pop() if want_dual else None
        configs[elem] = (primary, secondary)
    return configs


def _prompt(prompt_text, valid=None, allow_empty=False):
    while True:
        ans = input(prompt_text).strip()
        if allow_empty and ans == "":
            return ""
        if valid is None or ans.upper() in [v.upper() for v in valid]:
            return ans.upper() if valid else ans
        print(f"    (please enter one of: {', '.join(valid)})")


SECTOR_SIZE     = 2352
SECTOR_DATA_OFF = 24
SECTOR_DATA_LEN = 2048


def find_file_lba(bin_data, needle_bytes, search_len=64):
    """Locate a file's starting LBA inside a raw 2352-byte-sector .bin by
    matching its first `search_len` bytes against each sector's 2048-byte
    data payload (properly skipping the 24-byte sync/header per sector)."""
    needle = needle_bytes[:search_len]
    num_sectors = len(bin_data) // SECTOR_SIZE
    for lba in range(num_sectors):
        sec_off = lba * SECTOR_SIZE
        chunk = bin_data[sec_off + SECTOR_DATA_OFF: sec_off + SECTOR_DATA_OFF + search_len]
        if chunk == needle:
            return lba
    return None


def extract_file_from_bin(bin_data, lba, file_size):
    """Pull a file's bytes out of the raw .bin, properly deinterleaving the
    2048-byte data payload of each 2352-byte sector starting at `lba`."""
    num_sectors = (file_size + SECTOR_DATA_LEN - 1) // SECTOR_DATA_LEN
    out = bytearray()
    for i in range(num_sectors):
        sec_off = (lba + i) * SECTOR_SIZE
        out += bin_data[sec_off + SECTOR_DATA_OFF: sec_off + SECTOR_DATA_OFF + SECTOR_DATA_LEN]
    return bytes(out[:file_size])


def write_file_into_bin(bin_data, lba, file_bytes):
    """Write a (same-size!) file's bytes back into the raw .bin at the given
    LBA, respecting sector structure — only touches each sector's 2048-byte
    data payload, never the sync/header/ECC bytes around it."""
    num_sectors = (len(file_bytes) + SECTOR_DATA_LEN - 1) // SECTOR_DATA_LEN
    for i in range(num_sectors):
        sec_off = (lba + i) * SECTOR_SIZE
        chunk = file_bytes[i * SECTOR_DATA_LEN: (i + 1) * SECTOR_DATA_LEN]
        if len(chunk) < SECTOR_DATA_LEN:
            # last partial sector — keep the original tail bytes beyond file end
            chunk = chunk + bin_data[sec_off + SECTOR_DATA_OFF + len(chunk):
                                      sec_off + SECTOR_DATA_OFF + SECTOR_DATA_LEN]
        bin_data[sec_off + SECTOR_DATA_OFF: sec_off + SECTOR_DATA_OFF + SECTOR_DATA_LEN] = chunk


def randomize_starter_decks(bin_data, bdrv_lba, bdrv_size, deck_configs, custom_deck=None):
    """Extract B.DRV from the .bin, randomize all three starter deck tables
    using the given {partner_element: (primary_color, secondary_color)}
    config, and write it back in place. Modifies bin_data (a bytearray).

    custom_deck: optional (element, deck_list) override — that element's
    slot gets `deck_list` written directly instead of a build_deck() call
    (used by the build-your-own-deck feature)."""
    bdrv = bytearray(extract_file_from_bin(bin_data, bdrv_lba, bdrv_size))
    custom_elem, custom_list = custom_deck if custom_deck else (None, None)

    print("\n[*] Altering starter decks ...")
    for partner_elem, (primary_color, secondary_color) in deck_configs.items():
        off, label = BDRV_TABLE_OFFSETS[partner_elem]
        if partner_elem == custom_elem:
            deck = custom_list
            for i in range(_NUM_SLOTS):
                cid = deck[i]
                bdrv[off + i * 2: off + i * 2 + 2] = cid.to_bytes(2, 'little')
            print(f"    {label:24s} [custom build-your-own-deck]: applied")
            continue
        deck = build_deck(partner_elem, primary_color, secondary_color)
        for i in range(_NUM_SLOTS):
            cid = deck[i]
            bdrv[off + i * 2: off + i * 2 + 2] = cid.to_bytes(2, 'little')
        color_desc = primary_color + (f"/{secondary_color}" if secondary_color else "")
        print(f"    {label:24s} [{color_desc:12s}]: randomized")

    write_file_into_bin(bin_data, bdrv_lba, bytes(bdrv))


# =============================================================================
# UNIFIED ENTRY POINT
# =============================================================================



# =============================================================================
# OPPONENT DECK STRENGTHENING
# =============================================================================
#
# 109 named opponent/NPC decks, located precisely within B.DRV via exact
# card-composition matching against the original deck list. Each gets a
# tier (1-6) based on its relative position in that list — later decks get
# progressively stronger treatment, per the source material's own difficulty
# curve. Star card (or best-guess fallback) is always protected.
#
# Explicitly excluded (never touched): Tutorial Deck, Pick Up Deck,
# Darkness Wave Deck (scripted), the 13 "given from X if Y is not partner"
# fallback decks, and the Red/Green/Yellow starters (handled separately).
# Fire Heart Deck (WarGreymon) is also left untouched. Fire Heart Deck
# (Davis) gets a small special-case Sevens injection instead of the normal
# tier engine — see apply_fire_heart_davis_sevens() below.

_OPPONENT_DECK_DATA_JSON = '''[{"name":"Tricolor Starter Deck","offset":23646326,"digimon_counts":{"20":1,"24":1,"27":4,"33":2,"55":1,"60":1,"63":3,"68":3,"90":1,"94":1,"97":3,"98":3},"star_id":27,"star_name":"Agumon","colors":["Fire","Ice","Nature"],"tier":2},{"name":"Penguinmon Color Deck","offset":23646436,"digimon_counts":{"51":1,"52":2,"56":2,"57":1,"61":2,"62":3,"64":4,"65":2,"162":2,"163":1,"169":2,"171":2},"star_id":64,"star_name":"Penguinmon","colors":["Ice","Rare"],"tier":2},{"name":"New Power Deck","offset":23646546,"digimon_counts":{"7":1,"15":1,"25":1,"28":1,"31":1,"32":1,"40":1,"48":1,"57":1,"65":3,"78":1,"83":2,"99":3},"star_id":null,"star_name":"Babamon","colors":["Fire","Ice","Nature"],"tier":2},{"name":"Burning Hot! Deck","offset":23646656,"digimon_counts":{"10":2,"18":4,"20":3,"26":3,"28":3,"29":2,"30":2,"31":3,"32":3,"33":1},"star_id":18,"star_name":"Meramon","colors":["Fire"],"tier":2},{"name":"Big Red Sky Deck","offset":23646766,"digimon_counts":{"3":4,"13":2,"20":3,"23":3,"28":4,"29":4,"30":2},"star_id":3,"star_name":"Phoenixmon","colors":["Fire"],"tier":2},{"name":"Go Go Dinosaur Deck","offset":23646876,"digimon_counts":{"8":1,"9":1,"10":1,"14":2,"16":2,"17":2,"27":2,"28":2,"29":1,"32":2,"33":1,"175":4,"172":1,"185":1,"173":1,"12":1},"star_id":175,"star_name":"Veemon","colors":["Fire"],"tier":2},{"name":"Quick Digivolve Deck","offset":23646986,"digimon_counts":{"78":2,"79":2,"80":2,"84":2,"89":2,"94":2,"95":4,"97":4,"98":4,"99":4,"102":2},"star_id":92,"star_name":"Vegiemon","colors":["Nature"],"tier":2},{"name":"Switching Deck","offset":23647096,"digimon_counts":{"83":2,"89":4,"91":2,"93":2,"97":2,"98":2,"99":2,"100":2,"101":2},"star_id":89,"star_name":"Ninjamon","colors":["Nature"],"tier":2},{"name":"V For Victory Deck","offset":23647206,"digimon_counts":{"72":2,"80":1,"81":4,"87":3,"97":3,"98":3,"99":3,"102":2},"star_id":81,"star_name":"Veedramon","colors":["Nature"],"tier":2},{"name":"Tryout Deck","offset":23647316,"digimon_counts":{"90":1,"91":1,"100":1,"102":1,"119":2,"126":2,"132":2,"136":2,"137":2,"187":4,"186":1,"177":1,"117":1},"star_id":187,"star_name":"Wormmon","colors":["Nature","Darkness"],"tier":2},{"name":"Hearty Meal Deck","offset":23647426,"digimon_counts":{"38":1,"45":1,"52":4,"55":1,"60":2,"61":2,"62":2,"64":3,"67":3},"star_id":52,"star_name":"Frigimon","colors":["Ice"],"tier":2},{"name":"Guarding Sea Deck","offset":23647536,"digimon_counts":{"40":1,"42":1,"44":1,"47":2,"48":2,"49":2,"56":1,"61":3,"63":3,"65":3,"66":3},"star_id":49,"star_name":"Whamon","colors":["Ice"],"tier":2},{"name":"Fightback Deck","offset":23647646,"digimon_counts":{"39":1,"40":2,"46":4,"59":2,"60":2,"62":3,"64":3,"66":2,"67":3},"star_id":46,"star_name":"Garurumon","colors":["Ice"],"tier":2},{"name":"Black Storm Deck","offset":23647756,"digimon_counts":{"112":2,"114":2,"117":2,"120":2,"129":2,"133":3,"135":4,"138":3},"star_id":117,"star_name":"Stingmon","colors":["Darkness"],"tier":2},{"name":"Toy Party Deck","offset":23647866,"digimon_counts":{"146":1,"148":1,"149":1,"152":2,"153":2,"159":2,"165":2,"166":4,"167":2,"168":2,"169":2},"star_id":166,"star_name":"Hagurumon","colors":["Rare"],"tier":2},{"name":"Jam-Jam Deck","offset":23647976,"digimon_counts":{"155":4,"157":3,"160":2,"168":3,"170":3,"171":3},"star_id":155,"star_name":"ShellNumemon","colors":["Rare"],"tier":2},{"name":"Hail King Sukamon Deck","offset":23648086,"digimon_counts":{"154":2,"156":1,"158":4,"165":1,"168":3,"169":4,"170":3},"star_id":null,"star_name":"KingSukamon","colors":["Rare"],"tier":2},{"name":"Evil Fire Deck","offset":23648196,"digimon_counts":{"10":1,"26":1,"31":1,"109":1,"114":2,"117":2,"130":2,"135":2,"136":2,"137":2,"187":4,"186":4},"star_id":null,"star_name":"Shadramon","colors":["Fire","Darkness"],"tier":2},{"name":"Get Serious Deck","offset":23648306,"digimon_counts":{"90":2,"100":1,"102":3,"113":1,"115":1,"119":2,"126":2,"132":2,"136":3,"137":2},"star_id":187,"star_name":"Wormmon","colors":["Nature","Darkness"],"tier":2},{"name":"Black Storm Again Deck","offset":23648416,"digimon_counts":{"112":2,"114":2,"117":4,"120":1,"129":2,"133":2,"135":4,"138":3,"187":1},"star_id":117,"star_name":"Stingmon","colors":["Darkness"],"tier":2},{"name":"Evil Fire Revived Deck","offset":23648526,"digimon_counts":{"10":1,"26":1,"31":1,"111":1,"114":1,"117":1,"130":2,"135":2,"136":1,"137":2,"187":4,"186":4},"star_id":null,"star_name":"Shadramon","colors":["Fire","Darkness"],"tier":2},{"name":"Bad Luck Wind Deck","offset":23648636,"digimon_counts":{"43":1,"50":1,"58":1,"65":1,"112":2,"114":1,"117":2,"120":2,"132":2,"136":2,"187":4,"177":4},"star_id":null,"star_name":"Quetzalmon","colors":["Ice","Darkness"],"tier":2},{"name":"Binding Chain Deck","offset":23648746,"digimon_counts":{"104":2,"109":1,"117":3,"118":2,"124":1,"132":2,"134":2,"135":2,"138":4,"187":1},"star_id":null,"star_name":"Digimon Emperor","colors":["Darkness"],"tier":2},{"name":"Gate of Fire Deck","offset":23648856,"digimon_counts":{"11":3,"17":2,"19":3,"23":2,"24":1,"27":4,"31":4,"32":2},"star_id":19,"star_name":"Centarumon","colors":["Fire"],"tier":2},{"name":"Paleo-Energy Deck","offset":23648966,"digimon_counts":{"8":3,"16":4,"17":1,"27":3,"29":2,"30":2,"80":1,"91":2,"92":2,"97":2,"101":3},"star_id":16,"star_name":"Tyrannomon","colors":["Fire","Nature"],"tier":2},{"name":"Evil-Slayer Deck","offset":23649076,"digimon_counts":{"75":1,"77":2,"82":4,"88":2,"96":2,"97":3,"98":3,"99":4},"star_id":82,"star_name":"Angemon","colors":["Nature"],"tier":2},{"name":"Ready to Go Deck","offset":23649406,"digimon_counts":{"142":2,"143":1,"151":3,"161":2,"163":2,"165":3,"166":2,"167":2,"168":2,"190":1},"star_id":null,"star_name":"Cody","colors":["Rare"],"tier":2},{"name":"Wings of Hope Deck","offset":23649516,"digimon_counts":{"75":2,"77":1,"82":3,"87":2,"88":2,"97":4,"98":1,"99":4,"183":1},"star_id":null,"star_name":"T.K.","colors":["Nature"],"tier":2},{"name":"Magic Strike Deck","offset":23649626,"digimon_counts":{"45":1,"57":2,"67":3,"115":2,"118":4,"127":1,"134":2,"135":2,"138":3},"star_id":118,"star_name":"Wizardmon","colors":["Ice","Darkness"],"tier":2},{"name":"Slayer Deck","offset":23649736,"digimon_counts":{"72":4,"81":4,"85":3,"97":3,"98":3,"99":1,"100":3},"star_id":72,"star_name":"AeroVeedramon","colors":["Nature"],"tier":2},{"name":"Cat Attack Deck","offset":23649846,"digimon_counts":{"83":1,"85":2,"91":2,"99":2,"100":3,"101":3,"184":4,"181":1,"178":1},"star_id":184,"star_name":"Gatomon","colors":["Nature"],"tier":2},{"name":"Ladies’ Night Deck","offset":23649956,"digimon_counts":{"20":1,"29":1,"73":1,"77":2,"78":1,"83":3,"84":3,"98":4,"99":4,"184":1},"star_id":null,"star_name":"Kari","colors":["Fire","Nature"],"tier":2},{"name":"Out of Control Deck","offset":23650066,"digimon_counts":{"33":3,"68":3,"101":3,"138":3,"166":3},"star_id":33,"star_name":"Goburimon","colors":["Fire","Ice","Nature","Darkness","Rare"],"tier":2},{"name":"Dark Digivolution Deck","offset":23650176,"digimon_counts":{"106":1,"111":2,"113":2,"114":1,"132":4,"133":4,"135":4,"136":4,"137":4},"star_id":132,"star_name":"DemiDevimon","colors":["Darkness"],"tier":2},{"name":"Mega Shock Deck","offset":23650286,"digimon_counts":{"112":4,"119":4,"129":4,"133":2,"134":4,"135":4},"star_id":112,"star_name":"Megadramon","colors":["Darkness"],"tier":3},{"name":"Mega Giga Deck","offset":23650396,"digimon_counts":{"5":2,"20":1,"26":3,"27":3,"28":2,"112":2,"124":3,"127":1,"134":3,"136":2},"star_id":5,"star_name":"Gigadramon","colors":["Fire","Darkness"],"tier":3},{"name":"Spiky Deck","offset":23650506,"digimon_counts":{"78":2,"84":4,"89":3,"92":1,"98":4,"100":3,"102":3},"star_id":84,"star_name":"Togemon","colors":["Nature"],"tier":3},{"name":"Anti-A Deck","offset":23650616,"digimon_counts":{"79":2,"86":4,"90":3,"94":1,"97":4,"101":3,"102":3},"star_id":86,"star_name":"Kabuterimon","colors":["Nature"],"tier":3},{"name":"Anti Fire Deck","offset":23650726,"digimon_counts":{"40":2,"47":4,"52":3,"58":1,"61":4,"64":3,"65":3,"67":1},"star_id":47,"star_name":"Ikkakumon","colors":["Ice"],"tier":3},{"name":"First Attack Deck","offset":23650836,"digimon_counts":{"7":2,"13":2,"20":4,"21":2,"29":4,"31":3,"33":3},"star_id":20,"star_name":"Birdramon","colors":["Fire"],"tier":3},{"name":"Howl to the Moon Deck","offset":23650946,"digimon_counts":{"39":4,"46":4,"59":2,"60":1,"62":3,"64":3,"66":1,"67":3},"star_id":39,"star_name":"WereGarurumon","colors":["Ice"],"tier":3},{"name":"SEVEN Deck","offset":23651056,"digimon_counts":{"6":4,"14":1,"20":1,"27":4,"29":1,"46":1,"47":1,"61":1,"62":1,"82":1,"84":1,"86":1,"97":1,"98":1,"99":1},"star_id":9,"star_name":"MetalGreymon","colors":["Fire","Ice","Nature"],"tier":3},{"name":"Fighting Monsters Deck","offset":23651166,"digimon_counts":{"108":1,"113":2,"121":4,"122":1,"126":1,"128":1,"133":3,"135":3,"138":4},"star_id":121,"star_name":"Tuskmon","colors":["Darkness"],"tier":3},{"name":"Sickle Slayer Deck","offset":23651276,"digimon_counts":{"114":4,"123":4,"127":3,"135":3,"137":4,"138":3},"star_id":114,"star_name":"Phantomon","colors":["Darkness"],"tier":3},{"name":"Mega Flood Deck","offset":23651386,"digimon_counts":{"42":4,"47":1,"48":2,"52":2,"55":2,"64":3,"65":3,"67":2,"68":3},"star_id":42,"star_name":"MegaSeadramon","colors":["Ice"],"tier":3},{"name":"Evil King Deck","offset":23651496,"digimon_counts":{"106":4,"119":3,"121":2,"123":2,"132":4,"133":3,"135":3},"star_id":106,"star_name":"VenomMyotismon","colors":["Darkness"],"tier":3},{"name":"Battle Gear Deck","offset":23651606,"digimon_counts":{"85":4,"91":2,"99":3,"100":2,"101":1,"126":3,"133":3,"138":1},"star_id":85,"star_name":"Leomon","colors":["Nature","Darkness"],"tier":3},{"name":"Cool Devil Deck","offset":23651716,"digimon_counts":{"58":4,"65":2,"68":4,"120":4,"132":4,"136":2},"star_id":null,"star_name":"","colors":["Ice","Darkness"],"tier":3},{"name":"Steel Gate Deck","offset":23651826,"digimon_counts":{"141":3,"150":2,"162":2,"163":2,"164":2,"165":3,"169":3,"170":3},"star_id":141,"star_name":"MetalEtemon","colors":["Rare"],"tier":3},{"name":"Dark Revival Deck","offset":23651936,"digimon_counts":{"111":4,"119":3,"121":2,"123":2,"132":4,"133":3,"135":3},"star_id":null,"star_name":"","colors":["Darkness"],"tier":3},{"name":"Strong-V Deck","offset":23652156,"digimon_counts":{"12":4,"14":2,"15":2,"27":4,"30":3,"31":3},"star_id":12,"star_name":"ExVeemon","colors":["Fire"],"tier":3},{"name":"Rocket Bomb Deck","offset":23652266,"digimon_counts":{"11":1,"12":1,"18":1,"25":2,"27":1,"28":2,"31":2,"32":2,"175":4,"172":4},"star_id":null,"star_name":"Flamedramon","colors":["Fire"],"tier":3},{"name":"Raiden Blade Deck","offset":23652376,"digimon_counts":{"12":1,"26":1,"29":1,"30":1,"118":2,"125":1,"134":2,"136":2,"175":4,"185":4},"star_id":null,"star_name":"Raidramon","colors":["Fire","Darkness"],"tier":3},{"name":"Quick Draw Deck","offset":23652486,"digimon_counts":{"83":2,"84":1,"87":2,"91":2,"99":2,"101":3,"102":2,"182":4,"179":1,"188":1},"star_id":182,"star_name":"Hawkmon","colors":["Nature"],"tier":3},{"name":"Storm Bringer Deck","offset":23652596,"digimon_counts":{"7":2,"13":2,"20":2,"28":1,"29":4,"72":2,"87":2,"94":2,"97":3,"100":1,"182":1},"star_id":13,"star_name":"Aquilamon","colors":["Fire","Nature"],"tier":3},{"name":"Burning Love Deck","offset":23652706,"digimon_counts":{"76":1,"81":1,"87":2,"94":2,"97":2,"99":2,"100":2,"182":4,"179":4},"star_id":null,"star_name":"Halsemon","colors":["Nature"],"tier":3},{"name":"Mountain Crusher Deck","offset":23652816,"digimon_counts":{"159":1,"165":1,"166":2,"169":2,"170":2,"190":4,"189":1,"176":1,"151":1},"star_id":190,"star_name":"Armadillomon","colors":["Rare"],"tier":3},{"name":"Rock Head Deck","offset":23652926,"digimon_counts":{"144":3,"151":4,"154":2,"163":2,"165":3,"168":2,"169":2,"170":3},"star_id":151,"star_name":"Ankylomon","colors":["Rare"],"tier":3},{"name":"Mountain Crusher DX Deck","offset":23653036,"digimon_counts":{"142":1,"159":1,"165":1,"166":1,"169":2,"170":2,"190":4,"189":4},"star_id":null,"star_name":"Digmon","colors":["Rare"],"tier":3},{"name":"Blitzkrieg Deck","offset":23653146,"digimon_counts":{"146":3,"153":4,"164":2,"166":4,"167":4,"169":2},"star_id":153,"star_name":"Thundermon","colors":["Rare"],"tier":3},{"name":"Bean Stalk Deck","offset":23653256,"digimon_counts":{"89":3,"97":2,"101":3,"146":2,"148":2,"149":2,"152":2,"153":2,"156":2,"166":3,"168":3},"star_id":148,"star_name":"MetalMamemon","colors":["Nature","Rare"],"tier":3},{"name":"Star Force Deck","offset":23653366,"digimon_counts":{"140":4,"147":1,"152":4,"161":4,"165":4,"166":3,"169":4},"star_id":140,"star_name":"SuperStarmon","colors":["Rare"],"tier":3},{"name":"Dancing Ghosts Deck","offset":23653476,"digimon_counts":{"123":4,"127":4,"133":3,"135":3,"137":4},"star_id":123,"star_name":"Bakemon","colors":["Darkness"],"tier":4},{"name":"Devil’s Call Deck","offset":23653586,"digimon_counts":{"113":2,"119":2,"120":4,"122":2,"132":4,"135":3,"138":3},"star_id":null,"star_name":"","colors":["Darkness"],"tier":4},{"name":"Stealth Skull Deck","offset":23653696,"digimon_counts":{"113":4,"120":3,"122":2,"125":2,"132":4,"135":3,"138":3},"star_id":113,"star_name":"SkullGreymon","colors":["Darkness"],"tier":4},{"name":"Dark Prince Deck","offset":23653806,"digimon_counts":{"111":4,"118":4,"120":3,"132":3,"135":4,"137":3},"star_id":null,"star_name":"","colors":["Darkness"],"tier":4},{"name":"Friendly Deck","offset":23653916,"digimon_counts":{"97":1,"98":1,"99":1,"100":1,"101":1,"102":1,"183":4,"180":1,"174":1,"82":1},"star_id":183,"star_name":"Patamon","colors":["Nature"],"tier":4},{"name":"Twin Meteor Deck","offset":23654026,"digimon_counts":{"11":1,"26":1,"28":1,"32":2,"75":2,"82":2,"99":2,"101":2,"183":4,"174":4},"star_id":null,"star_name":"Baronmon","colors":["Fire","Nature"],"tier":4},{"name":"Great Hope Deck","offset":23654136,"digimon_counts":{"70":1,"75":1,"82":2,"87":2,"88":2,"97":2,"98":1,"99":2,"183":4,"180":4},"star_id":null,"star_name":"Pegasusmon","colors":["Nature"],"tier":4},{"name":"Call of Destiny Deck","offset":23654246,"digimon_counts":{"75":2,"85":3,"91":2,"99":3,"100":3,"101":3},"star_id":184,"star_name":"Gatomon","colors":["Nature"],"tier":4},{"name":"Divine Monster Deck","offset":23654356,"digimon_counts":{"71":1,"77":1,"87":2,"88":2,"98":2,"99":2,"100":2,"184":4,"181":4},"star_id":null,"star_name":"Nefertimon","colors":["Nature"],"tier":4},{"name":"Swirling Light Deck","offset":23654466,"digimon_counts":{"38":1,"50":1,"56":1,"63":1,"66":1,"71":1,"82":2,"96":1,"99":2,"102":1,"184":4,"178":4},"star_id":null,"star_name":"Tylomon","colors":["Ice","Nature"],"tier":4},{"name":"Head-On Collision Deck","offset":23654686,"digimon_counts":{"84":1,"90":4,"91":2,"97":4,"100":3,"101":3},"star_id":90,"star_name":"Kuwagamon","colors":["Nature"],"tier":4},{"name":"Beetle Cross Deck","offset":23654796,"digimon_counts":{"74":4,"79":1,"86":2,"90":2,"94":1,"97":3,"102":3,"117":3,"134":2,"136":2},"star_id":74,"star_name":"HerculesKabuterimon","colors":["Nature","Darkness"],"tier":4},{"name":"Three Signs Deck","offset":23655126,"digimon_counts":{"4":4,"12":3,"19":2,"27":4,"30":3,"31":3},"star_id":4,"star_name":"Paildramon","colors":["Fire"],"tier":4},{"name":"Sun’s Gift Deck","offset":23655236,"digimon_counts":{"7":4,"13":3,"20":4,"27":3,"28":4,"29":4},"star_id":7,"star_name":"Garudamon","colors":["Fire"],"tier":4},{"name":"Hyper Digivolution Deck","offset":23655346,"digimon_counts":{"7":4,"20":4,"26":2,"27":3,"29":4,"30":3},"star_id":null,"star_name":"Sora","colors":["Fire"],"tier":4},{"name":"Ninja Deck","offset":23655456,"digimon_counts":{"76":1,"89":1,"98":1,"101":1,"156":2,"168":2,"169":2,"182":4,"188":4},"star_id":null,"star_name":"Shurimon","colors":["Nature","Rare"],"tier":4},{"name":"Flower Fairies Deck","offset":23655566,"digimon_counts":{"73":1,"78":4,"80":2,"83":1,"84":4,"89":2,"96":3,"97":3,"98":4,"99":2,"100":2,"101":2},"star_id":78,"star_name":"Lillymon","colors":["Nature"],"tier":4},{"name":"Princess Deck","offset":23655676,"digimon_counts":{"53":2,"66":3,"78":4,"84":3,"98":4,"122":1,"137":2,"157":1,"158":1,"165":3},"star_id":null,"star_name":"Mimi","colors":["Ice","Nature","Darkness","Rare"],"tier":4},{"name":"Yellow Submarine Deck","offset":23655786,"digimon_counts":{"34":1,"47":1,"56":1,"61":1,"63":2,"142":1,"151":2,"165":2,"190":4,"176":4},"star_id":null,"star_name":"Submarimon","colors":["Ice","Rare"],"tier":4},{"name":"Shoot Everything! Deck","offset":23655896,"digimon_counts":{"36":4,"39":1,"46":4,"58":2,"60":1,"62":4,"65":3,"68":3},"star_id":37,"star_name":"MetalGarurumon","colors":["Ice"],"tier":4},{"name":"Bonding Deck","offset":23656006,"digimon_counts":{"36":3,"46":4,"62":4,"64":2,"75":1,"82":3,"100":3,"101":1},"star_id":null,"star_name":"Matt","colors":["Ice","Nature"],"tier":4},{"name":"Armed Deck","offset":23656116,"digimon_counts":{"40":4,"47":4,"57":2,"59":1,"61":4,"68":4,"118":1,"138":2},"star_id":40,"star_name":"Zudomon","colors":["Ice","Darkness"],"tier":4},{"name":"First Aid Deck","offset":23656226,"digimon_counts":{"0":3,"38":3,"39":1,"40":2,"47":3,"48":3,"52":2,"55":2,"61":4,"63":4,"66":3},"star_id":null,"star_name":"Joe","colors":["Fire","Ice"],"tier":4},{"name":"Intercepting Traps Deck","offset":23656336,"digimon_counts":{"46":3,"79":4,"86":3,"90":3,"97":4,"101":3,"102":3,"161":3},"star_id":79,"star_name":"MegaKabuterimon","colors":["Ice","Nature","Rare"],"tier":4},{"name":"Program Deck","offset":23656446,"digimon_counts":{"79":3,"86":4,"90":3,"97":4,"101":3,"102":3},"star_id":null,"star_name":"Izzy","colors":["Nature"],"tier":4},{"name":"Divine Sword Deck","offset":23656556,"digimon_counts":{"70":1,"75":3,"82":4,"88":2,"96":1,"97":2,"98":3,"99":4,"183":1},"star_id":75,"star_name":"MagnaAngemon","colors":["Nature"],"tier":5},{"name":"Shining Goddess Deck","offset":23656666,"digimon_counts":{"77":4,"87":4,"88":2,"98":2,"99":4,"100":3,"184":1},"star_id":77,"star_name":"Angewomon","colors":["Nature"],"tier":5},{"name":"Wormhole Deck","offset":23656886,"digimon_counts":{"104":3,"117":3,"118":2,"124":1,"132":2,"134":1,"135":2,"138":4,"187":1},"star_id":null,"star_name":"Ken","colors":["Darkness"],"tier":5},{"name":"Rough Sea King Deck","offset":23656996,"digimon_counts":{"36":3,"42":1,"43":1,"50":3,"51":2,"54":2,"63":3,"65":4,"66":3},"star_id":36,"star_name":"MetalSeadramon","colors":["Ice"],"tier":5},{"name":"Toy Castle Deck","offset":23657106,"digimon_counts":{"139":4,"147":1,"159":4,"163":3,"165":2,"166":2,"167":4,"168":3},"star_id":139,"star_name":"Puppetmon","colors":["Rare"],"tier":5},{"name":"Machine Empire Deck","offset":23657216,"digimon_counts":{"108":4,"116":1,"124":4,"134":4,"159":3,"165":3,"166":3},"star_id":108,"star_name":"Machinedramon","colors":["Darkness","Rare"],"tier":5},{"name":"Evil Flower Deck","offset":23657326,"digimon_counts":{"110":3,"119":3,"120":3,"132":4,"135":3,"137":4},"star_id":110,"star_name":"LadyDevimon","colors":["Darkness"],"tier":5},{"name":"Strong Monsters Deck","offset":23657436,"digimon_counts":{"36":1,"50":2,"65":3,"107":1,"108":1,"124":2,"125":2,"139":1,"159":2,"166":4,"167":3},"star_id":107,"star_name":"Piedmon","colors":["Ice","Darkness","Rare"],"tier":5},{"name":"Miracle Knight’s Deck","offset":23657546,"digimon_counts":{"4":2,"12":2,"17":1,"23":2,"27":2,"29":2,"31":2,"175":4,"173":4},"star_id":null,"star_name":"Magnamon","colors":["Fire"],"tier":5},{"name":"Storm Tamer Deck","offset":23657656,"digimon_counts":{"76":4,"81":2,"87":3,"89":2,"97":4,"98":3,"101":2,"182":1},"star_id":76,"star_name":"Sylphymon","colors":["Nature"],"tier":5},{"name":"Ancient Legend Deck","offset":23657766,"digimon_counts":{"142":3,"143":1,"151":3,"159":2,"163":2,"165":4,"169":3,"170":3},"star_id":142,"star_name":"Shakkoumon","colors":["Rare"],"tier":5},{"name":"Heaven’s Gate Deck","offset":23657876,"digimon_counts":{"70":3,"75":1,"82":4,"88":2,"96":1,"97":2,"98":3,"99":4,"183":1},"star_id":70,"star_name":"Seraphimon","colors":["Nature"],"tier":5},{"name":"Divine Dragon Deck","offset":23657986,"digimon_counts":{"71":4,"87":4,"88":2,"98":2,"99":4,"100":3,"184":1},"star_id":71,"star_name":"Magnadramon","colors":["Nature"],"tier":5},{"name":"Forever Increase Deck","offset":23658096,"digimon_counts":{"109":4,"123":2,"127":4,"134":4,"137":4,"138":4,"154":4},"star_id":109,"star_name":"Infermon","colors":["Darkness","Rare"],"tier":5},{"name":"Time Bomb Deck","offset":23658206,"digimon_counts":{"105":4,"124":3,"125":3,"133":2,"134":4,"137":4},"star_id":105,"star_name":"Diaboromon","colors":["Darkness"],"tier":5},{"name":"Invincible Emperor Deck","offset":23658316,"digimon_counts":{"0":3,"12":4,"27":2,"29":2,"36":1,"50":2,"61":2,"62":1,"71":1,"87":2,"97":1,"98":1,"99":1,"175":1},"star_id":0,"star_name":"Imperialdramon","colors":["Fire","Ice","Nature"],"tier":6},{"name":"Warrior Princess Deck","offset":23658426,"digimon_counts":{"69":4,"81":2,"87":3,"89":2,"97":4,"98":3,"101":3,"182":1},"star_id":69,"star_name":"Valkyrimon","colors":["Nature"],"tier":6},{"name":"Permafrost Deck","offset":23658536,"digimon_counts":{"34":3,"47":2,"55":2,"61":3,"63":3,"142":1,"151":2,"165":3,"190":1},"star_id":34,"star_name":"Vikemon","colors":["Ice","Rare"],"tier":6},{"name":"Black Fire Heart Deck","offset":23658866,"digimon_counts":{"2":4,"5":1,"14":4,"15":2,"24":1,"27":4,"30":4,"31":2},"star_id":null,"star_name":"BK WarGreymon","colors":["Fire"],"tier":6},{"name":"Patriot Deck","offset":23658976,"digimon_counts":{"36":3,"43":2,"46":4,"57":3,"62":4,"65":3,"68":3},"star_id":null,"star_name":"BK MetalGarurumon","colors":["Ice"],"tier":6},{"name":"Rose Garden Deck","offset":23659196,"digimon_counts":{"22":1,"28":2,"73":3,"84":2,"92":2,"98":4,"101":3,"131":2,"137":3},"star_id":73,"star_name":"Rosemon","colors":["Fire","Nature","Darkness"],"tier":6},{"name":"Return Deck","offset":23659416,"digimon_counts":{"80":4,"86":2,"90":2,"92":3,"97":2,"99":4,"102":4},"star_id":80,"star_name":"Piximon","colors":["Nature"],"tier":4},{"name":"Blue Star Red Moon Deck","offset":23658646,"offsets_all":[23658646],"digimon_counts":{"1":2,"14":4,"27":4,"30":1,"35":2,"46":4,"62":4,"64":1},"star_id":1,"star_name":"Omnimon I","colors":["Fire","Ice"],"tier":5},{"name":"Desperate Space Deck","offset":23658756,"offsets_all":[23658756,23659086,23659526,23659636,23659746,23659856,23659966,23660076,23660186],"digimon_counts":{"103":3,"105":1,"106":1,"119":2,"121":2,"124":2,"132":3,"133":3,"134":3,"135":1},"star_id":103,"star_name":"Apokarimon","colors":["Darkness"],"tier":5},{"name":"Who Are You? Deck","offset":23659306,"offsets_all":[23659306,23660296,23660406,23660516,23660626],"digimon_counts":{"144":2,"145":1,"155":2,"156":3,"161":2,"165":3,"169":3,"171":4},"star_id":156,"star_name":"Nanimon","colors":["Rare"],"tier":5}]'''

_MAX_CARD_COPIES = 4  # hard cap, applies to every card except the star (always exactly 4)

# Display names for every confirmed option card ID (191-300), sourced from
# the Digimon Fandom wiki card list and cross-verified against two IDs (193
# "Whistle", 230 "Mega Hand") independently confirmed via live ROM name-string
# search — both matched exactly, giving good confidence in the full list.
_OPTION_CARD_NAMES = {
    191: 'Golden Banana', 192: "Devil's Chip", 193: 'Whistle', 194: 'Giga Hand',
    195: 'Metallic Banana', 196: 'Shining Mane', 197: 'Mega Rec. Floppy',
    198: 'Mega Attack Chip', 199: "Dark Lord's Cape", 200: 'Fake Sevens',
    201: 'Net Worm', 202: 'Missile Pod', 203: "Shogun's Order",
    204: 'Beetle Diamond', 205: 'Dark Bone', 206: 'Red Digivice',
    207: 'Blue Digivice', 208: 'Green Digivice', 209: 'Black Digivice',
    210: 'Yellow Digivice', 211: 'Pink Digivice', 212: 'Another Dimension',
    213: 'UnInstall', 214: 'Evil Program', 215: 'Coliseum', 216: 'Fire Altar',
    217: 'Ice Altar', 218: 'Nature Altar', 219: 'Darkness Altar',
    220: 'Rare Altar', 221: 'Sup. Rec. Floppy', 222: 'Mega Def. Disk O',
    223: 'Mega Def. Disk Tri', 224: 'Mega Def. Disk X', 225: 'Heap of Junk',
    226: 'Beam Gun', 227: 'Chain Saw', 228: 'Metal Parts', 229: 'Metal Armor',
    230: 'Mega Hand', 231: 'Level Balancer', 232: 'Level Manager',
    233: 'Level Booster', 234: 'Armor Clash', 235: 'Silver Ball',
    236: 'Coral Charm', 237: 'Patch of Love', 238: 'Mystery Egg',
    239: 'Miracle Ruby', 240: 'Cyber Parts', 241: 'Liquid Crystal',
    242: 'Deluxe Mushroom', 243: 'Lucky Mushroom', 244: 'Premium Steak',
    245: 'Short Lance', 246: 'Med. Rec. Floppy', 247: 'Digimon Analyzer',
    248: 'Training Manual', 249: 'Circle Hitter', 250: 'Triangle Hitter',
    251: 'Cross Hitter', 252: "Suka's Curse", 253: "Cherrymon's Mist",
    254: 'Hacking', 255: 'Digimon Grave', 256: 'Data Copy',
    257: 'Partner Finder', 258: 'Fire Spot', 259: 'Ice Crystal',
    260: 'Earth Charm', 261: 'Black Gear', 262: 'Stuffed Animal',
    263: 'Disrupt Ray', 264: 'Attack Chip', 265: 'High Speed Disk',
    266: 'Recovery Floppy', 267: 'Attack Disk O', 268: 'Attack Disk Tri',
    269: 'Attack Disk X', 270: 'Defense Disk O', 271: 'Defense Disk Tri',
    272: 'Defense Disk X', 273: 'Digi-Garnet', 274: 'Digi-Amethyst',
    275: 'Digi-Aquamarine', 276: 'Digi-Diamond', 277: 'Digi-Emerald',
    278: 'Digi-Pearl', 279: 'Digi-Ruby', 280: 'Digi-Sardnyx',
    281: 'Digi-Sapphire', 282: 'Digi-Opal', 283: 'Digi-Topaz',
    284: 'Digi-Turquoise', 285: 'Wild Sevens', 286: 'Holy Sevens',
    287: 'Dark Sevens', 288: 'Grand Sevens', 289: 'Mystic Sevens',
    290: 'Speed Sevens', 291: 'Reverse Sevens', 292: "Rosemon's Lure",
    293: 'Download Digivolve', 294: 'ArmorCrush Digivolve',
    295: 'Special Digivolve', 296: 'Mutant Digivolve', 297: 'Warp Digivolve',
    298: 'De-Armor Digivolve', 299: 'Speed Digivolve', 300: 'Digi-devolve',
}

# Full 5-tier option card system (94 confirmed cards total).
#
# NOTE: id 8 in tier 2 is NOT a typo in this list — it also shows up in real
# opponent deck data occupying an option-array slot (e.g. "Anti Fire Deck"
# and "Evil Fire Revived Deck" both place 8 directly amongst other option
# IDs like 231/222/243/244/267, not amongst monster IDs). Card 8 is *also*
# the monster ID for MasterTyrannomon (Fire Ultimate) elsewhere in
# CARD_DATABASE. Unconfirmed whether this is: (a) a genuine dev-side reuse
# of the same numeric ID across both namespaces, disambiguated by some other
# byte/context we haven't found yet, or (b) an actual bug/quirk in the
# original game carried faithfully into this tier list. Needs a targeted
# live test: grant/select option-tier-2 in-game repeatedly until id 8 comes
# up, then check what actually gets applied — id 8 has no entry in
# _OPTION_CARD_NAMES (191-300 covers all named options), so if 8 is ever
# genuinely selected as an option it may just silently resolve to
# MasterTyrannomon's monster stat block instead of an option effect, which
# would be worth confirming before this tier list is trusted for anything
# that actually executes id 8's effect in a real deck.
# Complete draw pools for every named pack, sourced from a cross-referenced
# card-list document and validated against 23 live RAM-dump/register samples
# collected via CPU-debugger breakpoints (23/23 matched exactly -- see chat
# history for the full session log). Confirms/upgrades several pools that
# were previously only "inferred" (e.g. Blue Pack) to fully "confirmed".
#
# Convention in the source document: a "+" prefix on a card marks the leading
# block of top-tier Ultimates that are shown for context but are NOT actually
# part of that pack's draw pool. This was independently confirmed 9/9 times
# against live pulls for every shop pack and S-pack, so the pools below
# already have those "+" boundary cards excluded.
#
# CAVEATS (see chat notes for full reasoning, not yet 100% resolved):
#   - Hyper Pack's Fire section skips ids 12,13 (ExVeemon, Aquilamon) in the
#     source doc -- the only non-contiguous gap across all 5 element blocks
#     in an otherwise perfectly reliable document. Encoded as-given.
#   - Option Pack / S-Option Pack: the "+" marks in the source doc do NOT
#     follow the same leading-exclusion pattern confirmed for monster packs.
#     No live pull of either pack exists yet to confirm what "+" means here,
#     so these two pools are encoded as the FULL listed range (both "+" and
#     unmarked entries included) pending confirmation.
MONSTER_PACK_POOLS = {
    'Red':      list(range(12, 34)),
    'S-Red':    list(range(5, 27)),
    'Blue':     list(range(46, 69)),
    'S-Blue':   list(range(40, 61)),
    'Green':    list(range(81, 103)),
    'S-Green':  list(range(77, 97)),
    'Black':    list(range(117, 139)),
    'S-Black':  list(range(110, 132)),
    'Yellow':   list(range(151, 172)),
    'S-Yellow': list(range(145, 165)),
}

# Basic Pack: rolled fresh at duel start (NOT the shop RNG path). Union of
# all 5 colors' narrower ranges (Champion tail + full Rookie tier only --
# smaller than the shop pack pool for the same color). NOT color-restricted
# per pull -- an early 2-sample guess suggested single-color draws, but that
# was coincidence; the actual pool spans all 5 colors like Hyper/Super/Great.
BASIC_PACK_POOL = (
    list(range(23, 34)) + list(range(57, 69)) + list(range(93, 103)) +
    list(range(128, 139)) + list(range(161, 172))
)

# Hyper Pack: rolled fresh at duel start. Union of all 5 colors, touching
# further into each color's Ultimate tier than Basic Pack does. See caveat
# above re: the Fire-section gap at ids 12,13.
HYPER_PACK_POOL = (
    [10, 11] + list(range(14, 34)) +          # Fire (skips 12, 13 - unconfirmed anomaly)
    list(range(44, 69)) +                      # Ice
    list(range(79, 103)) +                     # Nature
    list(range(115, 139)) +                    # Darkness
    list(range(149, 172))                      # Rare
)

# Super Pack: rolled fresh at duel start. Union of all 5 colors' Ultimate-
# inclusive ranges, plus a slice of option cards starting at id 231 (the
# "stronger half" of the option-tier system, per _OPTION_TIERS).
SUPER_PACK_POOL = (
    list(range(6, 27)) + list(range(40, 61)) + list(range(75, 97)) +
    list(range(111, 132)) + list(range(145, 165)) +
    [231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244,
     245, 246, 247, 248, 249, 250, 251, 252, 255, 256, 257, 258, 259, 260,
     261, 262, 263, 264, 266, 267, 268, 269, 270, 271, 272, 300]
)

# Great Pack: rolled fresh at duel start (confirmed via grant-function
# breakpoint, a completely separate mechanism from the shop-pack RNG). Union
# of all 5 colors' Ultimate-inclusive ranges (wider than Super Pack), plus a
# broad option-card range covering most of the option-tier system.
GREAT_PACK_POOL = (
    list(range(2, 20)) + list(range(37, 53)) + list(range(74, 88)) +
    list(range(107, 124)) + list(range(142, 158)) +
    [191, 192, 193, 194, 195, 196, 197, 198, 199, 201, 202, 203, 204, 205,
     206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219,
     220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233,
     234, 235, 236, 237, 238, 239, 240, 241, 253, 254, 265, 294, 295, 296,
     297, 298, 299]
)

# Option Pack / S-Option Pack: pure option-card pools, no monsters. See
# caveat above -- "+" meaning unconfirmed for these two, so both are encoded
# as the full listed range.
OPTION_PACK_POOL = [
    215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228,
    229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242,
    243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 255, 256, 257, 258,
    259, 260, 261, 262, 263, 264, 266, 267, 268, 269, 270, 271, 272, 295,
    296, 297, 298, 299, 300
]

S_OPTION_PACK_POOL = [
    191, 192, 193, 194, 195, 196, 197, 198, 199, 201, 202, 203, 204, 205,
    206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219,
    220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233,
    234, 235, 236, 237, 238, 239, 240, 241, 253, 254, 265, 294, 295, 296,
    297, 298, 299
]

_OPTION_TIERS = {
    1: [270, 271, 272, 249, 250, 251, 300, 298, 263, 262, 261, 260, 259, 258,
        257, 247, 240, 239, 236, 238, 237, 234, 225, 216, 217, 218, 219, 220],
    2: [295, 299, 296, 297, 264, 266, 267, 268, 269, 227, 226, 198, 197, 244,
        246, 242, 243, 8, 233, 231],
    3: [265, 256, 255, 254, 252, 248, 245, 235, 230, 222, 223, 224, 221, 215,
        214, 212, 202, 201, 194],
    4: [253, 229, 228, 208, 206, 211, 210, 209, 205, 204, 203, 213, 199, 196,
        195, 193, 192, 191],
    5: [285, 286, 287, 288, 289, 290, 291, 293, 292],
}

# For each deck tier (2-6), the weight given to picking an option from each
# option tier (1-5). Centers on option-tier = deck-tier - 1.
_DECK_TIER_OPTION_WEIGHTS = {
    2: {1: 0.75, 2: 0.20, 3: 0.05, 4: 0.00, 5: 0.00},
    3: {1: 0.15, 2: 0.55, 3: 0.25, 4: 0.05, 5: 0.00},
    4: {1: 0.05, 2: 0.15, 3: 0.55, 4: 0.20, 5: 0.05},
    5: {1: 0.00, 2: 0.05, 3: 0.20, 4: 0.55, 5: 0.20},
    6: {1: 0.00, 2: 0.00, 3: 0.10, 4: 0.30, 5: 0.60},
}

_OPPONENT_TIER_PARAMS = {
    2: dict(swap_chance=0.25, max_rank_jump=2,   allow_ultimate_add=False, options=(7, 9)),
    3: dict(swap_chance=0.45, max_rank_jump=4,   allow_ultimate_add=False, options=(8, 10)),
    4: dict(swap_chance=0.60, max_rank_jump=999, allow_ultimate_add=True,  options=(8, 11)),
    5: dict(swap_chance=0.75, max_rank_jump=999, allow_ultimate_add=True,  options=(9, 11)),
    6: dict(swap_chance=0.90, max_rank_jump=999, allow_ultimate_add=True,  options=(10, 11)),
}

_SUPPLEMENTARY_CARDS = {
    175: {'name': 'Veemon', 'element': 'Fire', 'stage': 'RP'},
    182: {'name': 'Hawkmon', 'element': 'Nature', 'stage': 'RP'},
    190: {'name': 'Armadillomon', 'element': 'Rare', 'stage': 'RP'},
    187: {'name': 'Wormmon', 'element': 'Darkness', 'stage': 'RP'},
    184: {'name': 'Gatomon', 'element': 'Nature', 'stage': 'RP'},
    183: {'name': 'Patamon', 'element': 'Nature', 'stage': 'RP'},
}


def build_full_card_lookup(CARD_DATABASE):
    lookup = {c['card_id']: c for c in CARD_DATABASE if c.get('card_id') is not None}
    lookup.update(_SUPPLEMENTARY_CARDS)
    return lookup


def card_rank_info(card_id, full_lookup, pools, rank_sorted_unique_fn):
    c = full_lookup.get(card_id)
    if not c:
        return None
    elem, stage = c.get('element'), c.get('stage')
    if elem not in ('Fire', 'Ice', 'Nature', 'Darkness', 'Rare'):
        return None
    ranked = rank_sorted_unique_fn(pools.get(elem, {}).get(stage, []))
    for rank, order, cid in ranked:
        if cid == card_id:
            return elem, stage, rank, len(ranked)
    return None


def _pick_option(tier, colors=None):
    weights = _DECK_TIER_OPTION_WEIGHTS[tier]
    option_tiers = list(weights.keys())
    w = [weights[t] for t in option_tiers]
    chosen_tier = random.choices(option_tiers, weights=w, k=1)[0]
    pool = _OPTION_TIERS[chosen_tier]
    if colors:
        filtered = filter_digivices_for_colors(pool, colors)
        if filtered:
            pool = filtered
    return random.choice(pool)


def strengthen_opponent_deck(digimon_counts, star_id, colors, tier, full_lookup, pools, rank_sorted_unique_fn):
    params = _OPPONENT_TIER_PARAMS[tier]
    counts = dict(digimon_counts)
    original_total = sum(counts.values())
    original_options_count = 30 - original_total

    protect_id = star_id if star_id in counts else None
    if protect_id is None:
        _STAGE_PRIORITY = {'U': 2, 'C': 1, 'R': 0, 'RP': -1}
        best_score = None
        for cid in counts:
            info = card_rank_info(cid, full_lookup, pools, rank_sorted_unique_fn)
            if info:
                elem, stage, rank, total = info
                score = (_STAGE_PRIORITY.get(stage, -2), -rank)
                if best_score is None or score > best_score:
                    best_score, protect_id = score, cid
    if protect_id is None:
        protect_id = next(iter(counts))

    new_counts = {protect_id: 4}
    for cid, cnt in counts.items():
        if cid == protect_id:
            continue
        info = card_rank_info(cid, full_lookup, pools, rank_sorted_unique_fn)
        if info is None or random.random() > params['swap_chance']:
            new_counts[cid] = new_counts.get(cid, 0) + cnt
            continue
        elem, stage, rank, total = info
        min_rank = max(1, rank - params['max_rank_jump'])
        ranked = rank_sorted_unique_fn(pools.get(elem, {}).get(stage, []))
        candidates = [c for r, o, c in ranked if min_rank <= r < rank and c != protect_id]
        if not candidates:
            new_counts[cid] = new_counts.get(cid, 0) + cnt
            continue
        new_cid = random.choice(candidates)
        new_counts[new_cid] = new_counts.get(new_cid, 0) + cnt

    if params['allow_ultimate_add'] and colors:
        elem = colors[0]
        ranked = rank_sorted_unique_fn(pools.get(elem, {}).get('U', []))
        if ranked:
            if tier == 4:
                pick_rank = max(1, len(ranked) // 2)
            elif tier == 6:
                pick_rank = 1
            else:
                pick_rank = max(1, len(ranked) // 4)
            cand = [c for r, o, c in ranked if r == pick_rank and c != protect_id]
            if cand:
                new_counts[cand[0]] = new_counts.get(cand[0], 0) + 1

    for cid in list(new_counts.keys()):
        if cid != protect_id and new_counts[cid] > _MAX_CARD_COPIES:
            new_counts[cid] = _MAX_CARD_COPIES

    digimon_total = sum(new_counts.values())

    lo, hi = params['options']
    effective_hi = max(hi, original_options_count)
    target_options = 30 - digimon_total

    while target_options < lo and digimon_total > 1:
        largest_cid = max((c for c in new_counts if c != protect_id),
                           key=lambda c: new_counts[c], default=None)
        if largest_cid is None or new_counts[largest_cid] <= 1:
            break
        new_counts[largest_cid] -= 1
        digimon_total -= 1
        target_options += 1
    while target_options > effective_hi:
        candidates = [c for c in new_counts if c != protect_id and new_counts[c] < _MAX_CARD_COPIES]
        if not candidates:
            break
        bump_cid = min(candidates, key=lambda c: new_counts[c])
        new_counts[bump_cid] += 1
        digimon_total += 1
        target_options -= 1
    n_options = max(lo, min(effective_hi, 30 - digimon_total))

    options = [_pick_option(tier, colors) for _ in range(n_options)]

    total = sum(new_counts.values()) + len(options)
    while total < 30:
        options.append(_pick_option(tier, colors))
        total += 1
    while total > 30 and options:
        options.pop()
        total -= 1

    return new_counts, options, protect_id
_DAVIS_FIRE_HEART_OFFSET = 0x168dba2
_DAVIS_FIRE_HEART_DIGIMON_COUNT = 21


def apply_fire_heart_davis_sevens(bdrv):
    """Fire Heart Deck (Davis): keep the deck exactly as-is, just splice 2
    Sevens cards into the existing option slots (leaving the rest of the
    original option bytes untouched, since we don't have confirmed IDs for
    all of Davis's original options like 'Mega Attack Chip')."""
    off = _DAVIS_FIRE_HEART_OFFSET + _DAVIS_FIRE_HEART_DIGIMON_COUNT * 2
    chosen = random.sample(_OPTION_TIERS[5][:7], 2)  # 2 of the 7 actual Sevens cards
    for i, cid in enumerate(chosen):
        bdrv[off + i*2 : off + i*2 + 2] = cid.to_bytes(2, 'little')


_HANDMADE_OPPONENT_DECKS_JSON = '''[{"name":"Tricolor Starter Deck","ids":[27,27,27,27,14,14,14,14,6,6,6,6,63,63,68,68,62,62,62,62,46,46,39,264,295,295,239,266,226,217],"offset":23646326},{"name":"Penguinmon Color Deck","ids":[64,64,64,64,49,49,49,49,44,44,44,44,59,43,52,55,62,65,162,169,171,68,68,225,296,295,270,259,268,217],"offset":23646436},{"name":"New Power Deck","ids":[40,7,13,23,28,31,32,48,56,63,63,63,78,99,99,99,60,60,270,270,226,226,225,225,225,264,266,266,239,251],"offset":23646546},{"name":"Burning Hot! Deck","ids":[31,31,31,31,18,18,18,18,11,11,11,11,8,8,32,32,32,32,30,30,30,23,217,217,217,264,264,258,216,251],"offset":23646656},{"name":"Big Red Sky Deck","ids":[29,29,29,29,20,20,20,20,7,7,7,7,3,3,3,3,28,28,30,30,18,18,222,240,233,269,258,242,216,250],"offset":23646766},{"name":"Go Go Dinosaur Deck","ids":[12,12,12,12,4,4,4,4,175,175,175,175,8,9,10,15,17,27,28,29,32,33,19,249,299,299,266,266,234,250],"offset":23646876},{"name":"Quick Digivolve Deck","ids":[101,101,101,101,92,92,92,92,78,79,80,84,88,94,95,97,97,98,98,99,99,102,102,204,266,266,224,251,247,271],"offset":23646986},{"name":"Switching Deck","ids":[102,102,102,102,89,89,89,89,91,93,97,98,99,99,100,100,101,101,94,94,204,204,204,204,197,245,233,212,250,247],"offset":23647096},{"name":"V For Victory Deck","ids":[81,81,81,81,72,72,72,72,80,80,87,97,97,97,98,98,98,101,101,96,96,242,271,267,246,243,264,264,264,240],"offset":23647206},{"name":"Tryout Deck","ids":[117,117,117,117,104,104,104,104,187,187,187,90,91,100,102,119,126,132,132,136,136,137,137,209,209,295,295,249,221,261],"offset":23647316},{"name":"Hearty Meal Deck","ids":[67,67,67,67,52,52,52,52,40,40,40,40,44,45,55,61,62,65,50,266,266,244,244,247,247,247,197,299,221,221],"offset":23647426},{"name":"Guarding Sea Deck","ids":[64,64,64,64,49,49,49,49,44,44,44,44,42,56,61,63,65,65,66,66,53,53,221,221,221,221,221,234,259,272],"offset":23647536},{"name":"Fightback Deck","ids":[62,62,62,62,46,46,46,46,39,39,39,39,60,61,61,64,64,66,66,51,51,299,299,231,231,197,197,261,246,247],"offset":23647646},{"name":"Black Storm Deck","ids":[117,117,117,117,104,104,104,104,110,110,114,114,137,137,136,136,138,138,126,126,128,128,272,244,197,261,261,209,209,209],"offset":23647756},{"name":"Toy Party Deck","ids":[166,166,166,166,152,152,152,152,139,139,139,139,146,147,149,153,159,167,168,171,163,205,300,300,234,262,247,198,238,211],"offset":23647866},{"name":"Jam-Jam Deck","ids":[169,169,169,169,155,155,155,155,144,144,144,144,157,168,170,171,162,152,300,300,300,198,198,269,269,272,240,239,238,211],"offset":23647976},{"name":"Hail King Sukamon Deck","ids":[154,154,154,154,156,156,165,168,168,168,169,169,169,169,170,170,170,159,159,212,212,212,212,212,300,300,300,300,265,262],"offset":23648086},{"name":"Evil Fire Deck","ids":[187,187,187,187,187,187,187,187,109,9,31,114,117,133,136,137,21,21,26,26,122,122,295,295,295,299,299,299,299,201],"offset":23648196},{"name":"Get Serious Deck","ids":[117,117,117,117,104,104,104,104,113,100,102,78,119,120,132,132,136,136,137,137,123,123,296,247,221,192,218,218,218,218],"offset":23648306},{"name":"Black Storm Again Deck","ids":[117,117,117,117,104,104,104,104,111,111,132,132,133,133,138,138,187,187,187,124,124,204,204,192,192,192,193,193,234,240],"offset":23648416},{"name":"Evil Fire Revived Deck","ids":[187,187,187,187,187,187,187,187,111,8,31,31,114,117,120,120,135,135,136,137,137,16,16,247,299,226,192,192,192,192],"offset":23648526},{"name":"Bad Luck Wind Deck","ids":[187,187,187,187,187,187,187,187,43,43,50,50,56,56,63,63,65,65,65,112,117,117,54,54,246,246,246,297,297,240],"offset":23648636},{"name":"Binding Chain Deck","ids":[104,104,104,104,117,117,117,130,130,130,130,134,135,135,135,135,187,187,187,187,287,287,287,239,286,286,209,209,209,209],"offset":23648746},{"name":"Gate of Fire Deck","ids":[28,28,28,28,19,19,19,19,9,9,9,9,10,23,27,27,30,30,32,32,24,24,215,215,215,215,264,265,242,240],"offset":23648856},{"name":"Paleo-Energy Deck","ids":[28,28,28,28,16,16,16,16,8,8,8,8,7,17,27,29,79,89,92,97,97,101,101,258,218,218,218,218,299,299],"offset":23648966},{"name":"Evil-Slayer Deck","ids":[82,82,82,82,75,75,75,75,88,88,96,96,97,97,183,183,183,99,99,99,99,204,204,244,244,219,219,299,247,219],"offset":23649076},{"name":"Ready to Go Deck","ids":[142,142,142,142,143,151,151,162,162,165,165,165,166,166,168,168,190,190,190,190,153,153,289,213,213,210,210,210,210,262],"offset":23649406},{"name":"Wings of Hope Deck","ids":[75,75,75,75,77,82,82,82,82,87,87,97,97,97,99,99,99,99,183,183,183,183,286,286,286,286,265,265,265,265],"offset":23649516},{"name":"Magic Strike Deck","ids":[133,133,133,133,118,118,118,118,110,110,110,110,45,55,67,115,127,132,135,138,246,246,246,246,266,292,258,240,201,265],"offset":23649626},{"name":"Slayer Deck","ids":[81,81,81,81,72,72,72,72,85,85,85,97,97,97,98,98,98,99,100,100,100,221,221,291,291,288,288,208,208,208],"offset":23649736},{"name":"Cat Attack Deck","ids":[99,99,99,99,83,83,83,83,77,77,77,77,184,184,184,85,91,183,183,212,212,257,257,225,225,265,265,195,195,205],"offset":23649846},{"name":"Ladies’ Night Deck","ids":[73,73,73,73,78,83,83,83,83,84,84,98,98,98,98,99,99,99,99,184,184,293,293,293,288,291,292,292,292,292],"offset":23649956},{"name":"Out of Control Deck","ids":[33,33,33,33,17,17,17,17,10,10,10,10,101,138,165,167,258,258,243,243,242,242,286,211,211,204,204,204,247,244],"offset":23650066},{"name":"Dark Digivolution Deck","ids":[132,132,132,132,120,120,120,120,111,111,111,111,106,106,133,133,135,135,187,187,187,198,198,291,291,293,293,293,297,297],"offset":23650176},{"name":"Mega Shock Deck","ids":[134,134,134,134,125,125,125,125,112,112,112,112,118,118,129,129,129,133,133,132,132,132,243,230,230,287,234,197,221,268],"offset":23650286},{"name":"Mega Giga Deck","ids":[32,32,32,32,23,23,23,23,5,5,5,5,20,26,27,112,121,125,133,133,136,136,222,222,266,266,299,290,293,268],"offset":23650396},{"name":"Spiky Deck","ids":[98,98,98,98,84,84,84,84,78,78,78,78,77,85,85,92,99,99,101,101,299,253,253,246,227,213,246,221,197,269],"offset":23650506},{"name":"Anti-A Deck","ids":[97,97,97,97,86,86,86,86,79,79,79,79,74,87,87,101,101,102,102,102,214,194,240,265,224,224,299,299,299,227],"offset":23650616},{"name":"Anti Fire Deck","ids":[61,61,61,61,47,47,47,47,40,40,40,40,52,52,58,62,62,65,65,65,67,8,216,216,216,231,222,243,244,267],"offset":23650726},{"name":"First Attack Deck","ids":[29,29,29,29,20,20,20,20,7,7,7,7,13,13,21,30,30,33,33,33,290,223,202,266,199,203,204,215,266,267],"offset":23650836},{"name":"Howl to the Moon Deck","ids":[62,62,62,62,46,46,46,46,39,39,39,39,37,37,37,37,58,64,64,66,244,244,244,244,297,231,264,299,266,291],"offset":23650946},{"name":"SEVEN Deck","ids":[32,32,32,32,25,25,25,25,9,9,9,9,6,14,27,39,46,62,62,293,293,293,293,299,299,265,295,295,295,295],"offset":23651056},{"name":"Fighting Monsters Deck","ids":[135,135,135,135,121,121,121,121,116,116,116,116,108,109,122,128,132,132,133,133,212,227,244,266,194,299,296,255,233,222],"offset":23651166},{"name":"Sickle Slayer Deck","ids":[123,123,123,123,114,114,114,114,127,127,127,135,135,135,134,134,134,134,291,291,291,198,198,204,226,266,221,265,266,288],"offset":23651276},{"name":"Mega Flood Deck","ids":[63,63,63,63,50,50,50,50,42,42,42,42,36,36,36,36,49,53,64,65,66,286,226,297,299,243,243,259,259,259],"offset":23651386},{"name":"Evil King Deck","ids":[132,132,132,132,120,120,120,120,111,111,111,111,106,106,106,106,119,117,134,134,297,297,297,244,248,299,222,235,293,218],"offset":23651496},{"name":"Battle Gear Deck","ids":[100,100,100,100,85,85,85,85,89,97,97,98,98,101,126,126,133,133,138,295,198,233,248,226,269,215,233,265,233,227],"offset":23651606},{"name":"Cool Devil Deck","ids":[42,111,120,120,120,120,58,58,58,58,65,65,65,65,132,132,132,132,136,136,136,136,244,214,243,198,266,265,246,248],"offset":23651716},{"name":"Steel Gate Deck","ids":[169,169,169,169,163,163,163,163,150,150,150,150,141,141,141,141,157,165,165,168,168,290,286,293,293,252,252,252,252,254],"offset":23651826},{"name":"Dark Revival Deck","ids":[111,111,111,111,120,120,120,120,117,117,132,132,132,132,135,135,135,223,223,239,239,239,269,269,266,226,293,293,293,223],"offset":23651936},{"name":"Strong-V Deck","ids":[12,12,12,12,4,4,4,4,15,15,175,175,31,31,8,8,243,243,234,234,226,226,297,297,230,201,235,267,252,233],"offset":23652156},{"name":"Rocket Bomb Deck","ids":[175,175,175,175,175,175,175,175,2,2,12,12,17,17,17,24,24,27,27,27,29,29,29,198,266,231,295,267,266,226],"offset":23652266},{"name":"Raiden Blade Deck","ids":[175,175,175,175,175,175,175,175,12,12,29,29,27,27,118,118,125,134,134,136,136,192,192,248,226,235,246,255,242,191],"offset":23652376},{"name":"Quick Draw Deck","ids":[87,87,87,87,182,182,182,182,82,82,83,91,91,91,99,99,99,101,101,101,98,98,290,233,198,244,205,205,219,264],"offset":23652486},{"name":"Storm Bringer Deck","ids":[29,29,29,29,13,13,13,13,7,7,7,7,3,18,18,27,77,77,92,92,97,97,100,182,182,243,255,233,296,265],"offset":23652596},{"name":"Burning Love Deck","ids":[182,182,182,182,182,182,182,182,81,81,76,76,87,87,90,90,97,97,99,99,98,98,8,243,296,299,299,231,227,286],"offset":23652706},{"name":"Mountain Crusher Deck","ids":[151,151,151,151,142,142,142,142,190,190,190,165,166,166,155,155,255,231,234,223,214,235,235,202,299,226,299,288,288,288],"offset":23652816},{"name":"Rock Head Deck","ids":[151,151,151,151,142,142,142,142,144,144,154,165,165,190,190,190,169,169,160,160,246,248,233,211,221,199,221,221,262,262],"offset":23652926},{"name":"Mountain Crusher DX Deck","ids":[190,190,190,190,190,190,190,190,142,142,151,151,151,163,163,165,165,165,254,254,291,291,291,291,212,222,272,197,198,198],"offset":23653036},{"name":"Blitzkrieg Deck","ids":[167,167,167,167,153,153,153,153,146,146,146,146,145,163,166,165,169,170,170,255,226,238,249,252,270,299,223,202,299,211],"offset":23653146},{"name":"Bean Stalk Deck","ids":[165,165,165,165,160,160,160,160,148,148,148,148,97,101,146,149,153,166,156,156,158,158,191,191,191,215,246,201,201,224],"offset":23653256},{"name":"Star Force Deck","ids":[166,166,166,166,152,152,152,152,140,140,140,140,146,151,151,165,165,165,169,169,169,289,289,285,265,265,295,295,210,210],"offset":23653366},{"name":"Dancing Ghosts Deck","ids":[123,123,123,123,114,114,114,114,124,124,132,132,135,135,137,137,137,110,110,285,253,264,198,270,254,224,209,209,209,209],"offset":23653476},{"name":"Devil’s Call Deck","ids":[118,118,119,119,119,119,121,121,132,132,132,132,138,138,138,109,285,285,287,287,289,289,265,265,202,299,203,209,209,209],"offset":23653586},{"name":"Stealth Skull Deck","ids":[138,138,138,138,122,122,122,122,113,113,113,113,118,119,119,125,125,132,132,135,135,104,297,201,194,194,210,230,222,218],"offset":23653696},{"name":"Dark Prince Deck","ids":[111,111,111,111,118,118,118,118,119,119,119,119,132,132,132,132,134,134,134,133,133,133,285,285,296,296,290,214,248,221],"offset":23653806},{"name":"Friendly Deck","ids":[82,82,82,82,75,75,75,75,183,183,183,97,99,99,71,71,70,70,293,293,293,286,256,247,205,253,297,205,221,191],"offset":23653916},{"name":"Twin Meteor Deck","ids":[183,183,183,183,183,183,183,183,75,75,14,14,28,28,32,32,82,82,98,101,101,101,4,293,293,286,295,245,226,219],"offset":23654026},{"name":"Great Hope Deck","ids":[183,183,183,183,183,183,183,183,70,99,72,72,293,293,293,286,286,286,265,265,193,193,214,214,254,254,265,265,219,219],"offset":23654136},{"name":"Call of Destiny Deck","ids":[99,99,99,99,83,83,83,83,77,77,77,77,84,91,98,223,285,285,265,265,193,193,286,286,286,208,208,208,208,264],"offset":23654246},{"name":"Divine Monster Deck","ids":[184,184,184,184,184,184,184,184,71,87,87,88,88,97,97,99,99,74,74,223,223,208,208,208,208,208,286,286,286,248],"offset":23654356},{"name":"Swirling Light Deck","ids":[184,184,184,184,184,184,184,184,71,49,56,61,63,63,83,83,99,99,101,39,36,36,205,205,192,221,286,286,289,246],"offset":23654466},{"name":"Head-On Collision Deck","ids":[97,97,97,97,90,90,90,90,83,83,86,86,100,100,100,100,73,256,293,289,245,224,221,224,199,255,224,204,195,245],"offset":23654686},{"name":"Beetle Cross Deck","ids":[97,97,97,97,86,86,86,86,79,79,79,79,74,74,74,74,84,87,101,299,299,198,240,222,248,292,292,204,285,289],"offset":23654796},{"name":"Three Signs Deck","ids":[12,12,12,12,4,4,4,4,0,0,0,0,17,17,27,27,29,29,175,175,206,206,206,290,290,290,226,254,224,253],"offset":23655126},{"name":"Sun’s Gift Deck","ids":[29,29,29,29,20,20,20,20,7,7,7,7,3,3,3,3,13,27,27,230,230,230,290,290,286,286,206,206,285,285],"offset":23655236},{"name":"Hyper Digivolution Deck","ids":[3,3,3,3,7,20,20,20,20,14,14,27,27,27,29,29,29,29,30,30,30,290,290,293,292,224,206,206,206,206],"offset":23655346},{"name":"Ninja Deck","ids":[182,182,182,182,182,182,182,182,156,76,76,89,89,97,97,98,98,166,73,205,205,205,253,287,204,204,204,265,288,288],"offset":23655456},{"name":"Flower Fairies Deck","ids":[98,98,98,98,84,84,84,84,78,78,78,78,73,73,73,73,81,83,97,100,100,265,208,208,208,208,193,287,299,299],"offset":23655566},{"name":"Princess Deck","ids":[81,81,84,84,84,84,98,98,98,98,183,183,183,183,73,73,73,73,290,290,290,290,292,292,292,292,288,288,289,289],"offset":23655676},{"name":"Yellow Submarine Deck","ids":[190,190,190,190,190,190,190,190,34,34,47,47,47,61,61,61,63,142,151,151,293,293,293,293,289,289,289,286,286,286],"offset":23655786},{"name":"Shoot Everything! Deck","ids":[62,62,62,62,46,46,46,46,39,39,39,39,37,37,37,37,35,55,66,207,207,207,289,290,290,286,286,248,202,293],"offset":23655896},{"name":"Bonding Deck","ids":[35,35,35,35,37,37,37,37,62,62,62,62,61,61,61,61,64,64,286,286,286,286,293,293,293,293,207,207,207,207],"offset":23656006},{"name":"Armed Deck","ids":[61,61,61,61,47,47,47,47,40,40,40,40,34,34,34,34,51,66,207,207,207,207,207,286,286,248,248,245,287,287],"offset":23656116},{"name":"First Aid Deck","ids":[34,34,34,47,47,47,47,49,49,61,61,61,61,64,64,64,64,0,0,293,293,201,201,196,288,288,207,207,207,207],"offset":23656226},{"name":"Intercepting Traps Deck","ids":[97,97,97,97,86,86,86,86,79,79,79,79,74,74,74,74,90,101,100,100,289,289,289,289,253,253,253,253,195,195],"offset":23656336},{"name":"Program Deck","ids":[74,74,74,74,86,86,86,86,90,90,97,97,97,97,100,100,100,100,69,208,208,208,208,293,293,293,290,290,290,285],"offset":23656446},{"name":"Return Deck","ids":[97,97,97,97,87,87,87,87,80,80,80,80,81,90,90,85,85,99,99,100,100,73,256,256,212,224,231,204,285,196],"offset":23659416},{"name":"Divine Sword Deck","ids":[82,82,82,82,75,75,75,75,70,70,70,70,97,97,97,183,183,183,183,208,208,208,287,287,293,293,219,219,219,192],"offset":23656556},{"name":"Shining Goddess Deck","ids":[99,99,99,99,83,83,83,83,77,77,77,77,71,71,71,71,85,84,97,98,184,184,213,293,293,293,293,199,208,192],"offset":23656666},{"name":"Wormhole Deck","ids":[104,104,104,104,117,117,117,117,119,119,134,134,135,135,135,187,187,187,187,105,293,293,293,287,287,287,287,286,286,203],"offset":23656886},{"name":"Rough Sea King Deck","ids":[63,63,63,63,50,50,50,50,43,43,43,43,36,36,36,36,41,54,61,65,65,287,287,287,293,289,285,288,286,203],"offset":23656996},{"name":"Toy Castle Deck","ids":[166,166,166,166,152,152,152,152,139,139,139,139,151,151,159,159,165,165,165,141,293,293,292,292,292,288,288,290,290,196],"offset":23657106},{"name":"Machine Empire Deck","ids":[134,134,134,134,124,124,124,124,108,108,108,108,125,125,133,133,133,133,105,287,287,287,290,290,290,293,293,286,285,196],"offset":23657216},{"name":"Evil Flower Deck","ids":[133,133,133,133,118,118,118,118,110,110,110,110,117,117,132,132,132,107,107,287,287,287,287,287,286,286,286,286,290,290],"offset":23657326},{"name":"Strong Monsters Deck","ids":[134,134,134,134,119,119,119,119,107,107,107,107,103,103,103,103,139,37,293,293,293,293,287,287,287,287,291,291,289,289],"offset":23657436},{"name":"Miracle Knight’s Deck","ids":[175,175,175,175,175,175,175,175,4,4,12,12,12,15,15,15,27,27,27,0,290,290,289,289,285,285,288,288,291,291],"offset":23657546},{"name":"Storm Tamer Deck","ids":[87,87,87,87,69,69,69,69,76,76,81,81,86,86,97,97,98,98,182,182,290,290,290,290,285,285,285,285,195,195],"offset":23657656},{"name":"Ancient Legend Deck","ids":[151,151,151,151,142,142,142,142,143,161,161,165,165,165,165,190,190,190,190,141,252,252,252,291,291,291,291,286,286,292],"offset":23657766},{"name":"Heaven’s Gate Deck","ids":[82,82,82,82,75,75,75,75,70,70,70,70,81,81,98,98,98,183,183,183,286,286,286,291,291,293,293,288,288,219],"offset":23657876},{"name":"Divine Dragon Deck","ids":[99,99,99,99,83,83,83,83,77,77,77,77,71,71,71,71,88,88,184,184,289,289,289,289,291,291,286,286,286,286],"offset":23657986},{"name":"Forever Increase Deck","ids":[132,132,132,132,119,119,119,119,109,109,109,109,105,105,105,105,127,187,287,287,287,287,293,293,293,293,286,291,289,285],"offset":23658096},{"name":"Time Bomb Deck","ids":[132,132,132,132,119,119,119,119,109,109,109,109,105,105,105,105,124,117,134,288,288,285,285,285,285,290,290,290,293,293],"offset":23658206},{"name":"Invincible Emperor Deck","ids":[12,12,12,12,4,4,4,4,0,0,0,0,103,187,175,175,286,286,286,286,286,286,293,293,293,293,291,291,291,291],"offset":23658316},{"name":"Warrior Princess Deck","ids":[87,87,87,87,69,69,69,69,76,76,81,81,182,182,290,290,290,290,290,290,293,293,293,293,293,289,289,289,289,289],"offset":23658426},{"name":"Permafrost Deck","ids":[61,61,61,61,47,47,47,47,40,40,40,40,34,34,34,34,63,286,286,286,293,293,293,293,285,285,289,289,291,291],"offset":23658536},{"name":"Black Fire Heart Deck","ids":[2,2,2,1,1,1,14,14,14,14,27,27,27,27,29,29,29,288,288,288,293,293,293,293,292,292,290,290,289,289],"offset":23658866},{"name":"Patriot Deck","ids":[1,1,1,37,46,46,46,46,62,62,62,62,67,67,67,41,41,292,292,290,290,285,285,293,293,293,293,286,287,287],"offset":23658976},{"name":"Rose Garden Deck","ids":[98,98,98,98,84,84,84,84,78,78,78,78,73,73,73,73,286,286,293,293,293,293,293,289,289,291,291,287,292,264],"offset":23659196},{"name":"Blue Star Red Moon Deck","offset":23658646,"offsets_all":[23658646],"ids":[27,27,27,27,14,14,14,14,6,6,6,6,2,2,2,2,46,62,295,295,295,295,293,293,293,293,288,288,286,286]},{"name":"Desperate Space Deck","offset":23658756,"offsets_all":[23658756,23659086,23659526,23659636,23659746,23659856,23659966,23660076,23660186],"ids":[134,134,134,134,119,119,119,119,107,107,107,107,103,103,103,103,124,132,133,285,286,287,288,289,290,291,293,293,299,299]},{"name":"Who Are You? Deck","offset":23659306,"offsets_all":[23659306,23660296,23660406,23660516,23660626],"ids":[170,170,170,170,156,156,156,156,145,145,145,145,144,155,161,165,169,169,171,171,201,201,238,238,253,253,253,253,296,296]}]'''


def apply_handmade_opponent_decks(bin_data):
    """Option 2: write the exact, hand-curated deck lists (from the
    user-edited review file) directly — no randomization at all."""
    import json as _json
    deck_data = _json.loads(_HANDMADE_OPPONENT_DECKS_JSON)

    bdrv_lba = find_file_lba(bytes(bin_data), _BDRV_SIGNATURE)
    if bdrv_lba is None:
        print("[ERROR] Could not locate B.DRV — skipping handmade opponent decks.")
        return
    bdrv = bytearray(extract_file_from_bin(bin_data, bdrv_lba, _BDRV_SIZE))

    print(f"\n[*] Writing {len(deck_data)} hand-curated opponent decks ...")
    for d in deck_data:
        offsets = d.get('offsets_all', [d['offset']])
        for off in offsets:
            for i, cid in enumerate(d['ids'][:30]):
                bdrv[off + i*2 : off + i*2 + 2] = cid.to_bytes(2, 'little')

    write_file_into_bin(bin_data, bdrv_lba, bytes(bdrv))


def prompt_opponent_deck_mode():
    print("\n" + "=" * 64)
    print("  OPPONENT DECK STRENGTH")
    print("=" * 64)
    print("  0 = Leave opponent decks as-is (only card stats are randomized)")
    print("  1 = Randomized deck lists (tier-based strengthening)")
    print("  2 = Hand-curated decks (a fixed, pre-designed deck per opponent)")
    choice = _prompt("  Choice (0/1/2): ", valid=['0', '1', '2'])
    return choice



def apply_opponent_deck_strengthening(bin_data):
    """Locate B.DRV in the .bin, strengthen all 109 standard opponent decks
    per their assigned tier, apply the Fire Heart (Davis) special case, and
    write everything back."""
    import json as _json
    deck_data = _json.loads(_OPPONENT_DECK_DATA_JSON)

    bdrv_lba = find_file_lba(bytes(bin_data), _BDRV_SIGNATURE)
    if bdrv_lba is None:
        print("[ERROR] Could not locate B.DRV — skipping opponent deck strengthening.")
        return
    bdrv = bytearray(extract_file_from_bin(bin_data, bdrv_lba, _BDRV_SIZE))

    full_lookup = build_full_card_lookup(CARD_DATABASE)
    pools = _build_element_pools()

    print(f"\n[*] Strengthening {len(deck_data)} opponent decks ...")
    tier_counts = {}
    for d in deck_data:
        counts = {int(k): v for k, v in d['digimon_counts'].items()}
        new_counts, options, protect_id = strengthen_opponent_deck(
            counts, d['star_id'], d['colors'], d['tier'], full_lookup, pools, _rank_sorted_unique)

        ids_in_order = []
        for cid, cnt in new_counts.items():
            ids_in_order.extend([cid] * cnt)
        ids_in_order.extend(options)
        ids_in_order = ids_in_order[:30]
        while len(ids_in_order) < 30:
            ids_in_order.append(options[0] if options else 264)

        offsets = d.get('offsets_all', [d['offset']])
        for off in offsets:
            for i, cid in enumerate(ids_in_order):
                bdrv[off + i*2 : off + i*2 + 2] = cid.to_bytes(2, 'little')
        tier_counts[d['tier']] = tier_counts.get(d['tier'], 0) + 1

    apply_fire_heart_davis_sevens(bdrv)

    print("    tier distribution:", dict(sorted(tier_counts.items())))
    write_file_into_bin(bin_data, bdrv_lba, bytes(bdrv))


def run_full_randomizer():
    global STAT_MODE
    print_intro_summary()
    STAT_MODE = prompt_stat_mode()
    print(f"[*] Loading {FILE_PATH} ...")
    with open(FILE_PATH, 'rb') as f:
        original_bin = f.read()

    working = bytearray(original_bin)

    # --- Stage 0: engine fixes (crash / collection / deck-limit) ---
    apply_executable_fixes(working)
    apply_pack_eligibility_fixes(working)

    # --- Stage 1: card stat + option randomization (proven logic, unchanged) ---
    search_block = working[START_SEARCH_OFFSET:END_SEARCH_OFFSET]
    max_orders = build_max_orders(CARD_DATABASE)
    dp_group_avg = build_dp_group_averages(CARD_DATABASE, DP_DATA)

    if STAT_MODE == "untouched":
        print("[*] Untouched stats mode -- skipping all card stat changes, every card keeps its vanilla values")
        guaranteed_strong_ids = compute_guaranteed_strong_ids(CARD_DATABASE)
        ok = not_found = no_stat = 0
    else:
        print(f"[*] Altering card stats ({len(CARD_DATABASE)} cards) ...")
        guaranteed_strong_ids = compute_guaranteed_strong_ids(CARD_DATABASE)
        recolor_handled = (apply_recolor_pairs(working, search_block, max_orders, dp_group_avg, guaranteed_strong_ids)
                            if STAT_MODE == "randomizer" else set())
        ok = not_found = no_stat = 0
    for card in CARD_DATABASE:
        if STAT_MODE == "untouched":
            continue
        name, orig_hp, orig_cir = card["name"], card["orig_hp"], card["orig_cir"]
        element, stage, order = card["element"], card["stage"], card["order"]

        if name in recolor_handled:
            ok += 1
            continue

        if name in ARMOR_DIGIMON_ELEMENT and STAT_MODE == "randomizer":
            # Fixed stats, no randomization -- see armor_digimon_fixed_stats.
            search = make_search_bytes(card)
            rel = find_search_bytes_at_word_boundary(search_block, search) \
                if card.get("card_id") is None else search_block.find(search)
            if rel == -1:
                not_found += 1
                continue
            name_abs = START_SEARCH_OFFSET + rel
            name_len = (len(card["name"]) + 1) if card.get("card_id") is not None else len(search)
            if card.get("card_id") is not None:
                name_abs += 3
            hp_off = find_hp(working, name_abs, name_len, orig_hp, orig_cir)
            if hp_off is None:
                no_stat += 1
                continue
            triangle_off = find_triangle_offset(working, hp_off)
            if triangle_off is None:
                no_stat += 1
                continue
            cross_off = find_cross(working, triangle_off, hp_off)
            new_hp, new_circle, new_triangle, new_cross = armor_digimon_fixed_stats(name)
            write_le16(working, hp_off, new_hp)
            write_le16(working, hp_off + 2, new_circle)
            write_le16(working, triangle_off, new_triangle)
            if cross_off is not None and cross_off + 2 <= len(working):
                write_le16(working, cross_off, new_cross)
            ok += 1
            continue

        if (name in FIXED_EQUAL_ATTACK_CARDS or name in FIXED_STAT_PAIRS) and STAT_MODE == "randomizer":
            search = make_search_bytes(card)
            rel = find_search_bytes_at_word_boundary(search_block, search) \
                if card.get("card_id") is None else search_block.find(search)
            if rel == -1:
                not_found += 1
                continue
            name_abs = START_SEARCH_OFFSET + rel
            name_len = (len(card["name"]) + 1) if card.get("card_id") is not None else len(search)
            if card.get("card_id") is not None:
                name_abs += 3
            hp_off = find_hp(working, name_abs, name_len, orig_hp, orig_cir)
            if hp_off is None:
                no_stat += 1
                continue
            triangle_off = find_triangle_offset(working, hp_off)
            if triangle_off is None:
                no_stat += 1
                continue
            cross_off = find_cross(working, triangle_off, hp_off)

            if name in FIXED_EQUAL_ATTACK_CARDS:
                spec = FIXED_EQUAL_ATTACK_CARDS[name]
                new_hp = flat_rand_stat(*spec["HP"])
                shared = flat_rand_stat(*spec["attack"])
                new_circle = new_triangle = new_cross = shared
            else:
                spec = FIXED_STAT_PAIRS[name]
                new_hp, new_circle, new_triangle, new_cross = (
                    spec["HP"], spec["Circle"], spec["Triangle"], spec["Cross"])

            write_le16(working, hp_off, new_hp)
            write_le16(working, hp_off + 2, new_circle)
            write_le16(working, triangle_off, new_triangle)
            if cross_off is not None and cross_off + 2 <= len(working):
                write_le16(working, cross_off, new_cross)
            ok += 1
            continue

        tier = STAT_RANGES[element][stage]
        max_ord = max_orders[(element, stage)]
        search = make_search_bytes(card)
        if card.get("card_id") is None:
            # No id prefix — vulnerable to substring collisions (Veemon
            # inside ExVeemon, Gatomon inside R-Gatomon), needs the
            # boundary-aware search.
            rel = find_search_bytes_at_word_boundary(search_block, search)
        else:
            # Search already starts with [id, 0, 0] — that prefix is the
            # real disambiguator, so a plain find is correct and safe here.
            rel = search_block.find(search)
        if rel == -1:
            not_found += 1
            continue
        name_abs = START_SEARCH_OFFSET + rel
        if card.get("card_id") is not None:
            name_abs += 3
            name_len = len(card["name"]) + 1
        else:
            name_len = len(search)
        hp_off = find_hp(working, name_abs, name_len, orig_hp, orig_cir)
        if hp_off is None:
            no_stat += 1
            continue
        triangle_off = find_triangle_offset(working, hp_off)
        if triangle_off is None:
            no_stat += 1
            continue
        cross_off = find_cross(working, triangle_off, hp_off)
        is_strong = card.get("card_id") in guaranteed_strong_ids

        # Whether the card has a real Cross attack slot at all (0 power in
        # the original data = no attack there — separate from ability text).
        has_cross = (cross_off is not None and cross_off + 2 <= len(working)
                     and read_le16(working, cross_off) != 0)

        if STAT_MODE in ("semi", "hand") and name in USER_BASE_STATS:
            base = USER_BASE_STATS[name]
            if STAT_MODE == "semi":
                new_hp = semi_randomize_stat(base["HP"], stage)
                new_circle = semi_randomize_stat(base["Circle"], stage)
                new_triangle = semi_randomize_stat(base["Triangle"], stage)
                new_cross = semi_randomize_stat(base["Cross"], stage) if has_cross else 0
            else:  # "hand"
                new_hp = hand_altered_stat(base["HP"])
                new_circle = hand_altered_stat(base["Circle"])
                new_triangle = hand_altered_stat(base["Triangle"])
                new_cross = hand_altered_stat(base["Cross"]) if has_cross else 0
            write_le16(working, hp_off, new_hp)
            write_le16(working, hp_off + 2, new_circle)
            write_le16(working, triangle_off, new_triangle)
            if has_cross:
                write_le16(working, cross_off, new_cross)
            ok += 1
            continue

        # The actual boost criterion: Cross ability tag is "None" (a plain
        # attack with no bonus condition), regardless of its power value.
        apply_no_ability_boost = name in NO_ABILITY_CROSS_CARDS
        boost = (1.0 + NO_CROSS_STAT_BOOST) if apply_no_ability_boost else 1.0
        # DP secondary nudge: order remains primary (the boundary logic in
        # weighted_rand_stat_v2 is untouched); this just shifts the whole
        # window slightly for cards whose DP is notably above/below their
        # group's average.
        boost *= dp_secondary_factor(name, element, stage, DP_DATA, dp_group_avg)
        flagship_tier = flagship_tier_of(name)
        strongest_stat = ELEMENT_ATTACK_ORDER.get(element, ["Circle", "Triangle", "Cross"])[0]

        def _stat_range(stat_name, minor_boost):
            """Explicit clean range if this is the element's strongest
            attack stat (or, for Rare, ANY attack stat) and card is
            Mega/Elite; otherwise the normal boosted-with-overlap range."""
            if flagship_tier and element == "Rare":
                ranges = ELITE_STAT_RANGES if flagship_tier == "elite" else MEGA_STAT_RANGES
                return ranges["Rare"]["all_attacks"]
            if flagship_tier and stat_name == strongest_stat:
                ranges = ELITE_STAT_RANGES if flagship_tier == "elite" else MEGA_STAT_RANGES
                return ranges[element][stat_name]
            b = boost
            if flagship_tier == "elite":
                b = 1.0 + ELITE_MINOR_BOOST
            elif flagship_tier == "mega":
                b = 1.0 + MEGA_MINOR_BOOST
            return (int(tier[stat_name][0] * b), int(tier[stat_name][1] * b))

        if flagship_tier == "elite":
            hp_range = ELITE_STAT_RANGES[element]["HP"]
        elif flagship_tier == "mega":
            hp_range = MEGA_STAT_RANGES[element]["HP"]
        else:
            hp_range = (int(tier["HP"][0] * boost), int(tier["HP"][1] * boost))
        circle_range = _stat_range("Circle", boost)
        triangle_range = _stat_range("Triangle", boost)

        if card.get("flat_random"):
            new_hp, new_circle, new_triangle = (flat_rand_stat(*hp_range),
                flat_rand_stat(*circle_range), flat_rand_stat(*triangle_range))
        else:
            new_hp, frac_hp = weighted_rand_stat_v2(*hp_range, order, max_ord,
                                                      0.0, is_strong)
            new_circle, frac_c = weighted_rand_stat_v2(*circle_range, order, max_ord,
                                                          frac_hp, is_strong)
            new_triangle, frac_t = weighted_rand_stat_v2(*triangle_range, order, max_ord,
                                                            max(frac_hp, frac_c), is_strong)
        write_le16(working, hp_off, new_hp)
        write_le16(working, hp_off + 2, new_circle)
        write_le16(working, triangle_off, new_triangle)
        if has_cross:
            cross_range = _stat_range("Cross", boost)
            if card.get("flat_random"):
                new_cross = flat_rand_stat(*cross_range)
            else:
                prior = max(frac_hp, frac_c, frac_t)
                new_cross, _ = weighted_rand_stat_v2(*cross_range, order, max_ord,
                                                       prior, is_strong)
            if name in EAT_UP_HP_CROSS_CARDS:
                penalty = random.randint(5, 10) * 10 if stage == "R" else 200
                new_cross = max(cross_range[0], new_cross - penalty)
                new_cross = (new_cross // 10) * 10
            write_le16(working, cross_off, new_cross)
        ok += 1
    print(f"    stats: {ok} modified, {not_found} not found, {no_stat} no stat block")

    if STAT_MODE != "untouched":
        run_option_randomizer(working)
    else:
        print("[*] Untouched stats mode -- skipping option card value changes too")

    # --- Stage 2: starter deck randomization (B.DRV, sector-aware) ---
    chosen_elem, mode, data = prompt_starter_deck_choice()
    custom_deck = None
    if mode == 'random':
        chosen_primary, chosen_secondary = data
    else:
        focus_name, power_level, is_partner = data
        focus_elem = (_BYOD_PARTNER_ELEMENT[focus_name] if is_partner
                      else next(c['element'] for c in CARD_DATABASE
                                 if c['name'] == focus_name and c.get('element')))
        chosen_primary, chosen_secondary = focus_elem, None
        custom_list = build_custom_starter_deck(focus_name, power_level, is_partner)
        custom_deck = (chosen_elem, custom_list)

    deck_configs = {chosen_elem: (chosen_primary, chosen_secondary)}
    deck_configs.update(random_other_partner_colors(chosen_elem, chosen_primary, chosen_secondary))

    bdrv_lba = find_file_lba(bytes(working), _BDRV_SIGNATURE)
    if bdrv_lba is None:
        print("[ERROR] Could not locate B.DRV inside the .bin — aborting deck randomization.")
    else:
        randomize_starter_decks(working, bdrv_lba, _BDRV_SIZE, deck_configs, custom_deck=custom_deck)

    # --- Stage 3: opponent deck strengthening (player's choice) ---
    opponent_mode = prompt_opponent_deck_mode()
    if opponent_mode == '0':
        print("\n[*] Leaving opponent decks unchanged (stats-only mode).")
    elif opponent_mode == '1':
        apply_opponent_deck_strengthening(working)
    elif opponent_mode == '2':
        apply_handmade_opponent_decks(working)

    # --- Stage 3: write output ---
    with open(OUTPUT_BIN_PATH, 'wb') as f:
        f.write(working)
    print(f"\n[DONE] Patched .bin written to {OUTPUT_BIN_PATH}")


if __name__ == "__main__":
    # Wrapped so double-clicking this file (instead of running it from an
    # already-open terminal) never just silently closes the window --
    # whether it finishes normally or hits an error, you'll see a message
    # and the window will wait for you to press Enter before closing.
    try:
        run_full_randomizer()
    except Exception:
        import traceback
        print("\n[ERROR] Something went wrong -- here's the full details:\n")
        traceback.print_exc()
    finally:
        input("\nPress Enter to exit...")
