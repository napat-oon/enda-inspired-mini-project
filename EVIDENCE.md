# Checks and decisions

> This file records what I checked, what actually happened, and why I accepted or changed the work. It does not repeat setup instructions or the implementation plan.

## Concrete checks
Write the first two expectations before implementation. Fill in actual results after running them.

| Check / requirement | Given | When | Expected result | Actual result / pass or fail |
|---|---|---|---|---|
| C1 / R1-R2 — normal case | The enemy attacks on the left side of the screen and, a second after the attack ends, exposes itself briefly on the right side | I press & hold block at the time the attack lands at the designated location and counterattack by pressing attack input when and where the enemy is exposed | I took 0 damage, nothing change to my health, from the successful block. The enemy took 1 damage from the successful attack. | [Complete after checking.] |
| C2 / R3 — boundary or failure case | The enemy's attack lands at the same time the enemy is exposed and hit by the player. | I successful attack at the same time I am hit by the enemy. The game ends with both the player and the enemy losing all their health simultaneously. | The game catches the error state and announce the rare "Draw" match result. | [Complete after checking.] |
| C3 / R4 — normal case | The game ends in any result state. | I press the restart button. | The game restarts and plays again. | [Complete after checking.] |

## Two review decisions
- Plan decision: [What I accepted or changed, and why. One or two sentences.]
- Code decision: [File/function/component, what I accepted or changed, and why. One or two sentences.]

## Automated tests
- Test file and behaviour checked: [...]
- Command I ran: [...]
- Final result: [Actual test count and outcome.]
- Correction and rerun, if needed: [Brief account, or None needed.]

## Realistic use and final judgment
- Task I tried: [One realistic use from start to finish.]
- Outcome: [What happened and whether it served the intended user/purpose.]
- Judgment: [Done / Partly done / Not done, with a brief reason based on the evidence.]
- Remaining limitation or unfinished work: [One specific item, or a useful next check.]
