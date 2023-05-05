# Checks every URL in uniquePages.txt - first counts the number of unique pages there are, then
# counts number of subdomains in ics.uci.edu domain, makes a list of subdomains in alphabetical order,
# and displays the number of unique pages detected in each subdomain.

# Import statements
from collections import defaultdict
from urllib.parse import urlparse
import re

# ============= Question 1 =============

# Set of visited URLs (prevents there from being duplicates)
setOfPages = set()

# Adds every URL to the setOfPages
uniquePages = open("uniquePages.txt")
for line in uniquePages:
    setOfPages.add(line)

# Prints number of unique pages found
print("Number of unique pages found:", len(setOfPages))

# ============= Question 4 =============

# List of tuples containing URL and number of unique pages
subdomainsAndPages = list()

# default dict with key = domain + subdomain, val = num of unique pages
subdomainsDict = defaultdict(int)

# Checks if URL is within ics.uci.edu domain, and if it is, adds it to defaultdict 
# (or adds one for unique page to existing key)
for url in setOfPages:
    parsed = urlparse(url)
    if re.search('\.ics\.uci\.edu', parsed.netloc):
        subdomain = parsed.netloc.split('.')[0]
        subdomainsDict[subdomain] += 1

# Iterates through each key,val in subdomainsDict and adds it to the subdomainsAndPages list in the form of
# a tuple - (URL, number of unique pages)
for key,val in subdomainsDict.items():
    subdomainsAndPages.append((f"https://{key.lower()}.ics.uci.edu",val))

subdomainsAndPages.sort(key = lambda x : x[0])      # sorts list alphabetically 

# Counts number of subdomains in ics.uci.edu domain and prints value
print("Number of subdomains in ics.uci.edu domain:", len(subdomainsAndPages))

# Prints list of subdomains ordered alphabetically and number of unique pages detected in that subdomain
for sub in subdomainsAndPages:
    print(f"{sub[0]}, {sub[1]}")