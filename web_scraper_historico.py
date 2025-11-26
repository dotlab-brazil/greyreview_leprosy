import json
import os
from datetime import datetime
from googlesearch import search
import time
import random
import requests
from bs4 import BeautifulSoup

class WebScraperHistoricoColab:
    def __init__(self, history_file='historico_leprosy_colab.json'):
        self.history_file = history_file
        self.urls_processed = self.load_history()
        self.data_processed = []
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]

        print(f"🧠 HISTORY SYSTEM ACTIVE")
        print(f"📊 URLs already processed: {len(self.urls_processed)}")
        if len(self.urls_processed) > 0:
            print(f"💡 The system will avoid reprocessing these {len(self.urls_processed)} URLs")
        else:
            print(f"🆕 This is your first run - all URLs will be new!")
        print()

    def load_history(self):
        """Load history of already processed URLs"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
                    return set(history.get('urls_processadas', []))
            except Exception as e:
                print(f"⚠️ Error loading history: {e}")
                return set()
        return set()

    def save_history(self):
        """Save history of processed URLs"""
        try:
            history = {
                'urls_processadas': list(self.urls_processed),
                'last_update': datetime.now().isoformat(),
                'total_urls': len(self.urls_processed),
                'version': 'Colab_History_v2.0'
            }

            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)

            print(f"💾 History updated: {len(self.urls_processed)} URLs")
        except Exception as e:
            print(f"⚠️ Error saving history: {e}")

    def filter_new_urls(self, found_urls):
        """Filter only new URLs not processed before"""
        new_urls = []
        repeated_urls = []

        for url in found_urls:
            if url not in self.urls_processed:
                new_urls.append(url)
            else:
                repeated_urls.append(url)

        print(f"🔍 ANTI-REPETITION FILTER:")
        print(f"   📊 URLs found in search: {len(found_urls)}")
        print(f"   🆕 New URLs (to be processed): {len(new_urls)}")
        print(f"   🔄 Already processed URLs (ignored): {len(repeated_urls)}")

        if repeated_urls and len(repeated_urls) <= 5:
            print(f"   📋 Ignored URLs (already in history):")
            for url in repeated_urls:
                print(f"      - {url[:60]}...")
        elif repeated_urls:
            print(f"   📋 Examples of ignored URLs:")
            for url in repeated_urls[:3]:
                print(f"      - {url[:60]}...")
            print(f"      ... and {len(repeated_urls)-3} more URLs")

        return new_urls

    def buscar_google_inteligente_incremental(self, max_urls=100):
        """Google search considering history"""
        print("🔍 GOOGLE INCREMENTAL SEARCH")
        print("=" * 40)

        # Expanded queries for deeper search
        queries = [
            '("mobile app" AND "Leprosy") after:2016',
            '("web application" AND "Hansen\'s Disease") after:2016',
            '("smartphone" AND "Leprosy diagnosis") after:2016',
            '("mHealth" AND "Leprosy") after:2016',
            '("digital health" AND "Hansen\'s Disease") after:2016',
            '("AI" AND "Leprosy detection") after:2016',
            '("machine learning" AND "Leprosy") after:2016',
            '("telemedicine" AND "Hansen\'s Disease") after:2016',
            '("computer vision" AND "Leprosy lesion") after:2016',
            '("neural network" AND "Hansen\'s Disease") after:2016'
        ]

        found_urls = set()

        for i, query in enumerate(queries, 1):
            print(f"\n🔍 Query {i}/{len(queries)}: {query}")

            try:
                urls_this_query = 0
                max_per_query = max_urls // len(queries)

                for url in search(query, num_results=max_per_query, sleep_interval=random.uniform(3, 6)):
                    if url not in found_urls:
                        found_urls.add(url)
                        urls_this_query += 1

                    if urls_this_query % 5 == 0:
                        print(f"   📊 {urls_this_query} URLs from this query")

                print(f"   ✅ {urls_this_query} URLs found")

            except Exception as e:
                print(f"   ⚠️ Error: {e}")
                if "429" in str(e):
                    print("   ⏳ Google blocked - waiting...")
                    time.sleep(30)

            # Pause between queries
            if i < len(queries):
                pause = random.uniform(8, 15)
                print(f"   ⏳ Pausing {pause:.1f}s...")
                time.sleep(pause)

        # Filter new URLs
        new_urls = self.filter_new_urls(list(found_urls))
        return new_urls

    def buscar_pubmed_expandido(self):
        """Expanded PubMed search"""
        print("\n🔬 PUBMED EXPANDED SEARCH")
        print("=" * 35)

        terms = [
            "leprosy mobile app",
            "hansen disease mobile application",
            "leprosy smartphone",
            "hansen disease digital health",
            "leprosy mHealth",
            "leprosy artificial intelligence",
            "hansen disease machine learning",
            "leprosy computer vision",
            "hansen disease telemedicine"
        ]

        pubmed_urls = []

        for term in terms:
            try:
                url_api = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
                params = {
                    'db': 'pubmed',
                    'term': f'{term} AND ("2016"[Date - Publication] : "3000"[Date - Publication])',
                    'retmax': 25,
                    'retmode': 'json'
                }

                response = requests.get(url_api, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if 'esearchresult' in data and 'idlist' in data['esearchresult']:
                        for pmid in data['esearchresult']['idlist']:
                            article_url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
                            pubmed_urls.append(article_url)

                time.sleep(1)

            except Exception as e:
                print(f"   ⚠️ Error searching '{term}': {e}")

        unique_urls = list(set(pubmed_urls))
        new_urls = self.filter_new_urls(unique_urls)

        print(f"   ✅ PubMed: {len(new_urls)} new URLs")
        return new_urls

    def buscar_fontes_especializadas_expandidas(self):
        """Expanded search in specialized sources"""
        print("\n🏥 EXPANDED SPECIALIZED SOURCES")
        print("=" * 45)

        specialized_urls = [
            # International Organizations
            "https://www.who.int/health-topics/leprosy",
            "https://www.who.int/news-room/fact-sheets/detail/leprosy",
            "https://www.cdc.gov/leprosy/about/index.html",

            # Specialized Organizations
            "https://nlrinternational.org/news/new-version-nlr-skinapp-launched-4-additional-diseases/",
            "https://nlrinternational.org/what-we-do/research-innovation/",
            "https://www.leprosymission.org/what-is-leprosy/",
            "https://www.validate-network.org/pathogens/leprosy",

            # Scientific Journals
            "https://mhealth.jmir.org/2021/4/e23718",
            "https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1012550",
            "https://link.springer.com/chapter/10.1007/978-3-031-53901-5_6",
            "https://ieeexplore.ieee.org/document/7860891",
            "https://leprosyreview.org/article/93/3/20-22043",

            # National Health Agencies
            "https://www.health.state.mn.us/diseases/leprosy/index.html",
            "https://www.health.vic.gov.au/infectious-diseases/leprosy-hansens-disease",
            "https://www.chp.gov.hk/en/healthtopics/content/24/107984.html",

            # Educational Resources
            "https://www.nps.gov/kala/learn/historyculture/hansensdisease.htm",
            "https://rarediseases.org/rare-diseases/leprosy/",
            "https://www.osmosis.org/learn/Leprosy",
            "https://www.drugs.com/cg/hansen-disease-leprosy.html"
        ]

        new_urls = self.filter_new_urls(specialized_urls)

        print(f"   ✅ Specialized sources: {len(new_urls)} new URLs")
        return new_urls

    def extrair_resumo_completo(self, url, timeout=12):
        """Extract title and abstract with robust strategies"""
        for attempt in range(2):
            try:
                headers = {
                    'User-Agent': random.choice(self.user_agents),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7'
                }

                response = requests.get(url, headers=headers, timeout=timeout)
                response.raise_for_status()

                soup = BeautifulSoup(response.content, 'html.parser')

                # Extract title
                title = self._extract_title(soup)

                # Extract abstract
                abstract = self._extract_abstract_multiple_strategies(soup)

                return title, abstract, "Sucesso"

            except Exception as e:
                if attempt == 1:
                    return "Access Error", f"Error: {str(e)[:80]}", "Erro"
                time.sleep(random.uniform(1, 3))

        return "Multiple Errors", "Failed after several attempts", "Erro"

    def _extract_title(self, soup):
        """Extract title using multiple strategies"""
        title = ""

        # 1. Title tag
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.get_text().strip()

        # 2. H1 fallback
        if not title:
            h1 = soup.find('h1')
            if h1:
                title = h1.get_text().strip()

        # 3. Meta title
        if not title:
            meta_title = soup.find('meta', attrs={'name': 'title'})
            if meta_title and meta_title.get('content'):
                title = meta_title.get('content').strip()

        if not title:
            title = "Title not found"

        # Limit size
        if len(title) > 180:
            title = title[:180] + "..."

        return title

    def _extract_abstract_multiple_strategies(self, soup):
        """Extract abstract using multiple strategies"""
        abstract = ""

        # 1. Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            abstract = meta_desc.get('content').strip()

        # 2. OpenGraph description
        if not abstract:
            og_desc = soup.find('meta', attrs={'property': 'og:description'})
            if og_desc and og_desc.get('content'):
                abstract = og_desc.get('content').strip()

        # 3. Academic article abstract
        if not abstract:
            abstract_div = soup.find('div', class_=lambda x: x and 'abstract' in x.lower())
            if abstract_div:
                paragraphs = abstract_div.find_all('p')
                if paragraphs:
                    abstract = paragraphs[0].get_text().strip()

        # 4. First substantial paragraphs
        if not abstract:
            paragraphs = soup.find_all('p')
            paragraph_texts = []
            for p in paragraphs[:5]:
                text = p.get_text().strip()
                if len(text) > 40:
                    paragraph_texts.append(text)
                    if len(" ".join(paragraph_texts)) > 400:
                        break
            abstract = " ".join(paragraph_texts)

        # Limit size
        if len(abstract) > 500:
            abstract = abstract[:500] + "..."

        if not abstract or len(abstract) < 20:
            abstract = "Abstract not available"

        return abstract

    def mostrar_historico(self):
        """Show history information"""
        print("📊 HISTORY INFORMATION")
        print("=" * 35)
        print(f"📚 Total URLs processed: {len(self.urls_processed)}")

        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
                    last_update = history.get('ultima_atualizacao', 'N/A')
                    if last_update != 'N/A':
                        try:
                            dt = datetime.fromisoformat(last_update.replace('Z', '+00:00'))
                            last_update = dt.strftime('%Y-%m-%d %H:%M:%S')
                        except:
                            pass
                    print(f"🕒 Last update: {last_update}")
                    print(f"📝 Version: {history.get('versao', 'N/A')}")
            except:
                pass

        if len(self.urls_processed) > 0:
            print("\n📋 Example URLs in history:")
            for i, url in enumerate(list(self.urls_processed)[:3], 1):
                print(f"   {i}. {url[:55]}...")
            if len(self.urls_processed) > 3:
                print(f"   ... and {len(self.urls_processed)-3} more URLs")

        print("=" * 35)
