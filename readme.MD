# 🔎 Search-API

**Search-API** is a lightweight, extensible RESTful service built with FastAPI that proxies web search requests to multiple search engines and returns structured JSON results.

---

## 🚀 Features

- **Multiple backends**: DuckDuckGo and Bing supported out of the box  
- **Clean JSON output**: `query`, `wrapper`, and an array of `{ title, url, description }`  
- **Fast & simple**: Powered by FastAPI and Uvicorn (ASGI)  
- **Pluggable architecture**: Add new engines by dropping in a service module  

---

## 📦 Installation

1. Clone the repository  
   ```bash
   git clone https://github.com/yourusername/Search-API.git
   cd Search-API
   ```

2. Create & activate a virtual environment  
   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate      # Windows
   ```

3. Install dependencies  
   ```bash
   pip install -r requirements.txt
   ```

---

## ⚙️ Running the Server

Start the API in development mode with auto-reload:

~~~bash
python run.py
~~~

By default, the server will listen on:

```
http://0.0.0.0:8000
```

You can change the host and port by editing the configuration file:

```
app/config.py
```

Example configuration:

~~~python
# app/config.py
class Settings:
    HOST: str = "127.0.0.1"
    PORT: int = 5000
    DEBUG: bool = True

settings = Settings()
~~~

The server will now run at:

```
http://127.0.0.1:5000
```

---

## 📘 API Endpoints

### `POST /search`

Perform a web search using the selected search engine (DuckDuckGo or Bing).

- **Request body (JSON)**

| Field   | Type   | Required | Description                                     |
|---------|--------|----------|-------------------------------------------------|
| `engine`| string | yes      | Search engine to use: `"duckduckgo"` or `"bing"` |
| `q`     | string | yes      | The search query                                |

- **Example Request**

~~~bash
curl -X POST "http://localhost:8000/search" \\
     -H "Content-Type: application/json" \\
     -d '{ "engine": "duckduckgo", "q": "python vs java" }'
~~~

- **Example Response**

~~~json
{
  "query": "python vs java",
  "wrapper": "DuckDuckGo instant answer text if available",
  "results": [
    {
      "title": "Python vs Java - A Comparison",
      "url": "https://example.com",
      "description": "An in-depth comparison between Python and Java..."
    },
    ...
  ]
}
~~~

- **Supported Engines**

Currently supported values for `"engine"`:

- `duckduckgo`
- `bing`

---

## 🗂 Project Structure

```
Search-API/
├── app/
│   ├── main.py            # FastAPI app instance & router registration
│   ├── api/
│   │   └── endpoints.py   # /search/duckduckgo & /search/bing routes
│   ├── models/
│   │   └── schema.py      # Pydantic models: ResultItem, SearchResult
│   └── services/
│       ├── duckduckgo.py  # DuckDuckGoService
│       └── bing.py        # BingService
├── run.py                 # Uvicorn launcher
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

---

## 🔧 Adding a New Search Engine

To add a new search engine (e.g., Qwant), follow these steps:

1. Create a new service module in `app/services/`, for example `qwant.py`, and implement a class:

~~~python
# app/services/qwant.py
class QwantService:
    def __init__(self, query: str):
        self.query = query

    def fetch_results(self) -> dict:
        # Your scraping or API logic here
        ...

    def get_results(self) -> dict:
        return self.fetch_results()
~~~

2. Update the `SearchEngine` enum in `app/api/endpoints.py`:

~~~python
class SearchEngine(str, Enum):
    duckduckgo = "duckduckgo"
    bing = "bing"
    qwant = "qwant"
~~~

3. Update the `search()` function logic in `endpoints.py`:

~~~python
from app.services.qwant import QwantService

@router.post("/search", response_model=SearchResult)
async def search(request: SearchRequest):
    if request.engine == SearchEngine.duckduckgo:
        return DuckDuckGoService(request.q).get_results()
    elif request.engine == SearchEngine.bing:
        return BingService(request.q).get_results()
    elif request.engine == SearchEngine.qwant:
        return QwantService(request.q).get_results()
    else:
        raise HTTPException(status_code=400, detail="Invalid search engine")
~~~

4. Restart the server. You can now send requests using `"engine": "qwant"` in the JSON body of `POST /search`.

---

## 📄 License

This project is licensed under the MIT License.  
Feel free to adapt and extend for your own use.