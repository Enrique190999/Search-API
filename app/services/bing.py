from bs4 import BeautifulSoup
import requests

class BingService:
    def __init__(self, query):
        self.query = query
        self.url = f"https://www.bing.com/search?q={query}"
        self.headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        self.results = {
            "query": query,
            "wrapper": "",
            "results": []
        }

    def fetch_results(self):
        response = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        for li in soup.select('.b_algo'):
            title_el = li.select_one('h2')
            url_el = li.select_one('h2 a')
            desc_el = li.select_one('.b_caption p')

            if title_el and url_el:
                title = title_el.get_text(strip=True)
                url = url_el['href']
                description = desc_el.get_text(strip=True) if desc_el else 'No description'

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
