from src.game.node import Node

def get_heuristic(child_node: Node):
    parent_node = child_node.parent

    if parent_node is None:
        return 0

    # uses parent's player_turn to know who just moved
    if parent_node.player_turn == 1:  # AI just moved
        pts_delta = child_node.ai_points - parent_node.ai_points
    else:  # human just moved
        pts_delta = child_node.human_points - parent_node.human_points

    left_symbol_penalty = 0
    right_symbol_penalty = 0

    i = child_node.move_index  # index where new symbol was placed, passed to Node() during tree generation

    if i != 0 and child_node.sequence[i] == child_node.sequence[i - 1]:
        left_symbol_penalty = -1

    if i != len(child_node.sequence) - 1 and child_node.sequence[i] == child_node.sequence[i + 1]:
        right_symbol_penalty = -1

    heur_func_val = (2 * pts_delta) + left_symbol_penalty + right_symbol_penalty

    return heur_func_val