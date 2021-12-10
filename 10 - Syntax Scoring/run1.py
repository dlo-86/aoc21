from pathlib import Path
from loguru import logger


class ChunkHandler:
    open_chars = "([{<"
    close_chars = ")]}>"
    score_table = {')': 3, ']': 57, '}': 1197, '>': 25137}

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


@logger.catch()
def main():
    file_input = Path("input.txt")
    with file_input.open("r") as file_handle:
        input_lines = file_handle.readlines()
    chunk_handler = ChunkHandler()
    score = 0
    for line in input_lines:
        stack = []
        for char in line:
            if char in "({[<":
                stack.append(char)
            elif char in ")}]>":
                if not stack.pop() == chunk_handler.to_opening(char):
                    score += chunk_handler.get_score(char)
                    break
    print(score)

# expected 1197 3 57 3 25137
main()
