import requests
import json


links = set()
count = 0
url = "https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle={category}&cmlimit=max&prop=links&format=json"
categories = []

def get_category_link(categor: str):
    global count
    global links
    global url
    count = count+1
    formatted_url = url.format(category=categor)
    if(count > 50):
        return
    # url.format(category="Category:Mental_health")
    print(formatted_url)
    result = requests.get(formatted_url)
    json_string = result.content.decode('utf-8')
    data = json.loads(json_string)
    for i in data['query']['categorymembers']:
        title = i['title']
        # print(title)
        if title.find("Category:") != -1:
            categories.append(title)
        else:
            links.add(title)
    return

# print(data['query']['categorymembers'][0].keys())

# for i in data['query']['categorymembers']:
#     print(i['title'])


get_category_link("Category:Mental_health")


print(len(links))

