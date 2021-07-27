from src.webdriver import BrowserDriver
from pytest import fixture


@fixture(params=['chrome', 'edge'], scope='class')
def browser(request):
    request.cls.browser = BrowserDriver(browser=request.param)
    yield
    request.cls.browser.close_browser()
