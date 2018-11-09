import pandas as pd
import requests

from bs4 import BeautifulSoup

from config.get_config import get_config


class Parser:
    def __init__(self):
        self._config = get_config()['urls']
        self.TREND = self._config['TREND']
        self.CUSTOM = self._config['CUSTOM']

    def get_fields(self, cur_list):
        """
        Rerurn list with video_url, video_name, author_url, author_name
        """
        lists = []
        for ind, element in enumerate(cur_list):
            try:
                video = element.find('h3', class_='yt-lockup-title ').find('a')
                author = element.find('h3', class_='yt-lockup-title ').find('a')
                lists.append({'video_url': video.get('href'),
                     'video_name': video.text,
                     'author_url': author.get('href'),
                     'author_name': author.text
                     })
            except Exception as e:
                print(e)
        return lists

    def parse_trend(self, html):
        soup = BeautifulSoup(html, "html.parser")
        ul = soup.find_all('ul', class_='expanded-shelf-content-list has-multiple-items')[0]
        lists = ul.find_all('li', class_='expanded-shelf-content-item-wrapper')
        lists = [element.find('div', class_='yt-lockup-content') for element in lists]
        return self.get_fields(lists)

    def parse_custom_query(self, html):
        soup = BeautifulSoup(html, "html.parser")
        ol = soup.find('ol', class_='item-section')
        divs = ol.find_all('div', class_='clearfix')

        lists = self.get_fields(divs)
        return lists

    def start_trend(self, trend_filename):
        trend_html = requests.get(self.TREND).text
        result_trend = self.parse_trend(trend_html)
        df = pd.DataFrame(result_trend)
        df.to_csv(trend_filename)

    def start_custom(self, custom_query, custom_filename):
        CUSTOM_URL = self.CUSTOM.format(custom_query)

        custom_html = requests.get(CUSTOM_URL).text
        result_custom = self.parse_custom_query(custom_html)
        df = pd.DataFrame(result_custom)
        df.to_csv(custom_filename)

