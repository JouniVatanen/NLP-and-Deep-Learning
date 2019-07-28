#%% 
import requests
import os
import fnmatch

def download_url(url, path = "."):
    print("Downloading: ",url)
    # assumes that the last segment after the / represents the file name
    # if url is abc/xyz/file.txt, the file name will be file.txt
    file_name_start_pos = url.rfind("/") + 1
    file_name = os.path.join(path, url[file_name_start_pos:])

    r = requests.get(url, stream=True)
    if r.status_code == requests.codes.ok:
        with open(file_name, 'wb') as f:
            for data in r:
                f.write(data)
    return url

# unfortunately Python 2 and 3 translates work differently
def remove_punctuation_2(s):
    return s.translate(None, string.punctuation)

def remove_punctuation_3(s):
    return s.translate(str.maketrans('', '', string.punctuation))

if sys.version.startswith('2'):
    remove_punctuation = remove_punctuation_2
else:
    remove_punctuation = remove_punctuation_3

def my_tokenizer(s):
    s = remove_punctuation(s)
    s = s.lower() # downcase
    return s.split()

#%%
def get_wikipedia_data(path = "."):
    print("")

    # Get filenames in a list
    wiki_files = []
    for root, dirnames, filenames in os.walk(os.path.normpath(path)):
        for filename in fnmatch.filter(filenames, "wiki*"):
            wiki_files.append(os.path.join(root, filename))
    
    output = wiki_files[0:10]
    
    # Read files
    for f in output:
        print("Reading: f")
        for line in open(f):
            line = line.strip


    return(output)


#%%
test = get_wikipedia_data("./data/processed/")



#%%
