import wikipedia as wiki
import requests

page = wiki.page("Python (programming language)")

# Extract the text content
text = page.links


print(text)