from src.game.node import Node
from src.game.generator import generate_tree

def minimax(_Node: Node):
    if not _Node.children:
        if _Node.ai_points > _Node.human_points:
            _Node.win_condition = 1
        elif _Node.ai_points < _Node.human_points:
            _Node.win_condition = -1
        else:
            _Node.win_condition = 0
        return

    eval_func = max if _Node.player_turn else min

    minimax(_Node.children[0])
    best_val = _Node.children[0].win_condition

    for Child_Node in _Node.children[1:]:
        minimax(Child_Node)
        best_val = eval_func(best_val, Child_Node.win_condition)

    _Node.win_condition = best_val
        

def find_best_move(root: Node, max_depth: int): # -> tuple(Node, int)
    generate_tree(root, max_depth)
    minimax(root)
    
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