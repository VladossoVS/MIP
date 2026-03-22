class MoveEntry:
    def __init__(
        self,
        move_number: int,
        player: str,
        pair_index: int,
        pair_text: str,
        result_value: int,
        points_delta: int,
        sequence_before: list[int],
        sequence_after: list[int],
        human_points: int,
        ai_points: int,
    ):
        self.move_number = move_number
        self.player = player
        self.pair_index = pair_index
        self.pair_text = pair_text
        self.result_value = result_value
        self.points_delta = points_delta
        self.sequence_before = sequence_before
        self.sequence_after = sequence_after
        self.human_points = human_points
        self.ai_points = ai_points

    def to_text(self) -> str:
        before_text = ""
        for value in self.sequence_before:
            before_text += str(value)

        after_text = ""
        for value in self.sequence_after:
            after_text += str(value)
        sign = "+" if self.points_delta > 0 else ""

        return (
            f"Move {self.move_number}: {self.player}\n"
            f"Pair index: {self.pair_index}\n"
            f"Pair: {self.pair_text} -> {self.result_value} ({sign}{self.points_delta})\n"
            f"Before: {before_text}\n"
            f"After: {after_text}\n"
            f"Score: Human {self.human_points} | AI {self.ai_points}\n"
        )
