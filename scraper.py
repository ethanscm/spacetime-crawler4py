import re
from urllib.parse import urlparse, urldefrag, urljoin
from bs4 import BeautifulSoup
import tokenizer
from SimHash import SimHash
from text_tracker import *

# Create an empty set to hold all the unique URLs when crawling
class dup_url:
    setOfURLs = set()


def scraper(url, resp):
    links = extract_next_links(url, resp)
    addToUniquePages(url)       # added
    valid_urls = [link for link in links if is_valid(link)]
    return valid_urls


class SimHashObj:
    simHash = SimHash(0.95)


def extract_next_links(url, resp):
    next_links = list()

    if resp.status == 200:
        soup = BeautifulSoup(resp.raw_response.content, 'html.parser')

        #create a word frequency list of all words in the current page
        text = soup.get_text()
        tokens = tokenizer.tokenize(text)
        frequencies = tokenizer.computeWordFrequencies(tokenizer.remove_stopwords(tokens))

        #   checks if webpage being scraped is within 90% similarity of existing pages
        #       If true, we just dont analyze it
        if SimHashObj.simHash.similar(frequencies) == True:
            return next_links

        #update the current frequency totals amongst all pages. Track the longest page.
        if(len(tokens) > 10000 or len(tokens) > text_tracker.longest_page[1]):
            text_tracker.longest_page = (url, len(tokens))
            lp_file = open("longest_page.txt", "a")
            lp_file.write(f"({url}, {len(tokens)})\n")
            lp_file.close()
            
        for t in frequencies:
            if t not in text_tracker.all_words:
                text_tracker.all_words[t] = frequencies[t]
                text_tracker.tokens.append(t)
            else:
                text_tracker.all_words[t] += frequencies[t]

        #save current frequencies
        freq_text = open('frequency.txt', 'w')
        freq_text.write(f"{text_tracker.all_words}\n")
        freq_text.close()
                    
        for link in soup.find_all('a', href=True):
            next_links.append(link['href'])
    else:
        if resp.status/100 == 3:
            soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
            for link in soup.find_all('a', href=True):
                next_links.append(link['href'])
        else:
            print(resp.error)

    #turn relative urls into absolute
    # [Ethan] defragment the urls here instead of in is_valid
    for i in range(len(next_links)):
        potential_url = urljoin(url, next_links[i])
        potential_url = urldefrag(potential_url)
        next_links[i] = potential_url[0]

    return next_links



def is_valid(url):
    try:
        # Takes url parameter and removes fragment part of URL, then parse through the defragmented URL to ensure 
        # it is only counted as one website
        url = urldefrag(url)
        parsed = urlparse(url[0])

        if parsed.scheme not in set(["http", "https"]):
            return False

        # Checks if URL is in valid domain (one of the four domains - ics, cs, informatics, stat)
        if not re.search('\.ics\.uci\.edu|\.cs\.uci\.edu|\.informatics\.uci\.edu|\.stat\.uci\.edu', parsed.netloc):
            return False

        # Checks for duplicate URLs
        if url not in dup_url.setOfURLs:
            dup_url.setOfURLs.add(url)
        else:
            return False

        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz"
            + r"|pdf|png|ppsx|json|ma)$", parsed.path.lower()) #more file formats to avoid crawling

    except TypeError:
        print ("TypeError for ", parsed)
        raise


# Added helper function - Adds new URL to the uniquePages.txt document if it is valid
def addToUniquePages(url):
    uniquePage = open('uniquePages.txt', 'a')
    uniquePage.write(f"{url}\n")
    uniquePage.close()

# In the event the server crashes during a crawl, this function restores the setOfURLs variable and re-adds all
# existing URLs that were already crawled and added to the uniquePages.txt file
def restoreDupURLs():
    pageFile = open("uniquePages.txt", "r")
    for line in pageFile:
        dup_url.setOfURLs.add(line)
    pageFile.close()