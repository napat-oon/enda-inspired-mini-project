# Checks and decisions

> This file records what I checked, what actually happened, and why I accepted or changed the work. It does not repeat setup instructions or the implementation plan.

## Concrete checks
Write the first two expectations before implementation. Fill in actual results after running them.

| Check / requirement | Given | When | Expected result | Actual result / pass or fail |
|---|---|---|---|---|
| C1 / R1-R2, R5 — normal case | The enemy attacks on the left side of the screen and, a second after the attack ends, exposes itself briefly on the right side | I press & hold block at the time the attack lands at the designated location and counterattack by pressing attack input multiple times when and where the enemy is exposed | I took 0 damage, nothing change to my health, from the successful block. The enemy took 1 damage from the successful attack. | Pass, Pass |
| C2 / R3 — boundary or failure case | The enemy's attack is about to land at the same time the enemy is exposed and hit by the player. A few other enemy's attacks still start appearing while the game has not ended. | I successfully attack at the same time I am hit by the enemy. The game ends with both the player and the enemy losing all their health simultaneously. | The game catches the state and announce the rare "Draw" match result. The remaining enemy's attacks play until they end, but they do not change any health value. | Pass |
| C3 / R4, R6 — normal case | The game ends in any result state. | I press the restart button. | The game restarts and plays again, with different blocking and attacking positions from the last round. | Pass, Pass |

## Two review decisions
- Plan decision: I accepted Tkinter as the UI framework instead of Pygame because it is Python standard library, and it requires no runtime dependency beyond a Python installation with Tk support.
- Code decision: `game_logic.py`/`restart`, I accepted the change to the retart function because I planned and asked for the 2nd implementation which added a few more variables that should not persist between rounds so I have to ensure the game is still consistent.

## Automated tests
- Test file and behaviour checked: `test_game_logic.py`; successful and failed blocks, five-block vulnerability gating, one-hit vulnerability protection, successful and invalid attacks, win/loss/draw results, post-game immutability, restart, bounded seeded target randomization, and center-out geometry.
- Command I ran: `py -m unittest discover -v`
- Final result: 14 tests passed.
- Correction and rerun, if needed: Updated fixed-coordinate tests to use randomized targets, then reran the suite successfully.

## Realistic use and final judgment
- Task I tried: I playtest the game multiple times after each iteration, walking through the game entirely at least once, and finding bugs and unintended behaviors.
- Outcome: It was working as required but NOT intended for the first implementation, so I planned, changed, and asked for the next, second implementation which addressed and polished the behaviors. (I now understand the difference between 'Verification' (working as required) and 'Validation' (working as intended) for this mini game project).
- Judgment: (Mostly) done, the game is working as required and intended, only the timing of the prompt executions are off for a bit (the block alert and animation end before the actual block window).
- Remaining limitation or unfinished work: I would polish the timing window of blocking, play test again, then balance the time between each block and attack so the game could progress faster.
