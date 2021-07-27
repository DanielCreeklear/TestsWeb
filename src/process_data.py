# -*- coding: utf-8 -*-
import json


def get_json(file_path):
    """
        Faz a leitura de um arquivo Json com codificacao utf-8,
        apenas para arquivos dentro do diretorio folhacerta_settings

        :param file_path: (string) nome do arquivo json com extensao
        :return: Dicionario com os dados do json
    """
    with open(file_path, encoding='utf-8') as data_json:
        return json.load(data_json)
