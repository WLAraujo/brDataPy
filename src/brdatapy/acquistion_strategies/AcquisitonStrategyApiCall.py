from brdatapy.acquistion_strategies.AcquisitonStrategy import AcquisitonStrategy
import requests
from io import BytesIO

class AcquisitonStrategyApiCall(AcquisitonStrategy):
    """Classe concreta que implementa a estratégia de obtenção de dados quando a forma de obtenção definida no arquivo de metadados for "api_call".
    Essa estratégia concreta obtem os dados via chamada de API e armazena o conteúdo obtido em um BytesIO para armazenamento em memória.
    """

    def __init__(self, metadados_dataset:dict, parametros_query_api:dict):
        """Método inicializador da estratégia de aquisição do dataset que cria um atributo dicionário com metadados do dataset.
        Esse método é específico para a estratégia de aquisição via chamada de API onde é necessária a criação de alguns outros atributos visando facilitar a chamada de API.

        Args:
            metadados_dataset (dict): Dicionário com todos os metadados do dataset que estão contidos no yaml de configuração.
            parametros_query_api (dict): Dicionário com chaves e valores que serão usados na query de chamada de API. Esse dicionário deve ser definido em cada dataset concreto.
        """
        self.metadados_dataset = metadados_dataset
        self.parametros_query_api = parametros_query_api

    @property
    def metadados_obrigatorios(self)->set:
        """Método que retorna os nomes dos metadados obrigatórios para o tipo de obtenção de dataset via chamada de API.

        Returns:
            set: Conjunto de nomes dos metadados obrigatórios para o tipo de obtenção do dataset.
        """
        return {"formato_dataset", "forma_obtencao_dataset", "descricao_dataset", "tags_dataset", "url_base", "endpoint_requisitado"}
    
    @property
    def url_base_api(self)->str:
        """Método que retorna propriedade "url_base" dos datasets obtidos via chamada de API.
        Essa propriedade é a URL base da API que é usada nas chamadas à API.

        Returns:
            str: URL base da API usada para obter as informações do dataset.
        """
        return self.metadados_dataset["url_base"]
    
    def obter_dados(self)->BytesIO:
        """Método para obtenção do dataset via chamada de API pelo endpoint contido nos metadados do datset.
        O método retorna um BytesIO visando com que os dados sejam tratados em memória.
        Para obtenção de dados via API é necessário que no dataset concreto seja definido o atributo parametros_query, um dicionário python com os parâmetros de query que devem ser adicionados à URL usada na chamada da API. Caso não seja instanciado esse atributo não será passado nenhum parâmetro à chamada de API.
        
        Returns:
            BytesIO: Dados obtidos via chamada de API no formato de BytesIO.
        """
        if self.parametros_query_api == {}:
            endpoint_chamada = f'{self.metadados_dataset["url_base"]}{self.metadados_dataset["endpoint_requisitado"]}'
            resposta_request = requests.get(endpoint_chamada)
        else:
            texto_parametros_query_api = "&".join([f"{parametro}={valor}" for parametro, valor in self.parametros_query_api.items()])
            endpoint_chamada = f'{self.metadados_dataset["url_base"]}{self.metadados_dataset["endpoint_requisitado"]}?{texto_parametros_query_api}'
            resposta_request = requests.get(endpoint_chamada)
        conteudo_dataset = BytesIO(resposta_request.content)
        return conteudo_dataset

    def _validar_metadados(self)->bool:
        """Método privado que valida se o arquivo yaml de metadados do dataset contém todos os metadados necessários para o tipo específico de estratégia de obtenção de dados.

        Returns:
            bool: Caso os metadados obrigatórios estejam contidos no arquivo yaml de metadados retorna True, caso contrário retorna False.
        """
        if self.metadados_obrigatorios.issubset(self.metadados_dataset.keys()):
            return True
        else:
            return False