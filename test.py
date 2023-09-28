with open ("level_1.txt", 'w', encoding="utf-8") as file:
    file.write("""If there are any idiots in the room, will they please stand up", said the sarcastic teacher.
After a long silence, one freshman rose to his feet.
"Now then mister, why do you consider yourself an idiot?", inquired the teacher with a sneer.
"Well, actually I don't," said the student, "but I hate to see you standing up there all by yourself.""")

with open("level_1.txt", "r", encoding="utf-8") as file:
    data = file.read()

    for line in file:
        print(line)



