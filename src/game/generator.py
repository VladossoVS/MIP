from game.node import Node

# Saģenerē iespējamos gājienus no parent_node
def generate_tree(parent_node, max_depth=4):
    if parent_node.level >= max_depth or len(parent_node.sequence) <= 1:
        return

    sequence = parent_node.sequence

    for i in range(len(sequence) - 1):
        pair = sequence[i:i+2]

        if pair == [0,0]:
            new_sequence = sequence[:i] + [1] + sequence[i+2:] # 00 -> 1 un piekskaita 1p

            new_human_points = parent_node.human_points
            new_ai_points = parent_node.ai_points

            if parent_node.player_turn == 0:
                new_human_points += 1
            else: new_ai_points += 1

            child = Node(new_sequence, new_human_points, new_ai_points, 1 - parent_node.player_turn, parent_node, parent_node.level + 1)
            parent_node.children.append(child)
            #rekursīvi saģenerē iespējamos gājienus no šī bērna
            generate_tree(child, max_depth)

        elif pair == [0,1]:
            new_sequence = sequence[:i] + [0] + sequence[i+2:] # 01 -> 0 un atņem 1p

            new_human_points = parent_node.human_points
            new_ai_points = parent_node.ai_points

            if parent_node.player_turn == 0:
                new_human_points -= 1
            else: new_ai_points -= 1

            child = Node(new_sequence, new_human_points, new_ai_points, 1 - parent_node.player_turn, parent_node, parent_node.level + 1)
            parent_node.children.append(child)
            generate_tree(child, max_depth)

        elif pair == [1,0]:
            new_sequence = sequence[:i] + [1] + sequence[i+2:] # 10 -> 1 un atņem 1p

            new_human_points = parent_node.human_points
            new_ai_points = parent_node.ai_points

            if parent_node.player_turn == 0:
                new_human_points -= 1
            else: new_ai_points -= 1

            child = Node(new_sequence, new_human_points, new_ai_points, 1 - parent_node.player_turn, parent_node, parent_node.level + 1)
            parent_node.children.append(child)
            generate_tree(child, max_depth)

        elif pair == [1,1]:
            new_sequence = sequence[:i] + [0] + sequence[i+2:] # 11 -> 0 un piekskaita 1p

            new_human_points = parent_node.human_points
            new_ai_points = parent_node.ai_points

            if parent_node.player_turn == 0:
                new_human_points += 1
            else: new_ai_points += 1

            child = Node(new_sequence, new_human_points, new_ai_points, 1 - parent_node.player_turn, parent_node, parent_node.level + 1)
            parent_node.children.append(child)
            generate_tree(child, max_depth)