from bs4 import BeautifulSoup
import requests

class DuckDuckGoService:
    def __init__(self, query):
        self.query = query
        self.url = f"https://duckduckgo.com/html/?q={query}"
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.results = {
            "query": query,
            "wrapper": "",
            "results": []
        }
    
    def fetch_results(self):
        response = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        self.results["wrapper"] = soup.select_one('.zci__result').get_text(" ", strip=True) if soup.select_one('.zci__result') else ""

        for div in soup.select('.result'):
            title = div.select_one('h2').text.strip() if div.select_one('h2') else 'No title'
            url = div.select_one('a.result__a')['href']
            description = div.select_one('.result__snippet').text.strip() if div.select_one('.result__snippet') else 'No description'
            self.results["results"].append({
                "title": title,
                "url": url,
                "description": description
            })
        
        return self.results
    
    def get_results(self):
        if not self.results["results"]:
            return self.fetch_results()
        return self.results
    