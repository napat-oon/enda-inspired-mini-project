# Implementation plan

> This file records my project-specific steps reviewed before coding. Replace the prompts below with the agreed plan; refer to the requirements rather than copying the requirements here.

## Steps
1. Create `game_logic.py` for display-independent combat state, health, phases, target checks, terminal results, restart behavior, block counting, one-hit vulnerability protection, bounded target randomization, and animation geometry.
2. Implement R1, R2, R2.1, R5, and R6 in `game_logic.py`: require five successful blocks before each vulnerability, allow one successful hit per opening, randomize targets inside the game area, and keep target generation testable with seeded randomness.
3. Update `game.py` to hide inactive prompts, reveal only the current block or attack target, and animate an empty outline from the target center to full size over the exact warning or vulnerability duration. Protect scheduled callbacks across restart and game over.
4. Preserve R3 and R4 by resolving simultaneous damage before selecting `WON`, `LOST`, or `DRAW`, preventing post-game health changes, and restoring all counters and targets on restart.
5. Automate C1-C3 plus the new R2.1, R5, R6, and animation geometry cases in `test_game_logic.py`. Run them with `py -m unittest discover -v`.
6. Try a full manual task: launch the game, complete five blocks, counterattack once during an opening, observe hidden/revealed prompts and timing animation, reach a result, and press restart.

## Later changes, if any
Added an atomic simultaneous-exchange method to the logic layer so the C2 draw boundary can be tested deterministically before the terminal result is chosen.

Added R2.1, R5, and R6 to polish the last implementation. The block-attack cycle is extended. Player could end the game in one cycle because the enemy did not regain invulnerability after one hit. And the game was a prototype and had no randomization for the game replayability. 