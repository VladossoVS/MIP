from src.game.node import Node
from src.game.generator import generate_tree

def alpha_beta(_Node: Node, alpha=-2, beta=2):
    if not _Node.children:
        if _Node.ai_points > _Node.human_points:
            _Node.win_condition = 1
        elif _Node.ai_points < _Node.human_points:
            _Node.win_condition = -1
        else:
            _Node.win_condition = 0

        return _Node.win_condition

    if _Node.player_turn: # MAX move
        max_val = -2
        for Child_Node in _Node.children:
            val = alpha_beta(Child_Node, alpha, beta)
            max_val = max(max_val, val)
            alpha = max(max_val, val)
            if beta <= alpha:
                break

        _Node.win_condition = max_val
        return max_val
    else: # MIN move
        min_val = 2
        for Child_Node in _Node.children:
            val = alpha_beta(Child_Node, alpha, beta)
            min_val = min(min_val, val)
            beta = min(min_val, val)
            if beta <= alpha:
                break

        _Node.win_condition = min_val
        return min_val


def find_best_move(root: Node, max_depth: int): # -> tuple(Node, int)
    generate_tree(root, max_depth)
    alpha_beta(root)
    
    best_val = root.win_condition

    if not root.children:
        return root, best_val

    high_heur = -5
    best_move = None

    for Child_Node in root.children:
        if Child_Node.win_condition == best_val:
            if Child_Node.heuristic_val > high_heur:
                best_move = Child_Node
                high_heur = Child_Node.heuristic_val 

            if high_heur == 2:
                return Child_Node, high_heur

    return best_move, best_val