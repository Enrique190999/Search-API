import requests

query = "Youtube"
url = f"https://duckduckgo.com/html/?q={query}"
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)

from bs4 import BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

results = {
    "query": query,
    "wrapper":soup.select_one('.zci__result').text.strip() if soup.select_one('.zci__result') else "",
    "results": []
}

for div in soup.select('.result'):
    title = div.select_one('h2').text.strip() if div.select_one('h2') else 'No title'
    url = div.select_one('a.result__a')['href']
    description = div.select_one('.result__snippet').text.strip() if div.select_one('.result__snippet') else 'No description'
    results["results"].append({
        "title": title,
        "url": url,
        "description": description
    })
   
    
print(results)
