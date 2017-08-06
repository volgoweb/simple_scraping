from bs4 import BeautifulSoup
import requests

class LifehackerCountCommentsParser(object):
    BASE_URL = 'https://lifehacker.com/tag/how-i-work'
    PER_PAGE = 20
    MAX_PAGES = 5

    def run(self, update_state_func):
        self.found_article_comments = {}
        i = 0
        while i < self.MAX_PAGES:
            i += 1
            progress_percent = int(float(i * 100) / self.MAX_PAGES)
            update_state_func(state='PENDING', meta={
                'current': progress_percent,
                'total': self.MAX_PAGES,
                'status': 'Parsing...',
            })
            page_content = self._get_page_content()
            if not page_content:
                break
            self._parse_content(page_content)
            print(self.found_article_comments)
        update_state_func(state='FINISH', meta={
            'current': self.MAX_PAGES,
            'total': self.MAX_PAGES,
            'status': 'Finish.',
        })
        return list(self.found_article_comments.items())

    def _parse_content(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        tiles = soup.find_all('div', {'class': 'post-wrapper'}, recursive=True)
        for tile in tiles:
            article_title_el = tile.find('a', {'class': 'js_entry-link'}, recursive=True)
            go_to_comments_link_el = tile.find('a', {'class': 'meta__data--comment'}, recursive=True)
            comments_count_el = go_to_comments_link_el.find('span', {'class': 'text'}, recursive=True)
            try:
                comments_count = int(comments_count_el.text)
            except ValueError:
                comments_count = None
            self.found_article_comments[article_title_el.text] = comments_count

    def _get_current_page_number(self):
        self._page_number = getattr(self, '_page_number', 0) + 1
        print('page:', self._page_number)
        return self._page_number

    def _get_page_content(self):
        startindex = self._get_current_page_number() * self.PER_PAGE
        params = {
            'startindex': startindex,
        }
        # response = requests.get(''.format(self.BASE_URL, startindex), params=params)
        response = requests.get('{}?startindex={}'.format(self.BASE_URL, startindex))
        return response.content
