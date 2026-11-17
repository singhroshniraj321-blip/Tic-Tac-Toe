import streamlit as st

BG, BOX, BLUE, PINK = "#0F172A", "#1E293B", "#38BDF8", "#FF8FD6"

st.markdown(f"""<style>
.stApp {{ background: {BG}; text-align: center; }}
.block-container {{ max-width: 380px !important; padding: 1.5rem 1rem !important; }}
h3, h4, p {{ text-align: center !important; color: white !important; font-weight: bold !important; }}
[data-testid="stHorizontalBlock"] {{ flex-wrap: nowrap !important; gap: 10px !important; }}
[data-testid="stHorizontalBlock"] > div {{ min-width: 0 !important; width: 100% !important; }}
[data-testid="stHorizontalBlock"]:has(> :nth-child(3)) {{ border: 2px solid {BLUE}; border-radius: 20px; padding: 15px; background: #131C31; }}
.stButton button {{ height: 80px !important; padding: 0 !important; background: {BOX} !important; border: 2px solid {BLUE} !important; border-radius: 14px !important; }}
.stButton button:hover {{ border-color: {PINK} !important; }}
.stButton button p {{ font-size: 20px !important; color: {PINK} !important; }}
</style>""", unsafe_allow_html=True)

def check_win(b):
    wins = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
    for x, y, z in wins:
        if b[x] == b[y] == b[z] != " ":
            return [x, y, z]
    return []

def write_log(text):
    f = open("game_log.txt", "a")
    f.write(text + "\n")
    f.close()

S = st.session_state
if "board" not in S:
    S.board, S.stack, S.turn = [" "] * 9, [], "X"
    S.score = {"X": 0, "O": 0}

win = check_win(S.board)

st.markdown("### 🌸 Tic-Tac-Toe ✨")
st.write(f"Scoreboard — ❌ Player X: {S.score['X']}  |  ⭕ Player O: {S.score['O']}")

cols = st.columns(3)
for i in range(9):
    label = f"✨{S.board[i]}✨" if i in win else S.board[i]
    if cols[i % 3].button(label, key=f"b{i}", use_container_width=True):
        if S.board[i] == " " and not win:
            S.board[i] = S.turn
            S.stack.append(i)
            if check_win(S.board):
                S.score[S.turn] += 1
                write_log(f"Match Won by Player {S.turn}")
                st.balloons()
            elif " " not in S.board:
                write_log("Match Ended in a Draw")
            S.turn = "O" if S.turn == "X" else "X"
            st.rerun()

if win:
    st.success(f"🎉 WINNER: PLAYER {S.board[win[0]]}!")
elif " " not in S.board:
    st.warning("🤝 IT'S A DRAW!")
elif S.turn == "X":
    st.info("⚡ CURRENT TURN: PLAYER X")
else:
    st.error("🌸 CURRENT TURN: PLAYER O")

c1, c2 = st.columns(2)
if c1.button("⏪ Undo", use_container_width=True) and S.stack and not win:
    S.board[S.stack.pop()] = " "
    S.turn = "O" if S.turn == "X" else "X"
    st.rerun()

if c2.button("🔄 Reset", use_container_width=True):
    S.board, S.stack = [" "] * 9, []
    st.rerun()

st.markdown("#### 📜 Last 3 Matches (`game_log.txt`)")
try:
    f = open("game_log.txt", "r")
    for line in f.readlines()[-3:]:
        if "Player X" in line: st.success("🏆 " + line)
        elif "Player O" in line: st.error("🌸 " + line)
        else: st.warning("🤝 " + line)
    f.close()
except Exception:
    st.caption("No matches played yet. Play a game!")