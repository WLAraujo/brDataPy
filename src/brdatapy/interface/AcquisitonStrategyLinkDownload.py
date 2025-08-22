from brdatapy.interface.AcquisitonStrategy import AcquisitonStrategy
import requests
from io import StringIO

class AcquisitonStrategyLinkDownload(AcquisitonStrategy):

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
        response = requests.get(self.url_link_download)
        response.raise_for_status()
        data = StringIO(response.text)
        return data

    def _validar_metadados(self)->bool:
        """Método privado que valida se o arquivo yaml de metadados do dataset contém todos os metadados necessários para o tipo específico de estratégia de obtenção de dados.

        Returns:
            bool: Caso os metadados obrigatórios estejam contidos no arquivo yaml de metadados retorna True, caso contrário retorna False.
        """
        if self.metadados_obrigatorios.issubset(self.metadados_dataset.keys()):
            return True
        else:
            return False
