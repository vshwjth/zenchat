import wikipedia as wiki
import requests

# page = wiki.page("Python (programming language)")

# Extract the text content



# print(text)

with open('output.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        try:
            page = wiki.page(line)
            text = page.content
            filename = "./output/" + page.title.replace(" ","_") + ".txt"
            print(filename)
            with open(filename, 'w') as x:
                print(page.content, file=x)
        except:
            print("can't read" + line)
       

# c