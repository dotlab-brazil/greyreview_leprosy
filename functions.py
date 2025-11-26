from web_scraper_historico import WebScraperHistoricoColab
import time
from datetime import datetime
import random
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from urllib.parse import urlparse
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed

def executar_scraper_incremental(max_urls=120):
    print("🚀 INCREMENTAL WEB SCRAPER")
    print("🧠 ANTI-REPETITION SYSTEM ACTIVE")
    print("=" * 55)

    # Create scraper instance
    scraper = WebScraperHistoricoColab()

    # Show current history
    scraper.mostrar_historico()

    # Search URLs from multiple sources
    print("\n🔍 STARTING MULTI-SOURCE SEARCH...")
    print("=" * 50)

    urls_google = scraper.buscar_google_inteligente_incremental(max_urls=max_urls)
    urls_pubmed = scraper.buscar_pubmed_expandido()
    urls_specialized = scraper.buscar_fontes_especializadas_expandidas()

    # Combine all new URLs
    all_new_urls = list(set(urls_google + urls_pubmed + urls_specialized))

    print(f"\n📊 INCREMENTAL SEARCH SUMMARY:")
    print(f"   🔍 Google (new): {len(urls_google)} URLs")
    print(f"   🔬 PubMed (new): {len(urls_pubmed)} URLs")
    print(f"   🏥 Specialized (new): {len(urls_specialized)} URLs")
    print(f"   🆕 Total new URLs: {len(all_new_urls)} URLs")

    if not all_new_urls:
        print("\n✅ NO NEW URLS FOUND!")
        print("🎯 All available URLs were already processed before.")
        print("💡 This means the system is working perfectly!")
        print("🔄 Try again in a few days to capture new content.")
        print("📚 Or run with different parameters for deeper searches.")

        # Show statistics even with no new URLs
        if len(scraper.urls_processadas) > 0:
            print(f"\n📊 YOUR HISTORY STATISTICS:")
            print(f"   📚 Total URLs collected: {len(scraper.urls_processadas)}")
            print(f"   🎯 Database successfully built!")

        return None

    # Process new URLs
    print(f"\n🔄 PROCESSING {len(all_new_urls)} NEW URLs...")
    print("=" * 50)

    data = []
    success_count = 0
    error_count = 0

    for i, url in enumerate(all_new_urls, 1):
        print(f"[{i:2d}/{len(all_new_urls)}] {url[:55]}...")

        title, abstract, status = scraper.extrair_resumo_completo(url)

        # Identify source
        if 'pubmed.ncbi.nlm.nih.gov' in url:
            source = 'PubMed'
        elif any(term in url for term in ['who.int', 'cdc.gov']):
            source = 'Health Org.'
        elif any(term in url for term in ['nlr', 'leprosy']):
            source = 'Specialized'
        elif any(term in url for term in ['springer', 'wiley', 'journals', 'plos', 'jmir', 'ieee']):
            source = 'Journal'
        else:
            source = 'Google'

        data.append({
            'URL': url,
            'Title': title,
            'Abstract': abstract,
            'Status': status,
            'Source': source,
            'Processing_Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Execution': 'Incremental'
        })

        # Add to history
        scraper.urls_processadas.add(url)

        if status == "Sucesso":
            success_count += 1
        else:
            error_count += 1

        if i % 5 == 0:
            rate = (success_count / i) * 100
            print(f"    📊 {i}/{len(all_new_urls)} | ✅ {success_count} | ❌ {error_count} | 📈 {rate:.1f}%")

        time.sleep(random.uniform(1, 2))

    # Save updated history
    scraper.salvar_historico()

    # Create DataFrame
    df = pd.DataFrame(data)
    df = df.sort_values('Status', ascending=False)  # Success first

    # Save CSV
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_name = f"leprosy_incremental_{timestamp}.csv"
    df.to_csv(file_name, index=False, encoding='utf-8')

    # Final report
    print("\n" + "=" * 50)
    print("🎉 INCREMENTAL SEARCH COMPLETED!")
    print("=" * 50)
    print(f"📁 File: {file_name}")
    print(f"🆕 New URLs processed: {len(all_new_urls)}")
    print(f"✅ Successes: {success_count} ({success_count/len(all_new_urls)*100:.1f}%)")
    print(f"❌ Errors: {error_count}")
    print(f"📚 Total in history: {len(scraper.urls_processadas)} URLs")
    print(f"🔄 Next run will only process new URLs!")
    print("=" * 50)

    return df, file_name, scraper


