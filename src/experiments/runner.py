from pathlib import Path

from src.experiments.metrics import MoveEntry

result_folder = Path(__file__).resolve().parent / "results"

def create_result_folder():
    result_folder.mkdir(parents=True, exist_ok=True)

def get_algorithm_name(algorithm: str):
    if algorithm == "Minimax":
        return "minimax"
    return "alphabeta"

def get_next_experiment_index(algorithm: str):
    create_result_folder()
    algorithm_name = get_algorithm_name(algorithm)

    i = 1
    while True:
        file_path = result_folder / f"{algorithm_name}_experiment_{i}.txt"
        if not file_path.exists():
            return i
        i += 1

def get_file_path(algorithm: str, experiment_index: int):
    algorithm_name = get_algorithm_name(algorithm)
    return result_folder / f"{algorithm_name}_experiment_{experiment_index}.txt"

def start_experiment_file(file_path, algorithm: str, experiment_index: int, length: int, first_turn: int, sequence: list[int]):
    create_result_folder()

    if first_turn == 0:
        first_player = "Human"
    else:
        first_player = "AI"

    sequence_text = ""
    for value in sequence:
        sequence_text += str(value)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(f"Experiment: {experiment_index}\n")
        file.write(f"Algorithm: {algorithm}\n")
        file.write(f"Length: {length}\n")
        file.write(f"First turn: {first_player}\n")
        file.write(f"Initial sequence: {sequence_text}\n")
        file.write("\n")

def write_move_to_file(file_path, move_entry: MoveEntry):
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(move_entry.to_text())
        file.write("\n")

def write_result_to_file(file_path, human_points: int, ai_points: int, winner_text: str):
    with open(file_path, "a", encoding="utf-8") as file:
        file.write("Final result\n")
        file.write(f"Human points: {human_points}\n")
        file.write(f"AI points: {ai_points}\n")
        file.write(f"Winner: {winner_text}\n")
