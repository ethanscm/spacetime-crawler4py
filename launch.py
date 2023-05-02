from configparser import ConfigParser
from argparse import ArgumentParser

from utils.server_registration import get_cache_server
from utils.config import Config
from crawler import Crawler

from scraper import restoreDupURLs
from text_tracker import *


def main(config_file, restart):
    cparser = ConfigParser()
    cparser.read(config_file)
    config = Config(cparser)
    config.cache_server = get_cache_server(config, restart)
    crawler = Crawler(config, restart)

    #restore data back to the classes
    #comment it out if you are restarting
    #load_old_data()

    crawler.start()
    t50 = text_tracker.get_top_fifty(text_tracker.tokens)
    print("Top 50 Words")
    for t in range(50):
        print(f'{t}) {t50[t]} -> {text_tracker.all_words[t50[t]]}')

def load_old_data():
    text_tracker.restore_data()
    restoreDupURLs()
    text_tracker.restore_longest_page()

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--restart", action="store_true", default=True)
    parser.add_argument("--config_file", type=str, default="config.ini")
    args = parser.parse_args()
    main(args.config_file, args.restart)
