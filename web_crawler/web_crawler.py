import requests
import queue
from bs4 import BeautifulSoup
from dateutil import parser
from munch import Munch
from tinydb import TinyDB, Query
import time

from web_crawler import consts


class WebCrawler(object):

    def __init__(self, logger):
        self.url_queue = queue.Queue()
        self.db_queue = queue.Queue()
        self.db = TinyDB('pastebin_db.json')
        self.logger = logger

    def main(self):
        while True:
            self.fetch_urls()
            self.write_to_db()
            self.logger.info("sleeping")
            time.sleep(consts.TIME_TO_SLEEP)

    def fetch_urls(self):
        self.keys = set()
        soup = self._get_page_soup(consts.RECENT_PASTES_URL)
        recent_pastes_table = soup.find(
            "table", {"class": consts.TABLE_CLASS_NAME}
            )
        for table_row in recent_pastes_table.childGenerator():
            url_postfix = table_row.find("a")
            if url_postfix and url_postfix != -1:
                paste_id = url_postfix["href"]
                self.keys.add(paste_id)
                self.logger.info("Added %s to keys", paste_id)

    def write_to_db(self):
        for paste_id in self.keys:
            if not self._paste_in_db(paste_id):
                self.logger.info("Handling %s", paste_id)
                paste_url = "%s%s" % (consts.BASE_PASTEBIN_URL, paste_id)
                paste_soup = self._get_page_soup(paste_url)
                paste_info = paste_soup.find(
                    "div", {"class": consts.PASTE_INFO_CLASS}
                    )
                if not paste_info:
                    raise RuntimeError("IP was blocked by pastebin")
                title = self._get_paste_title(paste_info)
                author = self._get_paste_author(paste_info)
                date = self._get_date(paste_info)
                content = self._get_content(paste_soup)
                paste_object = Munch(id=paste_id,
                                     Title=title,
                                     Author=author,
                                     Date=date,
                                     Content=content
                                     )
                self.db.insert(paste_object)
                self.logger.info("Added %s to db", paste_id)
            else:
                self.logger.info("%s already in db", paste_id)

    def _paste_in_db(self, paste_id):
        Paste = Query()
        return bool(self.db.search(Paste.id == paste_id))

    def _get_page_soup(self, url):
        page = requests.get(url).text
        return BeautifulSoup(page, 'html.parser')

    def _get_paste_title(self, paste_info):
        title = paste_info.find("h1").text
        if title in consts.TITLES_TO_NORMALIZE:
            title = ""
        return title

    def _get_paste_author(self, paste_info):
        second_info_line = paste_info.find(
            "div", {"class": consts.PASTE_BOX_SECOND_LINE}
            )
        name_holder = second_info_line.find("a")
        if name_holder:
            return name_holder.text
        return ""

    def _get_date(self, paste_info):
        date = paste_info.find("span")
        normalized_date = parser.parse(date["title"], tzinfos={"CDT": "UTC-5"})
        return normalized_date.strftime(consts.TIME_FORMAT)

    def _get_content(self, paste_soup):
        content = paste_soup.find("textarea").text
        return content.rstrip()
