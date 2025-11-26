import logging
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from functions import executar_scraper_incremental_threads, criar_visualizacoes_automaticas, executar_scraper_incremental

warnings.filterwarnings('ignore')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

plt.style.use('default')
sns.set_palette("husl")

# Run with a single-thread incremental scraper
result = executar_scraper_incremental(max_urls=120)

# This one runs with 10 threads
# result = executar_scraper_incremental_threads(max_urls=120)