def executar_scraper_incremental_threads(max_urls=120, max_workers=10):
    print("🚀 INCREMENTAL WEB SCRAPER - MULTITHREAD MODE")
    print("🧠 ANTI-REPETITION SYSTEM ACTIVE")
    print("=" * 55)

    scraper = WebScraperHistoricoColab()
    scraper.mostrar_historico()

    print("\n🔍 STARTING MULTI-SOURCE SEARCH...")
    print("=" * 50)

    urls_google = scraper.buscar_google_inteligente_incremental(max_urls=max_urls)
    urls_pubmed = scraper.buscar_pubmed_expandido()
    urls_specialized = scraper.buscar_fontes_especializadas_expandidas()

    all_new_urls = list(set(urls_google + urls_pubmed + urls_specialized))

    print(f"\n📊 INCREMENTAL SEARCH SUMMARY:")
    print(f"   🔍 Google (new): {len(urls_google)} URLs")
    print(f"   🔬 PubMed (new): {len(urls_pubmed)} URLs")
    print(f"   🏥 Specialized (new): {len(urls_specialized)} URLs")
    print(f"   🆕 Total new URLs: {len(all_new_urls)} URLs")

    if not all_new_urls:
        print("\n✅ NO NEW URLS FOUND!")
        print("🎯 All available URLs were already processed before.")
        print("💡 This means the system is working perfectly!")
        print("🔄 Try again in a few days to capture new content.")
        print("📚 Or run with different parameters for deeper searches.")

        if len(scraper.urls_processadas) > 0:
            print(f"\n📊 YOUR HISTORY STATISTICS:")
            print(f"   📚 Total URLs collected: {len(scraper.urls_processadas)}")
            print(f"   🎯 Database successfully built!")

        return None

    print(f"\n🔄 PROCESSING {len(all_new_urls)} NEW URLs USING {max_workers} THREADS...")
    print("=" * 50)

    data = []
    success_count = 0
    error_count = 0

    def process_url(url):
        """Helper function to process a single URL."""
        title, abstract, status = scraper.extrair_resumo_completo(url)

        # Identify source
        if 'pubmed.ncbi.nlm.nih.gov' in url:
            source = 'PubMed'
        elif any(term in url for term in ['who.int', 'cdc.gov']):
            source = 'Health Org.'
        elif any(term in url for term in ['nlr', 'leprosy']):
            source = 'Specialized'
        elif any(term in url for term in ['springer', 'wiley', 'journals', 'plos', 'jmir', 'ieee']):
            source = 'Journal'
        else:
            source = 'Google'

        return {
            'URL': url,
            'Title': title,
            'Abstract': abstract,
            'Status': status,
            'Source': source,
            'Processing_Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Execution': 'Incremental'
        }

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(process_url, url): url for url in all_new_urls}

        for i, future in enumerate(as_completed(future_to_url), 1):
            url = future_to_url[future]
            try:
                result = future.result()
                data.append(result)
                scraper.urls_processadas.add(url)

                if result['Status'] == "Sucesso":
                    success_count += 1
                else:
                    error_count += 1

            except Exception as e:
                print(f"⚠️ Error processing {url[:50]}... -> {e}")
                error_count += 1

            if i % 5 == 0:
                rate = (success_count / i) * 100 if i > 0 else 0
                print(f"    📊 {i}/{len(all_new_urls)} | ✅ {success_count} | ❌ {error_count} | 📈 {rate:.1f}%")

    scraper.salvar_historico()

    df = pd.DataFrame(data)
    df = df.sort_values('Status', ascending=False)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_name = f"leprosy_incremental_{timestamp}.csv"
    df.to_csv(file_name, index=False, encoding='utf-8')

    print("\n" + "=" * 50)
    print("🎉 INCREMENTAL SEARCH COMPLETED!")
    print("=" * 50)
    print(f"📁 File: {file_name}")
    print(f"🆕 New URLs processed: {len(all_new_urls)}")
    print(f"✅ Successes: {success_count} ({success_count/len(all_new_urls)*100:.1f}%)")
    print(f"❌ Errors: {error_count}")
    print(f"📚 Total in history: {len(scraper.urls_processadas)} URLs")
    print(f"🔄 Next run will only process new URLs!")
    print("=" * 50)

    return df, file_name, scraper


