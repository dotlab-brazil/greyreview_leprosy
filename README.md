# 🕵️‍♂️ Incremental Web Scraper for Leprosy/Hansen's Disease Research

This project is an **incremental web scraper** designed to collect, store, and analyze online information related to **Leprosy (Hansen's Disease)**.  
It prevents duplicate data by maintaining a **local history** of processed URLs and provides **automatic visualizations** for quick insights.

---

## ✨ Features

- 🔍 **Incremental Search**: Collects only new URLs that were not processed before.  
- 🌐 **Multi-source scraping**:
  - Google (smart queries with date filters)  
  - PubMed (academic articles)  
  - Specialized sources (WHO, CDC, NLR, Leprosy Mission, etc.)  
- 📊 **Automatic analysis and visualizations**:
  - Status of scraped URLs (success/errors)  
  - Sources distribution (Google, PubMed, Journals, etc.)  
  - Database growth over time  
  - Most frequent domains  
  - Abstract lengths distribution  
  - Automatic topic detection (AI, ML, mHealth, Telemedicine, etc.)  
- 💾 **History management**: Stores processed URLs to avoid duplication in future runs.  
- ⚡ **Thread support**: Option to scrape multiple URLs in parallel.  

---

## 📂 Project Structure

```
.
├── main.py                  # Entry point of the project
├── functions.py             # Scraper logic, incremental execution, and visualizations
├── web_scraper_historico.py # History manager and web scraping strategies
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/your-username/leprosy-webscraper.git
cd leprosy-webscraper
```

Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

Run the incremental scraper:

```bash
python main.py
```

By default, it runs the single-thread incremental scraper.  
To enable **multi-threading** (faster execution), edit `main.py`:

```python
# result = executar_scraper_incremental(max_urls=120)
result = executar_scraper_incremental_threads(max_urls=120)
```

---

## 📊 Output

- All scraped results are saved as a **CSV file** with timestamp:
  ```
  leprosy_incremental_YYYYMMDD_HHMMSS.csv
  ```
- The scraper also updates a **history file**:
  ```
  historico_leprosy_colab.json
  ```

