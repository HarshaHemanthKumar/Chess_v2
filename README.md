# Python Chess

A browser-based chess game built entirely in Python using PyScript. Play against a friend or challenge the computer!

![Python Chess Screenshot](https://via.placeholder.com/800x500.png?text=Python+Chess+Screenshot)

## Features

- Complete chess game with all standard rules
- Beautiful, responsive chessboard interface
- Two-player mode for playing with a friend
- Computer opponent with basic AI
- Move validation and highlighting of legal moves
- Check and checkmate detection
- Runs entirely in the browser using Python (no JavaScript required)

## How to Play

1. Start the local web server (see Setup and Installation below)
2. Open `http://localhost:8000` in a modern web browser (Chrome, Firefox, Edge, or Safari)
3. The game starts with White to move
4. Click on a piece to select it - valid moves will be highlighted
5. Click on a highlighted square to move your piece
6. Use the "Play vs AI" button to toggle between two-player mode and playing against the computer
7. Click "New Game" to reset the board at any time

## Technical Details

This project demonstrates how to build a complete web application using Python that runs entirely in the browser. While a simple local web server is needed to serve the files (due to PyScript's security restrictions), all game logic runs client-side in the browser.

### Technologies Used

- **Python**: All game logic is written in Python
- **PyScript**: Allows Python code to run in the browser
- **python-chess**: A Python library for chess move validation and game state
- **HTML/CSS**: For the user interface

### How It Works

1. The application uses PyScript to run Python code directly in the browser
2. The chess engine is built using the python-chess library
3. DOM manipulation is handled through PyScript's JavaScript interoperability
4. The AI opponent uses a simple algorithm to select moves

## Setup and Installation

PyScript requires a web server to load local files. Follow these steps:

1. Download or clone this repository
2. Start the local web server by running:
   ```
   python server.py
   ```
3. Open `http://localhost:8000` in a modern web browser
4. Wait a few moments for PyScript to initialize
5. Start playing!

Note: The first load may take a few seconds as PyScript downloads the necessary Python packages. Do not open the HTML file directly, as PyScript cannot access local files without a web server.

## Requirements

- Python 3.6 or higher (to run the local web server)
- A modern web browser with JavaScript enabled
- Internet connection (for the first load to download PyScript)

## Future Improvements

Potential enhancements for future versions:

- Stronger chess AI using minimax with alpha-beta pruning
- Move history and notation
- Game save/load functionality
- Time controls
- Customizable board themes
- Sound effects

## License

This project is open source and available under the MIT License.

## Acknowledgments

- [PyScript](https://pyscript.net/) for making Python in the browser possible
- [python-chess](https://python-chess.readthedocs.io/) for the chess logic library
