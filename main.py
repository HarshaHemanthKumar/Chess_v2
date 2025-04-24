import chess
import random
import js
from pyodide.ffi import create_proxy

# Chess board representation
board = chess.Board()

# Game state
game_state = {
    "active_player": "white",
    "selected_square": None,
    "game_over": False,
    "ai_enabled": False,
    "ai_thinking": False,
    "message": "White to move"
}

# Board representation constants
COLUMNS = "abcdefgh"
ROWS = "87654321"

def setup_board():
    """Initialize the chessboard UI"""
    chessboard = js.document.getElementById("chessboard")
    chessboard.innerHTML = ""
    
    # Create the chess board squares
    for row in ROWS:
        for col in COLUMNS:
            square = js.document.createElement("div")
            square.className = "square"
            square.id = f"{col}{row}"
            
            # Alternate colors for squares
            if (ord(col) - ord('a') + int(row)) % 2 == 0:
                square.classList.add("light")
            else:
                square.classList.add("dark")
            
            # Add click event listener
            square.addEventListener("click", create_proxy(lambda event: handle_square_click(event.target.id)))
            
            chessboard.appendChild(square)
    
    update_board_display()

def update_board_display():
    """Update the visual representation of the board based on the current state"""
    # Clear all pieces
    for row in ROWS:
        for col in COLUMNS:
            square = js.document.getElementById(f"{col}{row}")
            square.innerHTML = ""
            
            # Remove highlight classes
            square.classList.remove("selected")
            square.classList.remove("valid-move")
    
    # Add pieces based on current board state
    for row in ROWS:
        for col in COLUMNS:
            square_name = f"{col}{row}"
            square = js.document.getElementById(square_name)
            
            # Get the piece at this position
            try:
                piece = board.piece_at(chess.parse_square(square_name))
                if piece:
                    # Create piece element
                    piece_element = js.document.createElement("div")
                    piece_element.className = "piece"
                    
                    # Set piece type and color
                    piece_symbol = piece.symbol()
                    piece_color = "white" if piece.color else "black"
                    piece_type = {
                        'P': 'pawn', 'N': 'knight', 'B': 'bishop',
                        'R': 'rook', 'Q': 'queen', 'K': 'king'
                    }[piece_symbol.upper()]
                    
                    piece_element.classList.add(piece_color)
                    piece_element.classList.add(piece_type)
                    
                    # Unicode chess symbols
                    unicode_pieces = {
                        'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
                        'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
                    }
                    piece_element.textContent = unicode_pieces[piece_symbol]
                    
                    square.appendChild(piece_element)
            except ValueError:
                # Invalid square name, ignore
                pass
    
    # Highlight selected square if any
    if game_state["selected_square"]:
        selected = js.document.getElementById(game_state["selected_square"])
        if selected:
            selected.classList.add("selected")
            
            # Highlight valid moves
            for move in board.legal_moves:
                if chess.square_name(move.from_square) == game_state["selected_square"]:
                    target_square = js.document.getElementById(chess.square_name(move.to_square))
                    if target_square:
                        target_square.classList.add("valid-move")
    
    # Update game status message
    update_status()

def update_status():
    """Update the game status message"""
    status_element = js.document.getElementById("status")
    
    if board.is_checkmate():
        winner = "Black" if board.turn == chess.WHITE else "White"
        game_state["message"] = f"Checkmate! {winner} wins!"
        game_state["game_over"] = True
    elif board.is_stalemate():
        game_state["message"] = "Game drawn by stalemate"
        game_state["game_over"] = True
    elif board.is_insufficient_material():
        game_state["message"] = "Game drawn due to insufficient material"
        game_state["game_over"] = True
    elif board.is_check():
        player = "White" if board.turn == chess.WHITE else "Black"
        game_state["message"] = f"{player} is in check!"
    else:
        player = "White" if board.turn == chess.WHITE else "Black"
        game_state["message"] = f"{player} to move"
    
    if game_state["ai_thinking"]:
        game_state["message"] += " (AI is thinking...)"
    
    status_element.textContent = game_state["message"]

