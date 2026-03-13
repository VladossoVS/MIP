from math import inf
from game.generator import generate_tree

def evaluate_node(node):
    return node.ai_points - node.human_points

def is_terminal(node):
    return len(node.sequence) <= 1 or not node.children

def alpha_beta(node, depth, alpha, beta, is_maximizing):
    if depth == 0 or is_terminal(node):
        return evaluate_node(node)

    if is_maximizing:
        best_value = -inf

        for child in node.children:
            value = alpha_beta(child, depth - 1, alpha, beta, False)
            best_value = max(best_value, value)
            alpha = max(alpha, best_value)

            if beta <= alpha:
                break

        return best_value

    best_value = inf

    for child in node.children:
        value = alpha_beta(child, depth - 1, alpha, beta, True)
        best_value = min(best_value, value)
        beta = min(beta, best_value)

        if beta <= alpha:
            break

    return best_value

def find_best_move(root, max_depth=4):
    if not root.children:
        generate_tree(root, max_depth)

    if not root.children:
        return None, evaluate_node(root)

    best_child = None
    is_ai_turn = root.player_turn == 1
    alpha = -inf
    beta = inf

    if is_ai_turn:
        best_value = -inf

        for child in root.children:
            value = alpha_beta(child, max_depth - 1, alpha, beta, False)
            child.heuristic_val = value

            if value > best_value:
                best_value = value
                best_child = child

            alpha = max(alpha, best_value)

        return best_child, best_value

    best_value = inf

    for child in root.children:
        value = alpha_beta(child, max_depth - 1, alpha, beta, True)
        child.heuristic_val = value

        if value < best_value:
            best_value = value
            best_child = child

        beta = min(beta, best_value)

    return best_child, best_value
