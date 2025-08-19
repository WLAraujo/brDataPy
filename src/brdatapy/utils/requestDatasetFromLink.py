import requests

class requestDatasetFromLink():
    """Classe que contém sessão usada para obtenção de um dataset via link usando o pacote requests.
    A origem do link pode levar a um download direto de arquivo ou a um endpoint de API. 
    """

    def __init__(necessita_autenticacao=False, c):
        self.autenticacao