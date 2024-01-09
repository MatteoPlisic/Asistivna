w, h = 1, 101
arr = [[0 for x in range(w)] for y in range(h)]
print(arr, "before")

print(arr, "after")

file_path = 'mappings.txt'

with open(file_path, 'r') as file:
    for line in file:

        numbers = list(map(int, line.split()))

        question_number = numbers[0]
        answers = numbers[1:]

        print(f"Question {question_number}: Answers {answers}")
        for number in answers:
            arr[question_number].append(number)

print(arr, "gotovo")

for i in range(100):
    arr[i][0] = i

print(arr, "gotovo")