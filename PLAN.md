# Implementation plan

> This file records my project-specific steps reviewed before coding. Replace the prompts below with the agreed plan; refer to R1–R4 rather than copying the requirements here.

## Steps
1. Create `game_logic.py` for display-independent combat state, health, phases, target checks, terminal results, and restart behavior. Create `game.py` for the Tkinter Canvas, mouse bindings, rendering, and scheduled phases.
2. Implement R1 and R2 in `game_logic.py` with a left block target, a right attack opening, left-click attacks, and held right-button blocking. Use `after()` callbacks in `game.py` to present the timing windows.
3. Handle R3 by resolving simultaneous damage before selecting `WON`, `LOST`, or `DRAW`, then rejecting further health changes and new gameplay phases after game over. Handle R4 with a restart button that restores the initial state.
4. Automate C1-C3 and the related failure cases in `test_game_logic.py`. Run them with `py -m unittest discover -v`.
5. Try a full manual task: launch the game, block an incoming attack, counterattack during the opening, reach a result, and press restart to begin a fresh match.

## Later changes, if any
Added an atomic simultaneous-exchange method to the logic layer so the C2 draw boundary can be tested deterministically before the terminal result is chosen.
