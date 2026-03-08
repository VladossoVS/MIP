# Klase priekš vienas virsotnes (stāvokļa) spēles kokā
class Node:
    def __init__(self, sequence, human_points, ai_points, player_turn, parent=None, level=0, heuristic_val=None):
        self.sequence = sequence        # list of 0s and 1s
        self.human_points = human_points      # human points
        self.ai_points = ai_points      # Ai points
        self.player_turn = player_turn  # 0 = human, 1 = Ai
        self.parent = parent            # vecāka virsotne vai None, ja tā ir sakne
        self.level = level              # līmenis kokā
        self.children = []              # bērnu virsotnes, kas atspoguļo iespējamos gājienus
        self.heuristic_val = heuristic_val  # heiristikā novērtējuma funkcijas vērtība