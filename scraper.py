import wikipedia as wiki
import requests

# page = wiki.page("Python (programming language)")

# Extract the text content



# print(text)


count =0 

with open('output.txt', 'r') as f:
    lines = f.readlines()
    n = len(lines)
    for line in lines:
        try:
            page = wiki.page(line)
            count = count + 1
            text = page.content
            filename = "./output/" + page.title.replace(" ","_") + ".txt"
            print("\033[H\033[J", end="")
            print(count*100/n, "%")
            print(filename)
            with open(filename, 'w') as x:
                print(page.content, file=x)
        except:
            print("can't read" + line)
       
