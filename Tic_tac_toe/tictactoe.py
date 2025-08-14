import streamlit as st
import math

# Page settings
st.set_page_config(page_title="Tic Tac Toe AI", page_icon="🎮", layout="centered")
st.markdown(
    """
    <style>
    div.stButton > button {
        height: 80px;
        width: 80px;
        font-size: 30px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🎯 Tic Tac Toe - Play vs AI")

# Initialize game state
if "board" not in st.session_state:
    st.session_state.board = [[' ' for _ in range(3)] for _ in range(3)]
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "winner" not in st.session_state:
    st.session_state.winner = None

# Check winner
def check_winner(board):
    lines = board + list(map(list, zip(*board))) + [
        [board[i][i] for i in range(3)],
        [board[i][2-i] for i in range(3)]
    ]
    for line in lines:
        if line == ['X', 'X', 'X']:
            return 'X'
        elif line == ['O', 'O', 'O']:
            return 'O'
    if all(cell != ' ' for row in board for cell in row):
        return 'Draw'
    return None

# Available moves
def get_available_moves(board):
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == ' ']

# Minimax
def minimax(board, depth, is_maximizing):
    result = check_winner(board)
    if result == 'X':
        return -1
    elif result == 'O':
        return 1
    elif result == 'Draw':
        return 0
    if is_maximizing:
        best_score = -math.inf
        for (r, c) in get_available_moves(board):
            board[r][c] = 'O'
            score = minimax(board, depth + 1, False)
            board[r][c] = ' '
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for (r, c) in get_available_moves(board):
            board[r][c] = 'X'
            score = minimax(board, depth + 1, True)
            board[r][c] = ' '
            best_score = min(score, best_score)
        return best_score

# AI move
def ai_move(board):
    best_score = -math.inf
    best_move = None
    for (r, c) in get_available_moves(board):
        board[r][c] = 'O'
        score = minimax(board, 0, False)
        board[r][c] = ' '
        if score > best_score:
            best_score = score
            best_move = (r, c)
    return best_move

# Handle click
def handle_click(r, c):
    if not st.session_state.game_over and st.session_state.board[r][c] == ' ':
        st.session_state.board[r][c] = 'X'
        winner = check_winner(st.session_state.board)
        if winner:
            st.session_state.game_over = True
            st.session_state.winner = winner
            return
        ai_r, ai_c = ai_move(st.session_state.board)
        st.session_state.board[ai_r][ai_c] = 'O'
        winner = check_winner(st.session_state.board)
        if winner:
            st.session_state.game_over = True
            st.session_state.winner = winner

# Display board
for r in range(3):
    cols = st.columns(3)
    for c in range(3):
        with cols[c]:
            if st.session_state.board[r][c] == ' ':
                if st.button(" ", key=f"{r}-{c}"):
                    handle_click(r, c)
                    st.rerun()
            else:
                st.button(st.session_state.board[r][c], key=f"{r}-{c}", disabled=True)

# Show result
if st.session_state.game_over:
    if st.session_state.winner == "Draw":
        st.success("It's a Draw! 🤝")
    elif st.session_state.winner == "X":
        st.success("You Win! 🎉")
    else:
        st.error("AI Wins! 🤖")

# Restart button
if st.button("🔄 Restart Game"):
    st.session_state.board = [[' ' for _ in range(3)] for _ in range(3)]
    st.session_state.game_over = False
    st.session_state.winner = None
    st.rerun()
