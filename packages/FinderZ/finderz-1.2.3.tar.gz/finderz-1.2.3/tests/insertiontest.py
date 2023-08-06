from updates import update

line = 1
for i in range(10000):
    update.insertTextInFile(str(line), line, "/Users/edwardferrari/MyPythonProjects/GitHubRepos/Active/Finderz/tests/insertion.txt", appendNewLines = True)
    line += 1