def handle_square_click(square_id):
    """Handle click on a chess square"""
    if game_state["game_over"] or game_state["ai_thinking"]:
        return
    
    # If AI is enabled and it's black's turn, don't allow moves
    if game_state["ai_enabled"] and board.turn == chess.BLACK:
        return
    
    try:
        clicked_square = chess.parse_square(square_id)
        
        # If no square is selected yet
        if game_state["selected_square"] is None:
            piece = board.piece_at(clicked_square)
            # Only allow selecting squares with pieces of the current player's color
            if piece and piece.color == board.turn:
                game_state["selected_square"] = square_id
                update_board_display()
        else:
            # A square was already selected
            from_square = chess.parse_square(game_state["selected_square"])
            to_square = clicked_square
            
            # Check if the move is valid
            move = chess.Move(from_square, to_square)
            # Check for promotion
            if board.piece_at(from_square) and board.piece_at(from_square).piece_type == chess.PAWN:
                if (board.turn == chess.WHITE and square_id[1] == '8') or \
                   (board.turn == chess.BLACK and square_id[1] == '1'):
                    move = chess.Move(from_square, to_square, promotion=chess.QUEEN)
            
            if move in board.legal_moves:
                # Make the move
                board.push(move)
                game_state["selected_square"] = None
                update_board_display()
                
                # If AI is enabled and it's now black's turn, make AI move
                if game_state["ai_enabled"] and board.turn == chess.BLACK and not game_state["game_over"]:
                    make_ai_move()
            else:
                # If clicking on own piece, select that piece instead
                piece = board.piece_at(clicked_square)
                if piece and piece.color == board.turn:
                    game_state["selected_square"] = square_id
                    update_board_display()
                else:
                    # Invalid move, deselect
                    game_state["selected_square"] = None
                    update_board_display()
    except ValueError:
        # Invalid square ID, ignore
        pass

def make_ai_move():
    """Make a move for the AI (black player)"""
    game_state["ai_thinking"] = True
    update_status()
    
    # Use setTimeout to allow the UI to update before calculating the move
    js.setTimeout(create_proxy(calculate_ai_move), 100)

def calculate_ai_move():
    """Calculate and make the best move for the AI"""
    # Simple AI: minimax with alpha-beta pruning would be better
    # For now, just choose a random legal move
    legal_moves = list(board.legal_moves)
    if legal_moves:
        ai_move = random.choice(legal_moves)
        board.push(ai_move)
    
    game_state["ai_thinking"] = False
    update_board_display()

def reset_game():
    """Reset the game to the starting position"""
    global board
    board = chess.Board()
    game_state["selected_square"] = None
    game_state["game_over"] = False
    game_state["message"] = "White to move"
    update_board_display()

def toggle_ai():
    """Toggle AI opponent on/off"""
    game_state["ai_enabled"] = not game_state["ai_enabled"]
    ai_button = js.document.getElementById("ai-button")
    
    if game_state["ai_enabled"]:
        ai_button.textContent = "Play vs Human"
        # If it's already black's turn, make an AI move
        if board.turn == chess.BLACK and not game_state["game_over"]:
            make_ai_move()
    else:
        ai_button.textContent = "Play vs AI"
    
    update_status()

# Initialize the game when the page loads
def init():
    setup_board()
    
    # Set up event listeners for buttons
    reset_button = js.document.getElementById("reset-button")
    reset_button.addEventListener("click", create_proxy(lambda event: reset_game()))
    
    ai_button = js.document.getElementById("ai-button")
    ai_button.addEventListener("click", create_proxy(lambda event: toggle_ai()))

# Export functions to be called from HTML
__all__ = ["init", "reset_game", "toggle_ai"]
