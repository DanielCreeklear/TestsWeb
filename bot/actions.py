from src.process_data import get_json


class Actions:
    """
        General actions for bot
    """

    def __init__(self, browser):
        """
            :param browser: Object BrowserChrome or BrowserEdge
        """
        self.browser = browser

    def access_google(self):
        """
            Redirects browser to google site
        """
        self.browser.to_url(get_json('../maps/urls.json')['google-main'])

    def click_in_html(self):
        html = self.browser.get_element(by='xpath', path='html')
        return self.browser.click_element(html)

    def research(self, text):
        """
            Search on google
        """
        steps = [
            self.write_in_search_field(text),
            self.click_in_html(),
            self.run_search()
        ]

        if False in steps:
            return False
        else:
            return True

    def write_in_search_field(self, text):
        bar = self.browser.get_element(by='css', path='input[type="text"]')
        return self.browser.write_in_element(bar, text)

    def run_search(self):
        bar = self.browser.get_element(by='css', path='input[type="text"]')
        steps = [
            self.browser.click_keyboard(bar, 'baixo'),
            self.browser.click_keyboard(bar, 'enter')
        ]
        if False in steps:
            return False
        else:
            return True
