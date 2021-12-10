import statistics
from pathlib import Path
from loguru import logger


class ChunkHandler:
    open_chars = "([{<"
    close_chars = ")]}>"
    score_table = {')': 1, ']': 2, '}': 3, '>': 4}

    def to_opening(self, text):
        for ch_close, ch_open in zip(self.close_chars, self.open_chars):
            if ch_close in text:
                text = text.replace(ch_close, ch_open)
        return text

    def to_closing(self, text):
        for ch_open, ch_close in zip(self.open_chars, self.close_chars):
            if ch_open in text:
                text = text.replace(ch_open, ch_close)
        return text

    def get_score(self, char):
        return self.score_table[char]

    def get_score_for_line(self, stack):
        score = 0
        while len(stack) != 0:
            char = self.to_closing(stack.pop())
            score *= 5
            score += self.score_table[char]
        return score


@logger.catch()
def main():
    file_input = Path("input.txt")
    with file_input.open("r") as file_handle:
        input_lines = file_handle.readlines()
    chunk_handler = ChunkHandler()
    scores = []
    for line in input_lines:
        stack = []
        for char in line:
            if char in "({[<":
                stack.append(char)
            elif char in ")}]>":
                if not stack.pop() == chunk_handler.to_opening(char):
                    break
        else:
            score_in_line = 0
            for char in stack:
                score_in_line += chunk_handler.get_score_for_line(stack)
            scores.append(score_in_line)

    scores.sort()
    print(statistics.median(scores))

# expected 1197 3 57 3 25137
main()
