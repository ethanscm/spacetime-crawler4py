import re
from urllib.parse import urlparse, urldefrag, urljoin
from bs4 import BeautifulSoup
import tokenizer
from SimHash import SimHash
from text_tracker import *


class dup_url:
    setOfURLs = set()

def scraper(url, resp):
    links = extract_next_links(url, resp)
    addToUniquePages(url)       # added
    return [link for link in links if is_valid(link)]

class SimHashObj:
    simHash = SimHash(0.9)

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    
    # implement:
    #   BeautifulSoup/lxml to parse
    #   Get all the Question info here maybe?
    #       insert website similarity hashing here (so comparision is possible)
    #       page length + common words recorded here
    #       
    #   relative -> absolute URLs

    next_links = list()

    # i added this garbage
    if resp.status == 200:
        #   fetching hyperlinks/urls
        #       find_all = returns list with all lines matching parameters
        #resp.raw_response.content
        soup = BeautifulSoup(resp.raw_response.content, 'html.parser') #resp.url = requests.get(url)

        #create a word frequency list of all words in the current page
        text = soup.get_text()
        tokens = tokenizer.tokenize(text)
        frequencies = tokenizer.computeWordFrequencies(tokenizer.remove_stopwords(tokens))

        #   checks if webpage being scraped is within 90% similarity of existing pages
        #       If true, we just dont analyze it
        if SimHashObj.simHash.similar(frequencies) == True:
            return next_links

        #update the current frequency totals amongst all pages. Track the longest page.
        if(len(tokens) > text_tracker.longest_page[1]):
            text_tracker.longest_page = (url, len(tokens))
            lp_file = open("longest_page.txt", "w")
            lp_file.write(f"({url}, {len(tokens)})")
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



# change this
def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.

    # implement:
    #   look for traps
    #   look for similar pages
    #       write something to detect similar URLs and/or similar webpage contents??
    #           ex: webpages sharing url (disregard fragment part)
    #   look for empty pages
    #   look for big files that do nothing

    

    try:
        url = urldefrag(url)        # edited - takes url parameter and removes the fragment (#aaa, #bbb part)
        parsed = urlparse(url[0])   # edited - url[0] is new url without fragment (so it's counted as one website)

        if parsed.scheme not in set(["http", "https"]):
            return False

        # NEW
        # Checks if URL is in valid domain (one of the four domains - ics, cs, informatics, stat)
        if not re.search('\.ics\.uci\.edu|\.cs\.uci\.edu|\.informatics\.uci\.edu|\.stat\.uci\.edu', parsed.netloc):
            return False

        # Checks for duplicate URLs
        if url not in dup_url.setOfURLs:
            dup_url.setOfURLs.add(url)
        else:
            return False
        # ===

        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise


# Added helper function
def addToUniquePages(url):
    # Adds new URL to the uniquePages.txt document if it is valid
    if is_valid(url):
        uniquePage = open('uniquePages.txt', 'a')
        uniquePage.write(f"{url}\n")
        uniquePage.close()

def restoreDupURLs():
    pageFile = open("uniquePages.txt", "r")
    for line in pageFile:
        dup_url.setOfURLs.add(line)
    pageFile.close()