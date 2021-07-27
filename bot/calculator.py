from bot.actions import Actions


class Calculator(Actions):
    """
        Calculates with google using a bot with Selenium WebDriver
    """

    def __init__(self, browser):
        """
            :param browser: Object Browser
        """
        super().__init__(browser)
        self.browser = browser

    def calculate(self, input_calculate):
        """Returns the result of the number obtained from google"""
        steps = [
            self.access_google(),
            self.research(input_calculate)
        ]
        result = self.browser.get_element(by='css', path='span[id="cwos"]')
        return self.browser.get_content(result)

