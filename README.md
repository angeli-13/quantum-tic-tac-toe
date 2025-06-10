# Quantum Tic-Tac-Toe
This is a fun twist on the game Tic-Tac-Toe that includes concepts from quantum mechanics! Play against a friend!

## How to Play
Quantum Tic-Tac-Toe plays like the traditional game, but with some exciting quantum rules:

**Place Entangled Particles:** Instead of placing a single 'X' or 'O' in a box, you choose two boxes on the board. A thin arced line will connect these two boxes, indicating your quantum particle is "entangled" between them. Lowercase 'x' and 'o' symbols will appear in these boxes, representing the quantum state.

**Quantum Superposition:** Your particle is potentially in both boxes, but its final location isn't determined yet. Multiple quantum particles can temporarily "share" a single box.

**Waveform Collapse:** As you play, you might create an "entanglement loop" (e.g., box A is entangled with B, B with C, and C with A). When a loop forms:

The waveform collapses, forcing the entangled particles into definite, "classical" positions.

The player who didn't complete the loop gets to choose how the most recently placed particle resolves into one of its two entangled boxes.

This choice can trigger a chain reaction, forcing other entangled particles out of their boxes and into their alternate positions, until all particles in the loop (and some related ones) settle into a single classical square. Once a square has a classical 'X' or 'O' (represented in uppercase and distinct colors), no new quantum particles can be placed there.

**Win Condition:** Just like classical Tic-Tac-Toe, the goal is to get three of your classical 'X's or 'O's in a row (horizontally, vertically, or diagonally). If both players achieve three in a row simultaneously, the game is a draw!

## How to Run
Clone the Repository:
```
git clone https://github.com/angeli-13/quantum-tic-tac-toe.git
cd quantum-tic-tac-toe
```

Ensure Python is Installed: This game requires Python 3. You can download it from python.org.

Run the Game:
```
python quantum_ttt-gui.py
```
Enjoy the quantum twists!
