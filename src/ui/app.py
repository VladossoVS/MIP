import random
import tkinter as tk
from tkinter import messagebox

from src.ai.alphabeta import find_best_move as find_best_move_alphabeta
from src.ai.minimax import find_best_move as find_best_move_minimax
from src.experiments.metrics import MoveEntry
from src.experiments.runner import get_next_experiment_index
from src.experiments.runner import get_file_path
from src.experiments.runner import start_experiment_file
from src.experiments.runner import write_move_to_file
from src.experiments.runner import write_result_to_file
from src.game.node import Node

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

def create_start_node(length, first_turn):
    # Izveidot izvēlēta garuma nejaušu bināro secību
    sequence = [random.randint(0, 1) for _ in range(length)]
    return Node(
        sequence=sequence,
        human_points=0,
        ai_points=0,
        player_turn=first_turn,
    )

def get_move_result(a, b):
    if a == 0 and b == 0:
        return 1, 1
    if a == 0 and b == 1:
        return 0, -1
    if a == 1 and b == 0:
        return 1, -1
    return 0, 1

def apply_move(node, index):

    a = node.sequence[index]
    b = node.sequence[index + 1]

    new_value, delta = get_move_result(a, b)
    new_sequence = node.sequence[:index] + [new_value] + node.sequence[index + 2:]

    human_points = node.human_points
    ai_points = node.ai_points

    if node.player_turn == HUMAN:
        human_points += delta
        next_turn = AI
    else:
        ai_points += delta
        next_turn = HUMAN

    # Atgriež jaunu node, kas atspoguļo jauno spēles stāvokli
    return Node(
        sequence=new_sequence,
        human_points=human_points,
        ai_points=ai_points,
        player_turn=next_turn,
        parent=node,
        level=node.level + 1,
        move_index=index,
    )

def get_status_text(node):
    if len(node.sequence) == 1:
        if node.human_points > node.ai_points:
            return "Human wins!"
        if node.ai_points > node.human_points:
            return "AI wins!"
        return "Draw!"

    if node.player_turn == HUMAN:
        return "Your turn"

    return "AI is thinking..."

def get_max_depth(seq_len):
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

def ai_move(node, algorithm):
    possible_moves = list(range(len(node.sequence) - 1))
    if not possible_moves:
        return None

    if algorithm == "Minimax":
        finder = find_best_move_minimax
    else:
        finder = find_best_move_alphabeta

    depth = get_max_depth(len(node.sequence))
    choice_node, _ = finder(node, max_depth=node.level + depth)

    # Ja algoritms nespēj atgriezt gājienu, izmanto nejaušu rezerves risinājumu
    if choice_node is None or choice_node.move_index is None:
        return random.choice(possible_moves)
    
    return choice_node.move_index

class GameUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Game")
        self.root.geometry("980x620")
        self.root.minsize(860, 560)
        self.root.configure(bg=BG)
        self.current_node = None

        # Logger eksperimentu saglabāšanai txt failos
        self.experiment_file_path = None
        self.move_number = 0

        self.start_length = 15
        self.first_turn = HUMAN
        self.algorithm = "Alpha-Beta"
        self.menu_frame = tk.Frame(self.root, bg=BG)
        self.game_frame = tk.Frame(self.root, bg=BG)
        self.show_menu()

    def clear_screen(self):
        # Paslēpt abus ekrānus
        self.menu_frame.pack_forget()
        self.game_frame.pack_forget()

        # Remove vecos elementus
        for element in self.menu_frame.winfo_children():
            element.destroy()
        for element in self.game_frame.winfo_children():
            element.destroy()

    def show_menu(self):
        self.clear_screen()
        self.menu_frame.pack(fill="both", expand=True)
        center = tk.Frame(self.menu_frame, bg=BG)
        center.place(relx=0.5, rely=0.43, anchor="center")

        tk.Label(
            center,
            text="Number of cells",
            bg=BG,
            fg=FG,
            font=("Segoe UI", 13, "normal"),
        ).pack(pady=(0, 8))
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

        # Pārbaude, kurš sāk 1
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

        tk.Label(
            center,
            text="Search Algorithm",
            bg=BG,
            fg=FG,
            font=("Segoe UI", 13, "normal"),
        ).pack(pady=(0, 8))
        self.algorithm_var = tk.StringVar(value="Alpha-Beta")
        algorithm_row = tk.Frame(center, bg=BG)
        algorithm_row.pack(pady=(0, 18))

        tk.Radiobutton(
            algorithm_row,
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
            algorithm_row,
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

        tk.Button(
            center,
            text="Play",
            command=self.start_game,
            width=16,
            bg=BTN,
            fg=FG,
            activebackground=BTN_HOVER,
            activeforeground=FG,
            relief="flat",
            bd=0,
            font=("Segoe UI", 11),
            pady=8,
            cursor="hand2",
        ).pack(pady=(4, 0))

    def show_game(self):
        self.clear_screen()
        self.game_frame.pack(fill="both", expand=True, padx=18, pady=18)
        top_row = tk.Frame(self.game_frame, bg=BG)
        top_row.pack(fill="x", pady=(0, 12))

        left_buttons = tk.Frame(top_row, bg=BG)
        left_buttons.pack(side="left")

        tk.Button(
            left_buttons,
            text="Menu",
            command=self.show_menu,
            width=10,
            bg=BTN,
            fg=FG,
            activebackground=BTN_HOVER,
            activeforeground=FG,
            relief="flat",
            bd=0,
            font=("Segoe UI", 11),
            pady=6,
            cursor="hand2",
        ).pack(side="left", padx=(0, 8))

        tk.Button(
            left_buttons,
            text="Restart",
            command=self.restart_game,
            width=10,
            bg=BTN,
            fg=FG,
            activebackground=BTN_HOVER,
            activeforeground=FG,
            relief="flat",
            bd=0,
            font=("Segoe UI", 11),
            pady=6,
            cursor="hand2",
        ).pack(side="left")

        score_wrap = tk.Frame(self.game_frame, bg=BG)
        score_wrap.pack(pady=(12, 2))

        self.score_label = tk.Label(
            score_wrap,
            text="Human: 0    AI: 0",
            bg=BG,
            fg=FG,
            font=("Segoe UI", 16, "bold"),
        )
        self.score_label.pack()
        self.status_label = tk.Label(
            self.game_frame,
            text="Your turn",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 12, "normal"),
        )
        self.status_label.pack(pady=(0, 28))

        # Canvas izmantošana garām secībām
        self.sequence_canvas = tk.Canvas(self.game_frame, bg=BG, height=90, highlightthickness=0)
        self.sequence_scrollbar = tk.Scrollbar(
            self.game_frame,
            orient="horizontal",
            command=self.sequence_canvas.xview,
        )
        self.sequence_canvas.configure(xscrollcommand=self.sequence_scrollbar.set)

        self.sequence_inner_frame = tk.Frame(self.sequence_canvas, bg=BG)
        self.sequence_canvas.create_window((0, 0), window=self.sequence_inner_frame, anchor="nw")
        self.sequence_inner_frame.bind("<Configure>", self.update_scroll_region)

        self.sequence_canvas.pack(fill="x", pady=(0, 4))
        self.sequence_scrollbar.pack(fill="x", pady=(0, 12))

        self.moves_frame = tk.Frame(self.game_frame, bg=BG)
        self.moves_frame.pack(pady=(0, 24))

        self.info_label = tk.Label(
            self.game_frame,
            text=f"Algorithm: {self.algorithm}",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 10, "normal"),
        )
        self.info_label.pack(side="bottom", pady=(0, 8))

        self.render_board()

    def update_scroll_region(self, event):
        self.sequence_canvas.configure(
            scrollregion=self.sequence_canvas.bbox("all")
        )

    def start_game(self):
        length = int(self.length_var.get())

        self.start_length = length
        self.first_turn = HUMAN if self.first_turn_var.get() else AI
        self.algorithm = self.algorithm_var.get()

        # Atrast nākamo brīvo eksperimenta numuru
        experiment_index = get_next_experiment_index(self.algorithm)

        self.current_node = create_start_node(self.start_length, self.first_turn)
        self.experiment_file_path = get_file_path(self.algorithm, experiment_index)
        self.move_number = 0

        start_experiment_file(
            self.experiment_file_path,
            self.algorithm,
            experiment_index,
            self.start_length,
            self.first_turn,
            self.current_node.sequence,
        )

        self.show_game()

        # Ja AI sāk pirmais, tas veic pirmo gājienu automātiski
        if self.current_node.player_turn == AI:
            self.root.after(500, self.do_ai_turn)

    def restart_game(self):
        self.start_game()

    def render_board(self):
        if self.current_node is None:
            return

        for element in self.sequence_inner_frame.winfo_children():
            element.destroy()
        for element in self.moves_frame.winfo_children():
            element.destroy()

        # Atjaunināt punktus un statusu
        self.score_label.config(text=f"Human: {self.current_node.human_points} AI: {self.current_node.ai_points}")
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

        if len(self.current_node.sequence) == 1:
            return

        moves = list(range(len(self.current_node.sequence) - 1))
        middle = (len(moves) + 1) // 2

        first_row = tk.Frame(self.moves_frame, bg=BG)
        second_row = tk.Frame(self.moves_frame, bg=BG)
        first_row.pack()
        second_row.pack(pady=(6, 0))

        if self.current_node.player_turn == HUMAN:
            state = "normal"
        else:
            state = "disabled"

        # Izveidojiet vienu pogu katram iespējamajam moves
        for index, move_index in enumerate(moves):
            a = self.current_node.sequence[move_index]
            b = self.current_node.sequence[move_index + 1]
            new_value, delta = get_move_result(a, b)

            if delta > 0:
                points_text = f"+{delta}"
            else:
                points_text = str(delta)

            button_text = f"{a}{b} -> {new_value} ({points_text})"

            if index < middle:
                row = first_row
            if index >= middle:
                row = second_row

            button = tk.Button(
                row,
                text=button_text,
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
                # Kad tiek nospiesta pogu, veic human gājienu ar šo pāra indeksu
                command=lambda current_index=move_index: self.on_human_move(current_index),
            )
            button.pack(side="left", padx=5, pady=5)

    def on_human_move(self, move_index):
        if self.current_node is None:
            return
        if self.current_node.player_turn != HUMAN:
            return

        old_node = self.current_node
        self.current_node = apply_move(self.current_node, move_index)

        # Saglabāt human gājienu teksta failā
        self.log_move(old_node, self.current_node, "Human")
        self.render_board()
        self.finish_game()

        # Ja spēle turpinās un tagad ir AI kārta, izsauc AI kārtu
        if len(self.current_node.sequence) > 1 and self.current_node.player_turn == AI:
            self.root.after(500, self.do_ai_turn)

    def do_ai_turn(self):
        if self.current_node is None:
            return
        if self.current_node.player_turn != AI:
            return
        if len(self.current_node.sequence) == 1:
            return

        self.status_label.config(text="AI is thinking...")
        self.root.update_idletasks()

        move_index = ai_move(self.current_node, self.algorithm)
        if move_index is None:
            return

        old_node = self.current_node
        self.current_node = apply_move(self.current_node, move_index)

        # Saglabāt AI gājienu teksta failā
        self.log_move(old_node, self.current_node, "AI")
        self.render_board()
        self.finish_game()

    def log_move(self, old_node, new_node, player_name):
        if self.experiment_file_path is None:
            return
        move_index = new_node.move_index
        if move_index is None:
            return

        a = old_node.sequence[move_index]
        b = old_node.sequence[move_index + 1]
        result_value, points_delta = get_move_result(a, b)
        self.move_number += 1

        entry = MoveEntry(
            move_number=self.move_number,
            player=player_name,
            pair_index=move_index,
            pair_text=f"{a}{b}",
            result_value=result_value,
            points_delta=points_delta,
            sequence_before=old_node.sequence[:],
            sequence_after=new_node.sequence[:],
            human_points=new_node.human_points,
            ai_points=new_node.ai_points,
        )
        write_move_to_file(self.experiment_file_path, entry)

    def finish_game(self):
        if self.current_node is None:
            return
        if self.experiment_file_path is None:
            return
        if len(self.current_node.sequence) > 1:
            return

        winner_text = get_status_text(self.current_node).replace("!", "")

        write_result_to_file(
        self.experiment_file_path,
        self.current_node.human_points,
        self.current_node.ai_points,
        winner_text,
        )
        # Izdzēst logger, lai galīgais rezultāts netiktu ierakstīts divreiz
        self.experiment_file_path = None

def run_app():
    root = tk.Tk()
    GameUI(root)
    root.mainloop()

if __name__ == "__main__":
    run_app()
