from pathlib import Path

gamma = ""
epsilon = ""
file_input = Path("input.txt")
with file_input.open("r") as file_handle:
    lines = file_handle.readlines()
    for i in range(0, len(lines[0])-1):
        ones = [word[i] for word in lines if word[i] == "1"]
        zeros = [word[i] for word in lines if word[i] == "0"]
        if len(ones) > len(zeros):
            gamma += "1"
            epsilon += "0"
        elif len(zeros) > len(ones):
            gamma += "0"
            epsilon += "1"
        else:
            print(f"Error: both values have same size {ones} {zeros}")
gamma_int = int(gamma, 2)
epsilon_int = int(epsilon, 2)
print(gamma_int, epsilon_int)
print("result", gamma_int * epsilon_int)
