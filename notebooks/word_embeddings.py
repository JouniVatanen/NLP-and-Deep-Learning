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

#%% DOWNLOAD WIKIPEDIA DUMP FILES
# Add a path to download files from url script
raw_data_path = os.path.normpath("./data/raw")

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

#%% MODIFY WIKIPEDIA DUMP FILES
wikipedia_files = [os.path.join(raw_data_path, f) for f in os.listdir(raw_data_path) if f.startswith("enwiki")]
processed_data_path = os.path.normpath("./data/processed")

# Loop all wikipedia dump files
for f in wikipedia_files:
	# Check loop situation
	print("Processing file: " + f)
	subprocess.call(["python", "./src/WikiExtractor.py", "-o", processed_data_path, f])
	# Create a single file and remove extracted files
	output_file = os.path.splitext(f)[0] + ".txt"
	print("Create single file: " + output_file)
	subprocess.call(["find", processed_data_path, "-name", "'*bz2'", "-exec", "bzip2", "-c", "{}", "\;", ">", output_file])
	subprocess.call(["rm", "-rf", processed_data_path + "/*/"]) 

#%%
subprocess.call(["rm", "-rf", os.path.join(processed_data_path, "/*/")]) 


#%%