def criar_visualizacoes_automaticas(df, scraper):
    """
    Create automatic visualizations of collected data
    """
    print("📊 GENERATING AUTOMATIC VISUALIZATIONS...")

    # Configure figure
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Incremental Analysis - Leprosy/Hansen\'s Disease Research', fontsize=16, fontweight='bold')

    # Chart 1: Status of URLs in this run
    ax1 = axes[0, 0]
    status_counts = df['Status'].value_counts()
    colors = ['#2ecc71', '#e74c3c']
    wedges, texts, autotexts = ax1.pie(status_counts.values, labels=status_counts.index,
                                       autopct='%1.1f%%', colors=colors, startangle=90)
    ax1.set_title('Status - This Run', fontweight='bold')

    # Chart 2: Sources of URLs
    ax2 = axes[0, 1]
    source_counts = df['Source'].value_counts()
    bars = ax2.bar(range(len(source_counts)), source_counts.values,
                   color=sns.color_palette("Set2", len(source_counts)))
    ax2.set_title('URLs by Source', fontweight='bold')
    ax2.set_xlabel('Sources')
    ax2.set_ylabel('Number of URLs')
    ax2.set_xticks(range(len(source_counts)))
    ax2.set_xticklabels(source_counts.index, rotation=45, ha='right')

    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{int(height)}', ha='center', va='bottom')

    # Chart 3: Historic vs New
    ax3 = axes[0, 2]
    historic_size = len(scraper.urls_processadas) - len(df)
    new_size = len(df)

    bars = ax3.bar(['Historic URLs', 'New URLs'], [historic_size, new_size],
                   color=['#3498db', '#e74c3c'])
    ax3.set_title('Database Growth', fontweight='bold')
    ax3.set_ylabel('Number of URLs')

    for i, v in enumerate([historic_size, new_size]):
        ax3.text(i, v + 1, str(v), ha='center', va='bottom', fontweight='bold')

    # Chart 4: Most frequent domains
    ax4 = axes[1, 0]
    domains = []
    for url in df['URL']:
        try:
            domain = urlparse(url).netloc
            if domain.startswith('www.'):
                domain = domain[4:]
            domains.append(domain)
        except:
            domains.append('Unknown')

    df['Domain'] = domains
    domain_counts = df['Domain'].value_counts().head(6)

    if len(domain_counts) > 0:
        bars = ax4.bar(range(len(domain_counts)), domain_counts.values,
                       color=sns.color_palette("husl", len(domain_counts)))
        ax4.set_title('Top 6 Domains', fontweight='bold')
        ax4.set_xlabel('Domains')
        ax4.set_ylabel('URLs')
        ax4.set_xticks(range(len(domain_counts)))
        ax4.set_xticklabels([d[:12] + '...' if len(d) > 12 else d for d in domain_counts.index],
                            rotation=45, ha='right')

        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{int(height)}', ha='center', va='bottom')

    # Chart 5: Distribution of abstract sizes
    ax5 = axes[1, 1]
    success_abstracts = df[df['Status'] == 'Sucesso']['Abstract'].dropna()
    abstract_lengths = [len(abs_text) for abs_text in success_abstracts if abs_text != 'Resumo não disponível']

    if abstract_lengths:
        ax5.hist(abstract_lengths, bins=10, color='skyblue', alpha=0.7, edgecolor='black')
        ax5.set_title('Abstract Lengths', fontweight='bold')
        ax5.set_xlabel('Characters')
        ax5.set_ylabel('Frequency')
        if len(abstract_lengths) > 1:
            ax5.axvline(np.mean(abstract_lengths), color='red', linestyle='--',
                       label=f'Mean: {np.mean(abstract_lengths):.0f}')
            ax5.legend()

    # Chart 6: Execution results
    ax6 = axes[1, 2]
    successes = len(df[df['Status'] == 'Sucesso'])
    errors = len(df[df['Status'] == 'Erro'])

    bars = ax6.bar(['Successes', 'Errors'], [successes, errors], color=['#2ecc71', '#e74c3c'])
    ax6.set_title('Execution Results', fontweight='bold')
    ax6.set_ylabel('Number of URLs')

    for i, v in enumerate([successes, errors]):
        ax6.text(i, v + 0.5, str(v), ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    plt.show()

    # Automatic topic analysis
    analyze_topics_automatic(df)


def analyze_topics_automatic(df):
    """Automatically analyze topics in abstracts"""
    print("\n🎯 AUTOMATIC TOPIC ANALYSIS:")

    successes = df[df['Status'] == 'Sucesso']

    relevant_topics = {
        'mobile app': 0,
        'artificial intelligence': 0,
        'machine learning': 0,
        'diagnosis': 0,
        'screening': 0,
        'digital health': 0,
        'mhealth': 0,
        'smartphone': 0,
        'telemedicine': 0,
        'neural network': 0,
        'computer vision': 0,
        'deep learning': 0
    }

    for abstract in successes['Abstract']:
        if abstract and abstract != 'Resumo não disponível':
            abs_lower = abstract.lower()
            for topic in relevant_topics:
                if topic in abs_lower:
                    relevant_topics[topic] += 1

    # Show only found topics
    found_topics = {k: v for k, v in relevant_topics.items() if v > 0}

    if found_topics:
        print("📊 Topics identified in abstracts:")
        for topic, count in sorted(found_topics.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {topic}: {count} mentions")

        # Topic chart
        if len(found_topics) > 1:
            plt.figure(figsize=(12, 6))
            plt.bar(found_topics.keys(), found_topics.values(),
                    color=sns.color_palette("Set3", len(found_topics)))
            plt.title('Topics Identified in Abstracts', fontweight='bold', fontsize=14)
            plt.xlabel('Topics')
            plt.ylabel('Number of Mentions')
            plt.xticks(rotation=45, ha='right')

            for i, (topic, count) in enumerate(found_topics.items()):
                plt.text(i, count + 0.1, str(count), ha='center', va='bottom', fontweight='bold')

            plt.tight_layout()
            plt.show()
    else:
        print("📊 No specific topics identified in abstracts in this run.")
