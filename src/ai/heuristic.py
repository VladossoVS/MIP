from game.node import Node

def get_heuristic(Child_Node: Node, i: int):
    Parent_Node = Child_Node.parent
    
    if Parent_Node == None:
        return
    
    if Child_Node.player_turn: # if TRUE -> AI
        pts_delta = Child_Node.ai_points - Parent_Node.ai_points
    else: # else -> Player
        pts_delta = Child_Node.human_points - Parent_Node.human_points

    left_symbol_penalty = 0
    right_symbol_penalty = 0

    if i != 0 and Child_Node.sequence[i] == Child_Node.sequence[i - 1]:
        left_symbol_penalty = -1
    
    if i != len(Child_Node.sequence) and Child_Node.sequence[i] == Child_Node.sequence[i + 1]:
        right_symbol_penalty = -1
    
    heur_func_val = pts_delta + left_symbol_penalty + right_symbol_penalty

    return heur_func_val