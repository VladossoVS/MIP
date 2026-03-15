from math import inf
from game.generator import generate_tree

def evaluate_node(node):
    return node.ai_points - node.human_points

def is_terminal(node):
    return len(node.sequence) <= 1 or not node.children

def minimax(node, depth, is_maximizing):
    if depth == 0 or is_terminal(node):
        return evaluate_node(node)

    if is_maximizing:
        best_value = -inf
        for child in node.children:
            value = minimax(child, depth - 1, False)
            best_value = max(best_value, value)
        return best_value

    best_value = inf
    for child in node.children:
        value = minimax(child, depth - 1, True)
        best_value = min(best_value, value)
    return best_value

def find_best_move(root, max_depth=4):
    if not root.children:
        generate_tree(root, max_depth)

    if not root.children:
        return None, evaluate_node(root)

    ai_turn = root.player_turn == 1
    best_child = None

    if ai_turn:
        best_value = -inf
        for child in root.children:
            value = minimax(child, max_depth - 1, False)
            child.heuristic_val = value

            if value > best_value:
                best_value = value
                best_child = child
    else:
        best_value = inf
        for child in root.children:
            value = minimax(child, max_depth - 1, True)
            child.heuristic_val = value

            if value < best_value:
                best_value = value
                best_child = child

    return best_child, best_value
