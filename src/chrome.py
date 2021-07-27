# -*- coding: utf-8 -*-
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from os.path import dirname, realpath
from time import strftime, sleep, time


class BrowserChrome:
    """
        Abre navegador chrome, possui todos os comandos para o chrome

        methods:
            go_to_url(url)
            get_url(url)
            console_log()
            count_error_console()
            get_element_xpath(screen, element)
            write_in_element(web_element, text)
            click_element(web_element)
            get_content(web_element)
            await_switch_url(current_url)
    """

    KEYS_KEYBOARD = {
        'esquerda': Keys.ARROW_LEFT,
        'baixo': Keys.ARROW_DOWN,
        'enter': Keys.ENTER,
        'cima': Keys.ARROW_UP,
        'home': Keys.HOME
    }

    def __init__(self, xpath):
        """
            Construtor da classe

            Attributes:
                dir_path(str): Caminho atual do arquivo, onde esta sendo executado
                __path_webdriver(str): Caminho para o chromedriver
                __initialized(str): Data+hora que foi invocado o script
                browser(Chrome): Webdriver
                seconds_to_except(int): Tempo em segundos para gerar excecao em caso de algum erro
                console_log(list): Contem o log do console obtido durante a execucao
        """

        self.dir_path = dirname(realpath(__file__))
        self.versions_chrome = ['89_0_4389_23', '91_0_4472_19']
        self.used_version_chrome = self.versions_chrome[1]
        self.__path_webdriver = self.dir_path + '/webdrivers/chromedriver_' + self.used_version_chrome + '.exe'
        self.__initialized = strftime('%X %x')
        self.browser = Chrome(executable_path=self.__path_webdriver, options=self.__get_options())
        self.xpath = xpath
        self.seconds_to_except = 6
        self.console_log = []

    def to_url(self, url, wait=0):
        """
            Acessa o url passado, verifica se houve algum erro para
            acessar e retorna quantidade de erros gerados ao acessar
            o link.

            :return: Quantidade de erros ou -1 em caso de exception
        """
        try:
            self.browser.get(url)
            sleep(wait)

        except InvalidArgumentException:
            print('Existem problemas com a URL')

            if 'https://' not in url:
                self.to_url('https://' + url)

        except WebDriverException:
            print('A URL está quebrada: ', url)

        except ValueError:
            print('O valor para espera está errado: ', wait)

        else:
            return self.count_error_console()

    def get_url(self):
        """
            Obtem o atual url.

            :return: Url atual da aba
        """

        return self.browser.current_url

    def get_console_log(self):
        """
            Obtem o log do console do navegador

            :return: lista com logs do consoles
        """

        return [log for log in self.browser.get_log('browser')]

    def count_error_console(self):
        """
            Conta a quantidade de erros graves que aconteceram no navegador

            :return: Quantidade de erros graves
        """

        errors = 0
        self.console_log = self.get_console_log()
        for console_log in self.console_log:
            if console_log['level'] == 'SEVERE':
                errors += 1
        return errors

    def get_element_xpath(self, element):
        """
            Recupera um elemento presente na tela, atraves do xpath

            :return: web_element
        """

        try:
            element_present = ec.presence_of_element_located((By.XPATH, element))
            web_element = WebDriverWait(driver=self.browser, timeout=self.seconds_to_except).until(element_present)

        except TimeoutException:
            print(f'O elemento {element} não apareceu em {self.seconds_to_except} segundos!')
            return self.browser.find_element_by_xpath('html')

        else:
            return web_element

    def get_element_map(self, element):
        """
            Recupera um elemento presente na tela, atraves do mapeamento feito via json

            :return: web_element
        """

        try:
            screen = self.get_url()
            if '/' in element:
                element_present = ec.presence_of_element_located((By.XPATH, self.xpath[screen][element.split('/')[0]][element.split('/')[1]]))
                web_element = WebDriverWait(driver=self.browser, timeout=self.seconds_to_except).until(element_present)
            else:
                element_present = ec.presence_of_element_located((By.XPATH, self.xpath[screen][element]))
                web_element = WebDriverWait(driver=self.browser, timeout=self.seconds_to_except).until(element_present)

        except TimeoutException:
            print(f'O elemento {element} não apareceu em {self.seconds_to_except} segundos!')
            return self.browser.find_element_by_xpath('html')

        else:
            return web_element

    def get_css(self, element):
        """
            Recupera um elemento presente na tela, atraves do css selector

            :return: web_element
        """

        try:
            element_present = ec.presence_of_element_located((By.CSS_SELECTOR, element))
            web_element = WebDriverWait(driver=self.browser, timeout=self.seconds_to_except).until(element_present)

        except TimeoutException:
            print(f'O elemento {element} não apareceu em {self.seconds_to_except} segundos!')
            return self.browser.find_element_by_xpath('html')

        else:
            return web_element

    def get_element(self, path, by):
        """
            Recupera o elemento na tela de acordo com o tipo de consulta

        :param path: String - O caminho para o elemento
        :param by: String - Tipo de consulta para encontrar o elemento
        :return: web_element
        """
        element = {
            'xpath': self.get_element_xpath,
            'map': self.get_element_map,
            'css': self.get_css
        }
        return element[by](path)

    @staticmethod
    def write_in_element(web_element, text, before_clear=True):
        """
            Escreve no objeto do web element caso ele seja encontrado

            :return: True caso encontre, False caso nao encontre
        """

        try:
            if before_clear:
                web_element.send_keys(Keys.CONTROL + 'a')
                web_element.send_keys(Keys.DELETE)
            web_element.send_keys(text)
        except Exception as execption:
            print('Não foi possível escrever [{}]'.format(text))
            print(Exception)
            print(execption)
            return False
        else:
            return True

    def click_keyboard(self, web_element, arrow):
        """
            Clica na seta do teclado dentro do web element

            :return: True caso encontre, False caso nao encontre
        """

        try:
            web_element.send_keys(self.KEYS_KEYBOARD[arrow])

        except ElementNotInteractableException:
            print('Não foi possível usar o teclado no elemento!')
            return False

        else:
            return True

    def click_element(self, web_element):
        """
            Clica no objeto do web elemento caso ele seja encontrado

            :return: True caso encontre, False caso nao encontre
        """

        try:
            start = time()
            while ec.element_to_be_clickable(web_element) is False:
                web_element.location_once_scrolled_into_view()
                try_click_time_fail = time()
                if try_click_time_fail - start > self.seconds_to_except:
                    break
            else:
                web_element.click()

        except ElementNotInteractableException:
            print('Não foi possível clicar no elemento!')
            return False

        except ElementClickInterceptedException:
            return False

        else:
            return True

    def set_page_to_up(self):
        """
            Vai ate o topo da página com a tecla HOME do teclado.
        """

        html = self.browser.find_element_by_tag_name('html')
        html.send_keys(self.KEYS_KEYBOARD['home'])
        sleep(1)

    def scroll_page(self, direction, steps):
        """
            Realiza o scroll da página utilizando o teclado, quantas vezes forem solicitadas.
            direções: cima ou baixo
        """
        html = self.browser.find_element_by_tag_name('html')
        for step in range(steps):
            html.send_keys(self.KEYS_KEYBOARD[direction])
        sleep(1)

    def get_content(self, web_element):
        """
            Obtem o texto do web element caso ele seja encontrado

            :return: String caso encontre, False caso não encontre
        """

        try:
            start = time()
            while web_element.text == '':
                try_time_fail = time()
                if try_time_fail - start > self.seconds_to_except:
                    break
            else:
                return web_element.text
        except Exception as execption:
            print('Não foi possível recuperar o conteúdo [{}]'.format(web_element))
            return False

    def compare_content_element(self, web_element, awaited_text):
        """
            Compara se o conteudo do elemento esta igual ao esperado

            :return: True caso seja igual, False caso nao seja igual, False caso de erro
        """

        try:
            start = time()
            content_equal = False
            content = web_element.text
            while content == '' and not content == awaited_text:
                content = web_element.text
                try_time_fail = time()
                if try_time_fail - start > self.seconds_to_except:
                    break
            else:
                content_equal = True
            return content_equal
        except Exception as execption:
            print('Não foi possível recuperar o conteúdo [{0}] e comparar com o texto [{1}]'.format(web_element, awaited_text))
            return False

    def __get_options(self):
        """
            Obtem as configuracoes para o navegador

            :return: Objeto ChromeOptions com as configuracoes para o navegador
        """

        options = ChromeOptions()
        self.__start_maximized(options=options)
        self.__enable_webcam(options=options)
        return options

    @staticmethod
    def __enable_webcam(options):
        """
            Habilita e permite a webcam ser usada no navegador

            :return: None
        """

        options.add_argument('auto-select-desktop-capture-source')
        options.add_argument('--use-fake-device-for-media-stream')
        # options.add_argument('--use-file-for-fake-video-capture=./webcam002.y4m')
        options.add_experimental_option('prefs', {'profile.default_content_setting_values.media_stream_camera': 1})
        options.add_argument('--allow-http-screen-capture')

    @staticmethod
    def __start_maximized(options):
        """
            Configura o navegador para iniciar maximizado

            :return: None
        """

        options.add_argument('--start-maximized')

    def await_switch_url(self, current_url):
        """
            Espera o navegador trocar a url

            :return: None
        """

        start = time()
        while current_url == self.get_url():
            try_time_fail = time()
            if try_time_fail - start > self.seconds_to_except:
                break
