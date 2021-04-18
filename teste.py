lines = []

with open("teste.txt", "a+"): pass

with open("teste.txt", "r") as f:
    lines = f.readlines()

    del lines[2]

with open("teste.txt", "w+") as f:
    for line in lines:
        f.write(line)
