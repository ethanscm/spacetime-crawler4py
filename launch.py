from configparser import ConfigParser
from argparse import ArgumentParser

from utils.server_registration import get_cache_server
from utils.config import Config
from crawler import Crawler

from scraper import restoreDupURLs, SimHashObj
from text_tracker import *


def main(config_file, restart):
    cparser = ConfigParser()
    cparser.read(config_file)
    config = Config(cparser)
    config.cache_server = get_cache_server(config, restart)
    crawler = Crawler(config, restart)

    #restore data back to the classes
    #comment it out if you are restarting
    load_old_data()

    crawler.start()
    
    top_tokens = text_tracker.get_top_tokens(text_tracker.tokens, 200)
    top_txt = open("top.txt", 'a')
    print("Top Tokens")
    for t in range(200):
        print(f'{t+1}) {top_tokens[t]} -> {text_tracker.all_words[top_tokens[t]]}')
        top_txt.write(f'{t+1}) {top_tokens[t]} -> {text_tracker.all_words[top_tokens[t]]}\n')
    top_txt.close()

def load_old_data():
    text_tracker.restore_data()
    restoreDupURLs()
    text_tracker.restore_longest_page()
    SimHashObj.simHash.restore_simhashes()

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--restart", action="store_true", default=False)
    parser.add_argument("--config_file", type=str, default="config.ini")
    args = parser.parse_args()
    main(args.config_file, args.restart)
