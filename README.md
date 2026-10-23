# enda-inspired-mini-project
A small game built with Agentic AI workflow using GitHub Copilot. Created purely for the sake of practicing Agentic AI, not vibe coding. All credits go to the original creators if there are references. Disclaimer: This mini project used AI in coding.

## Purpose
Who will use it: gamers or people who are interested in a small game or mini project (with the help of Agentic AI).
What will it help them do: playing a video game as a form of entertainment or as a practice challenge.

## Requirements
- R1: Attacking. Enemy will occasionally make an opening for player to attack for a limited time at a designated space. The player must move their cursor to that space and press attack input in the given moment. A successful player attack will decrease the enemy's health. Failing to attack in the designated time and space will cause nothing to change. (The player cannot attack if they are blocking).
- R2: Blocking. Enemy will often attack the player after hinting where it will attack at a designated space. The player must move their cursor to that space and press & hold block input in the given moment. As long as the player is holding block input at the correct area when the enemy's attack lands, it will be a successful block. A successful block will retain the player's health, no damage is done. Failing to block when the enemy's attack lands will decrease the player's health. (The player can block right away after attacking).
- R3: The game ends when the player or the enemy loses all their health. If the player is still alive at the end, the player wins. If the player is dead and the enemy is still alive at the end, the player loses. In the rare case, if both the player and the enemy are dead at the same time, the game announces a "Draw" result. When the game ends, the enemy stops attacking and no change will be made to health to prevent unwanted behavior as a boundary.
- R4: After the game ends in win or loss for the player, the player has the option to restart the game. Upon restart, the game state begins as if the game is opened the first time.

## Setup and use
- Prerequisites: Python 3.12 or another Python 3.x installation with Tkinter/Tcl-Tk support. No third-party packages are required.
- Setup: Open a terminal in this project directory. No package installation is needed.
- Run: `py game.py` on Windows, or `python game.py` where `python` points to Python 3. Hold the right mouse button over the block target during an incoming attack; left-click the attack opening when it appears.
- Run tests: `py -m unittest discover -v` on Windows, or `python -m unittest discover -v` elsewhere.

## Author and acknowledgements
- Name / student ID: [...] N O
- AI tools used: GitHub Copilot Student.
- External code/resources: [Links and what you used, or None.]

See PLAN.md for the implementation plan and EVIDENCE.md for results and decisions.
