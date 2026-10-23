# Checks and decisions

> This file records what I checked, what actually happened, and why I accepted or changed the work. It does not repeat setup instructions or the implementation plan.

## Concrete checks
Write the first two expectations before implementation. Fill in actual results after running them.

| Check / requirement | Given | When | Expected result | Actual result / pass or fail |
|---|---|---|---|---|
| C1 / R1-R2, R5 — normal case | The enemy attacks on the left side of the screen and, a second after the attack ends, exposes itself briefly on the right side | I press & hold block at the time the attack lands at the designated location and counterattack by pressing attack input multiple times when and where the enemy is exposed | I took 0 damage, nothing change to my health, from the successful block. The enemy took 1 damage from the successful attack. | Pass, Pending |
| C2 / R3 — boundary or failure case | The enemy's attack is about to land at the same time the enemy is exposed and hit by the player. A few other enemy's attacks still start appearing while the game has not ended. | I successfully attack at the same time I am hit by the enemy. The game ends with both the player and the enemy losing all their health simultaneously. | The game catches the state and announce the rare "Draw" match result. The remaining enemy's attacks play until they end, but they do not change any health value. | Pass |
| C3 / R4, R6 — normal case | The game ends in any result state. | I press the restart button. | The game restarts and plays again, with different blocking and attacking positions from the last round. | Pass, Pending |

## Two review decisions
- Plan decision: I accepted Tkinter as the UI framework instead of Pygame because it is Python standard library, and it requires no runtime dependency beyond a Python installation with Tk support.
- Code decision: [File/function/component, what I accepted or changed, and why. One or two sentences.]

## Automated tests
- Test file and behaviour checked: `test_game_logic.py`; successful and failed blocks, five-block vulnerability gating, one-hit vulnerability protection, successful and invalid attacks, win/loss/draw results, post-game immutability, restart, bounded seeded target randomization, and center-out geometry.
- Command I ran: `py -m unittest discover -v`
- Final result: 14 tests passed.
- Correction and rerun, if needed: Updated fixed-coordinate tests to use randomized targets, then reran the suite successfully.

## Realistic use and final judgment
- Task I tried: [One realistic use from start to finish.]
- Outcome: [What happened and whether it served the intended user/purpose.]
- Judgment: [Done / Partly done / Not done, with a brief reason based on the evidence.]
- Remaining limitation or unfinished work: [One specific item, or a useful next check.]
