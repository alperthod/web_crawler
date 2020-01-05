import logging

from web_crawler.web_crawler import WebCrawler


def main():
    logging.basicConfig(filename='web_crawler.log',
                        filemode='w',
                        format='%(asctime)s- %(levelname)s - %(message)s',
                        level=logging.DEBUG)
    logging.info("testttt")
    logger = logging.getLogger('web_crawler')
    web_crawler = WebCrawler(logger)
    try:
        web_crawler.main()
    except Exception:
        logging.error("Exception occurred", exc_info=True)


if __name__ == "__main__":
    main()
