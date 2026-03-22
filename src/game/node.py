# Klase priekš vienas virsotnes (stāvokļa) spēles kokā
class Node:

    def __init__(self, sequence, human_points, ai_points, player_turn, parent=None, level=0, heuristic_val=None, move_index=0, win_condition=None):
        self.sequence = sequence        # list of 0s and 1s
        self.human_points = human_points      # human points
        self.ai_points = ai_points      # Ai points
        self.player_turn = player_turn  # 0 = human, 1 = Ai
        self.parent = parent            # vecāka virsotne vai None, ja tā ir sakne
        self.level = level              # līmenis kokā
        self.children = []              # bērnu virsotnes, kas atspoguļo iespējamos gājienus
        self.heuristic_val = heuristic_val  # heiristikā novērtējuma funkcijas vērtība
        self.move_index = move_index    # pāra pozīcijas indekss, kas ģenerēja šo virsotni
        self.win_condition = win_condition


    def set_heuristic(self):
        parent_node = self.parent

        if parent_node is None:
            return 0

        # uses parent's player_turn to know who just moved
        if parent_node.player_turn == 1:  # AI just moved
            pts_delta = self.ai_points - parent_node.ai_points
        else:  # human just moved
            pts_delta = self.human_points - parent_node.human_points

        left_symbol_penalty = 0
        right_symbol_penalty = 0

        i = self.move_index  # index where new symbol was placed, passed to Node() during tree generation

        if i != 0 and self.sequence[i] == self.sequence[i - 1]:
            left_symbol_penalty = -1

        if i != len(self.sequence) - 1 and self.sequence[i] == self.sequence[i + 1]:
            right_symbol_penalty = -1

        heur_func_val = (2 * pts_delta) + left_symbol_penalty + right_symbol_penalty

        self.heuristic_val = heur_func_val