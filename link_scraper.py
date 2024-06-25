import requests
import json


links = set()
count = 0
url = "https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle={category}&cmlimit=max&prop=links&format=json"
categories = []

def get_category_link(idx):
    global links
    global url
    formatted_url = url.format(category=categories[idx])
    print(".")
    result = requests.get(formatted_url)
    json_string = result.content.decode('utf-8')
    data = json.loads(json_string)
    for i in data['query']['categorymembers']:
        title = i['title']
        # print(title)
        if title.find("Category:") != -1 and title.find("country") == -1:
            categories.append(title)
        else:
            links.add(title)
    return

# print(data['query']['categorymembers'][0].keys())

# for i in data['query']['categorymembers']:
#     print(i['title'])


categories.append("Category:Mental_health")

# get_category_link
for i in categories:
    if count > 1000:
        break
    print(count)
    get_category_link(count)
    count = count + 1

with open('output.txt', 'w') as f:
    # print(len(links))
    for i in links:
        print(i, file=f)

