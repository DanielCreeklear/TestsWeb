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
        self.time_limit_expected = 10

    def access_google(self):
        """
            Redirects browser to google site
        """
        self.browser.to_url(get_json('../maps/urls.json'))

