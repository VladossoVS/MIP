import random
import tkinter as tk
from tkinter import messagebox
from src.game.node import Node
from src.ai.minimax import find_best_move as find_best_move_minimax
from src.ai.alphabeta import find_best_move as find_best_move_alphabeta

HUMAN = 0
AI = 1
MAX_DEPTH = 4
MAX_NODES = 260000

BG = "#1e3a8a"
FG = "#f3f3f3"
MUTED = "#d7d7d7"
PANEL = "#1f40a4"
CARD = "#2d5ac2"
BTN = "#4679d6"
BTN_HOVER = "#598be5"


def create_initial_node(length: int, first_turn: int) -> Node:
    sequence = [random.randint(0, 1) for i in range(length)]
    return Node(sequence=sequence, human_points=0, ai_points=0, player_turn=first_turn)


def get_possible_moves(node: Node) -> list[int]:
    return list(range(len(node.sequence) - 1))


def apply_move(node: Node, index: int) -> Node:
    if index < 0 or index >= len(node.sequence) - 1:
        raise ValueError("Invalid move index")

    a, b = node.sequence[index], node.sequence[index + 1]
    if (a, b) == (0, 0):
        new_value, delta = 1, 1
    elif (a, b) == (0, 1):
        new_value, delta = 0, -1
    elif (a, b) == (1, 0):
        new_value, delta = 1, -1
    else:
        new_value, delta = 0, 1

    new_sequence = node.sequence[:index] + [new_value] + node.sequence[index + 2:]
    human_points = node.human_points + (delta if node.player_turn == HUMAN else 0)
    ai_points = node.ai_points + (delta if node.player_turn == AI else 0)

    return Node(
        sequence=new_sequence,
        human_points=human_points,
        ai_points=ai_points,
        player_turn=AI if node.player_turn == HUMAN else HUMAN,
        parent=node,
        level=node.level + 1,
        move_index=index,
    )


def is_terminal(node: Node) -> bool:
    return len(node.sequence) == 1


def get_status_text(node: Node) -> str:
    if is_terminal(node):
        if node.human_points > node.ai_points:
            return "Human wins!"
        if node.ai_points > node.human_points:
            return "AI wins!"
        return "Draw!"
    return "Your turn" if node.player_turn == HUMAN else "AI is thinking..."

def get_max_depth(seq_len: int):
    n = seq_len - 1
    nodes = 1
    depth = 0

    while n > 1:
        nodes *= n
        if nodes > MAX_NODES:
            break
        
        n -= 1
        depth += 1
    
    return max(depth, MAX_DEPTH)


def ai_choose_move(node: Node, algorithm: str):
    moves = get_possible_moves(node)
    if not moves:
        return None

    finder = find_best_move_minimax if algorithm == "Minimax" else find_best_move_alphabeta

    depth = get_max_depth(len(moves))
    choice_node, _ = finder(node, max_depth=node.level + depth)

    if choice_node is None or choice_node.move_index is None:
        return random.choice(moves)
    return choice_node.move_index


class GameUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Number Game")
        self.root.geometry("980x620")
        self.root.minsize(860, 560)
        self.root.configure(bg=BG)

        self.current_node: Node | None = None
        self.start_length = 15
        self.first_turn = HUMAN
        self.algorithm = "Alpha-Beta"

        self.menu_frame = tk.Frame(self.root, bg=BG)
        self.game_frame = tk.Frame(self.root, bg=BG)

        self.show_menu()

    def clear_screen(self):
        self.menu_frame.pack_forget()
        self.game_frame.pack_forget()
        for widget in self.menu_frame.winfo_children():
            widget.destroy()
        for widget in self.game_frame.winfo_children():
            widget.destroy()

    def create_button(self, parent, text, command, width=14, pady=8):
        return tk.Button(
            parent,
            text=text,
            command=command,
            width=width,
            bg=BTN,
            fg=FG,
            activebackground=BTN_HOVER,
            activeforeground=FG,
            relief="flat",
            bd=0,
            font=("Segoe UI", 11),
            pady=pady,
            cursor="hand2",
        )

    def create_label(self, parent, text, size=12, bold=False, fg=FG):
        font = ("Segoe UI", size, "bold" if bold else "normal")
        return tk.Label(parent, text=text, bg=BG, fg=fg, font=font)

    def show_menu(self):
        self.clear_screen()
        self.menu_frame.pack(fill="both", expand=True)

        center = tk.Frame(self.menu_frame, bg=BG)
        center.place(relx=0.5, rely=0.43, anchor="center")

        self.create_label(center, "Number of cells", size=13).pack(pady=(0, 8))

        slider_row = tk.Frame(center, bg=BG)
        slider_row.pack(pady=(0, 18))

        self.length_var = tk.IntVar(value=15)
        tk.Scale(
            slider_row,
            from_=15,
            to=25,
            orient="horizontal",
            variable=self.length_var,
            length=180,
            bg=BG,
            fg=FG,
            troughcolor=PANEL,
            activebackground=BTN,
            highlightthickness=0,
            bd=0,
            font=("Segoe UI", 10),
        ).pack(side="left")

        tk.Label(
            slider_row,
            textvariable=self.length_var,
            bg=BG,
            fg=FG,
            font=("Segoe UI", 12),
            width=3,
        ).pack(side="left", padx=(10, 0))

        self.first_turn_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            center,
            text="First turn",
            variable=self.first_turn_var,
            bg=BG,
            fg=FG,
            selectcolor=BG,
            activebackground=BG,
            activeforeground=FG,
            highlightthickness=0,
            bd=0,
            font=("Segoe UI", 12),
        ).pack(pady=(0, 18))

        self.create_label(center, "Search Algorithm", size=13).pack(pady=(0, 8))

        self.algorithm_var = tk.StringVar(value="Alpha-Beta")
        algo_row = tk.Frame(center, bg=BG)
        algo_row.pack(pady=(0, 18))

        tk.Radiobutton(
            algo_row,
            text="Minimax",
            variable=self.algorithm_var,
            value="Minimax",
            bg=BG,
            fg=FG,
            selectcolor=PANEL,
            activebackground=BG,
            activeforeground=FG,
            highlightthickness=0,
            font=("Segoe UI", 11),
        ).pack(side="left", padx=10)

        tk.Radiobutton(
            algo_row,
            text="Alpha-Beta",
            variable=self.algorithm_var,
            value="Alpha-Beta",
            bg=BG,
            fg=FG,
            selectcolor=PANEL,
            activebackground=BG,
            activeforeground=FG,
            highlightthickness=0,
            font=("Segoe UI", 11),
        ).pack(side="left", padx=10)

        self.create_button(center, "Play", self.start_game, width=16).pack(pady=(4, 0))

    def show_game(self):
        self.clear_screen()
        self.game_frame.pack(fill="both", expand=True, padx=18, pady=18)

        top_row = tk.Frame(self.game_frame, bg=BG)
        top_row.pack(fill="x", pady=(0, 12))

        left_buttons = tk.Frame(top_row, bg=BG)
        left_buttons.pack(side="left")

        self.create_button(left_buttons, "Menu", self.show_menu, width=10, pady=6).pack(side="left", padx=(0, 8))
        self.create_button(left_buttons, "Restart", self.restart_game, width=10, pady=6).pack(side="left")

        score_wrap = tk.Frame(self.game_frame, bg=BG)
        score_wrap.pack(pady=(12, 2))

        self.score_label = self.create_label(score_wrap, "Human: 0    AI: 0", size=16, bold=True)
        self.score_label.pack()

        self.status_label = self.create_label(self.game_frame, "Your turn", size=12, fg=MUTED)
        self.status_label.pack(pady=(0, 28))

        self.sequence_canvas = tk.Canvas(self.game_frame, bg=BG, height=90, highlightthickness=0)
        self.sequence_scrollbar = tk.Scrollbar(self.game_frame, orient="horizontal", command=self.sequence_canvas.xview)
        self.sequence_canvas.configure(xscrollcommand=self.sequence_scrollbar.set)

        self.sequence_inner_frame = tk.Frame(self.sequence_canvas, bg=BG)
        self.sequence_canvas.create_window((0, 0), window=self.sequence_inner_frame, anchor="nw")
        self.sequence_inner_frame.bind(
            "<Configure>", lambda e: self.sequence_canvas.configure(scrollregion=self.sequence_canvas.bbox("all"))
        )

        self.sequence_canvas.pack(fill="x", pady=(0, 4))
        self.sequence_scrollbar.pack(fill="x", pady=(0, 12))

        self.moves_frame = tk.Frame(self.game_frame, bg=BG)
        self.moves_frame.pack(pady=(0, 24))

        self.info_label = self.create_label(self.game_frame, f"Algorithm: {self.algorithm}", size=10, fg=MUTED)
        self.info_label.pack(side="bottom", pady=(0, 8))

        self.render_board()

    def start_game(self):
        try:
            length = int(self.length_var.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid input.")
            return

        if not 15 <= length <= 25:
            messagebox.showerror("Error", "Length must be between 15 and 25.")
            return

        self.start_length = length
        self.first_turn = HUMAN if self.first_turn_var.get() else AI
        self.algorithm = self.algorithm_var.get()

        self.current_node = create_initial_node(self.start_length, self.first_turn)
        self.show_game()

        if self.current_node.player_turn == AI:
            self.root.after(500, self.do_ai_turn)

    def restart_game(self):
        self.current_node = create_initial_node(self.start_length, self.first_turn)
        self.render_board()
        if self.current_node.player_turn == AI:
            self.root.after(500, self.do_ai_turn)

    def render_board(self):
        if self.current_node is None:
            return

        for widget in self.sequence_inner_frame.winfo_children():
            widget.destroy()
        for widget in self.moves_frame.winfo_children():
            widget.destroy()

        self.score_label.config(text=f"Human: {self.current_node.human_points}    AI: {self.current_node.ai_points}")
        self.status_label.config(text=get_status_text(self.current_node))
        self.info_label.config(text=f"Algorithm: {self.algorithm}")

        for value in self.current_node.sequence:
            tk.Label(
                self.sequence_inner_frame,
                text=str(value),
                bg=CARD,
                fg=FG,
                width=3,
                height=1,
                font=("Segoe UI", 16, "bold"),
                relief="flat",
                padx=10,
                pady=10,
            ).pack(side="left", padx=5)

        if is_terminal(self.current_node):
            return

        moves = get_possible_moves(self.current_node)
        half = (len(moves) + 1) // 2

        row1 = tk.Frame(self.moves_frame, bg=BG)
        row2 = tk.Frame(self.moves_frame, bg=BG)
        row1.pack()
        row2.pack(pady=(6, 0))

        state = "normal" if self.current_node.player_turn == HUMAN else "disabled"
        for idx, move in enumerate(moves):
            a = self.current_node.sequence[move]
            b = self.current_node.sequence[move + 1]

            text = f"{a}{b} → {('1' if (a, b) in [(0,0), (1,0)] else '0')} ({'+' if (a,b) in [(0,0),(1,1)] else '-'}1)"
            btn = tk.Button(
                row1 if idx < half else row2,
                text=text,
                state=state,
                bg=BTN,
                fg=FG,
                activebackground=BTN_HOVER,
                activeforeground=FG,
                relief="flat",
                bd=0,
                font=("Segoe UI", 10),
                padx=10,
                pady=8,
                cursor="hand2" if state == "normal" else "arrow",
                command=lambda idx=move: self.on_human_move(idx),
            )
            btn.pack(side="left", padx=5, pady=5)

    def on_human_move(self, move_index: int):
        if self.current_node is None or self.current_node.player_turn != HUMAN:
            return
        self.current_node = apply_move(self.current_node, move_index)
        self.render_board()
        if not is_terminal(self.current_node) and self.current_node.player_turn == AI:
            self.root.after(500, self.do_ai_turn)

    def do_ai_turn(self):
        if self.current_node is None or self.current_node.player_turn != AI or is_terminal(self.current_node):
            return
        self.status_label.config(text="AI is thinking...")
        self.root.update_idletasks()

        move = ai_choose_move(self.current_node, self.algorithm)
        if move is None:
            return
        self.current_node = apply_move(self.current_node, move)
        self.render_board()


def run_app():
    root = tk.Tk()
    GameUI(root)
    root.mainloop()


if __name__ == "__main__":
    run_app()
