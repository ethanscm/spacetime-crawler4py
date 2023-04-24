import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

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
        with open(url) as file:
            #resp.raw_response.content
            soup = BeautifulSoup(resp.raw_response.content, 'html.parser') #resp.url = requests.get(url)
        for link in soup.find_all('a', href=True):
            next_links.append(link['href'])

        
    else:
        #
        print(resp.error) #do something
    # garbage ends here 

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
        parsed = urlparse(url)
        defrag_url = urlparse.urldefrag(url)[0] #added

        if parsed.scheme not in set(["http", "https"]):
            return False
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
