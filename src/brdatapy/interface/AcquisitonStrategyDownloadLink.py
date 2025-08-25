from brdatapy.interface.AcquisitonStrategy import AcquisitonStrategy
import requests
from io import StringIO

class AcquisitonStrategyDownloadLink(AcquisitonStrategy):
    """Classe concreta que implementa a estratégia de obtenção de dados quando a forma de obtenção definida no arquivo de metadados for "download_link".
    Essa estratégia concreta obtem os dados do link e armazena o conteúdo obtido em um StringIO para armazenamento em memória.
    """

    @property
    def metadados_obrigatorios(self)->set:
        """Método que retorna os nomes dos metadados obrigatórios para o tipo de obtenção de dataset via download por link.

        Returns:
            set: Conjunto de nomes dos metadados obrigatórios para o tipo de obtenção do dataset.
        """
        return {"formato_dataset", "forma_obtencao_dataset", "descricao_dataset", "tags_dataset"}
    
    @property
    def url_link_download(self)->str:
        """Método que retorna propriedade "link_dataset" dos datasets obtidos via download por link.
        Essa propriedade nada mais é que o link para obter o dataset.

        Returns:
            str: Link para download das informações do dataset.
        """
        return self.metadados_dataset["link_dataset"]

    def obter_dados(self)->StringIO:
        """Método para obtenção do dataset via download pelo link contido nos metadados do datset.
        O método retorna um StringIO visando com que os dados sejam tratados em memória.
        
        Returns:
            StringIO: Arquivo obtido via download por link direto no formato de StringIO.
        """
        request_dataset = requests.get(self.url_link_download)
        try:
            request_dataset.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Falha em obter dados via link passado no arquivo de metadados, favor comunicar a equipe de desenvolvimento para atualizar o link.\nLink: self.url_link_download\nErro: {str(e)}")
        conteudo_dataset = StringIO(request_dataset.text)
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
