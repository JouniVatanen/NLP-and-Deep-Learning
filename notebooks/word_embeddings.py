#%% [markdown]
# # Word Embeddings part of the course
# This file will activate all the necessary sources.

#%% SETUP
import seaborn as sns
import pandas as pd
import sys
import os
import subprocess
from multiprocessing.pool import ThreadPool

# Import custom python scripts from project src/
sys.path.append("./src/")
import download_files

# Paths
processed_data_path = os.path.normpath("./data/processed")
raw_data_path = os.path.normpath("./data/raw")

#%% DOWNLOAD WIKIPEDIA DUMP FILES
# Add a path to download files from url script
def download_url_wrapper(url):
	return download_files.download_url(url, path = raw_data_path)

# Create a list of urls
dump_date = "20190701"
files = [
	"pages-articles1.xml-p10p30302.bz2",
    "pages-articles2.xml-p30304p88444.bz2",
    "pages-articles3.xml-p88445p200507.bz2",
    "pages-articles4.xml-p200511p352689.bz2",
    "pages-articles5.xml-p352690p565312.bz2"
	]
url = "https://ftp.acc.umu.se/mirror/wikimedia.org/dumps/enwiki/" + dump_date + "/enwiki-" + dump_date + "-"
urls = [url + x for x in files]

# Download data
results = ThreadPool(5).imap_unordered(download_url_wrapper, urls)
print(results)

#%%
# Create a single file
wikipedia_files = [os.path.join(raw_data_path, f) for f in os.listdir(raw_data_path) if f.startswith("enwiki")]
wikipedia_file = os.path.join(raw_data_path, "enwiki-20190701-pages-articles.xml.bz2")

buffer_size = 8  # Adjust this according to how "memory efficient" you need the program to be.

with open(wikipedia_file, 'wb') as dest_file:
    for file_name in wikipedia_files:
        with open(file_name, 'rb') as source_file:
            chunk = True
            while chunk:
                chunk = source_file.read(buffer_size)
                dest_file.write(chunk)

#%% MODIFY WIKIPEDIA DUMP FILES
subprocess.call(["python", "./src/wiki_extractor/WikiExtractor.py", "-o", processed_data_path, wikipedia_file])

#%% 
