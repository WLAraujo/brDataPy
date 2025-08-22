from abc import ABC, abstractmethod
from pathlib import Path
import inspect
import yaml
from brdatapy.interface.AcquisitonStrategy import AcquisitonStrategy
from brdatapy.interface.FormatStrategy import FormatStrategy
from brdatapy.interface.AcquisitonStrategyLinkDownload import AcquisitonStrategyLinkDownload

class DatasetFactory(ABC):
    """Classe abstrata que define a interface que as classes que implementam datasets devem implementar e estabelece métodos comuns para todas as classes concretas que de fato implementam os datasets.
    """

    def __init__(self):
        """Método inicializador de todo dataset do projeto.
        Esse método define dois dos pontos mais importantes para todo dataset: como o dataset será obtido e como ele será tratado devido ao seu formato.
        Também são feitas validações dos metadados.
        """
        metadados_obrigatorios = {"formato_dataset", "forma_obtencao_dataset", "descricao_dataset", "tags_dataset"}
        if not metadados_obrigatorios.issubset(self.metadados_dataset.keys()):
            raise Exception(f"Um dos metadados obrigatórios para todo dataset não foi encontrado no arquivo yaml de metadados. Favor entrar em contato com o time de desenvolvimento.")
        self.estrategia_forma_obtencao = self._definir_estrategia_obtencao()
        self.estrategia_formato = self._definir_estrategia_formato()
        self._validar_metadados_dataset()

    @property
    def arquivo_metadados_dataset(self)->str:
        """Método que retorna atributo constante para todos os dataset, o nome do arquivo yaml de metadados: dataset_metadata.yaml

        Returns:
            str: Retorna o nome do arquivo.
        """
        return "dataset_metadata.yaml"

    @property
    def path_arquivo_metadados(self)->Path:
        """Método que retorna o caminho do arquivo yaml em que estão contidos metadados do dataset.
        O método retorna um Path com o caminho para o arquivo de metadados do dataset.

        Returns:
            Path: Path completo do arquivo yaml que contém os metadados do dataset.
        """
        arquivo = inspect.getfile(self.__class__)
        return Path(arquivo).parent / self.arquivo_metadados_dataset        

    @property
    def metadados_dataset(self)->dict:
        """Método que faz a leitura das propriedades do dataset contidas no arquivo yaml padronizado de metadados. 
        O método retorna os metadados como um dicionário, sendo uma propriedade de cada classe concreta que implementa um dataset.

        Returns:
            dict: Dicionário com informações do arquivo yaml padrão com metadados do dataset.
        """
        with open(self.path_arquivo_metadados, 'r') as file:
            metadados_dataset = yaml.safe_load(file)
        return metadados_dataset
    
    @property
    def tags_dataset(self)->list:
        """Método que retorna todas as tags associadas ao dataset via arquivo de metadados.
        Retorna uma lista com todas as tags que estejam na lista tags_dataset do yaml.

        Returns:
            list: Lista de tags associada ao dataset pelo parâmetro tags_dataset do yaml de metadados.
        """
        return self.metadados_dataset["tags_dataset"]
    
    @property
    def descricao_dataset(self)->str:
        """Método que retorna a descrição do dataset contida no arquivo de metadados.
        Retorna a descrição do dataset que está contida no atributo descricao_dataset do yaml.

        Returns:
            str: Descrição do dataset definida pelo parâmetro descricao_dataset do yaml de metadados.
        """
        return self.metadados_dataset["descricao_dataset"]
    
    @property
    def forma_obtencao_dataset(self)->str:
        """Método que retorna a forma de obtenção do dataset, informação com origem no arquivo de metadados.
        Retorna a informação contida no parâmetro forma_obtencao_dataset do yaml de metadados.

        Returns:
            str: Forma de obtenção do dataset obtida do arquivo de metadados.
        """
        return self.metadados_dataset["forma_obtencao_dataset"]
    
    @property
    def formato_dataset(self)->str:
        """Método que retorna o formato do dataset, informação com origem no arquivo de metadados.
        Retorna a informação contida no parâmetro formato_dataset do yaml de metadados.

        Returns:
            str: Formato do dataset obtido do arquivo de metadados.
        """
        return self.metadados_dataset["formato_dataset"]

    @abstractmethod
    def obter_schema(self):
        """Método abstrato em que cada classe de factory específica deve implementar uma forma de obter o schema do dataset considerando os metadados do dataset obtidos.
        """
        pass

    def _definir_estrategia_obtencao(self):
        """Método abstrato usado para decidir qual será a estrátegia de obtenção do datasets.
        """
        if self.forma_obtencao_dataset == "download_link":
            return AcquisitonStrategyLinkDownload(self.metadados_dataset)
        else:
            raise Exception(f"Forma de obtenção {self.forma_obtencao} não existe, se deseja sugerir uma nova forma de obtenção de datasets entre em contato com a equipe de desenvolvimento.")

    def _definir_estrategia_formato(self):
        """Método abstrato usado para decidir qual será a estrátegia para tratar o formato de dataset.
        """
        if self.formato_dataset == "csv":
            pass
        else:
            raise Exception(f"Forma de obtenção {self.formato_dataset} não existe, se deseja sugerir uma nova forma de obtenção de datasets entre em contato com a equipe de desenvolvimento.")

    def _validar_metadados_dataset(self):
        """Método privado em que cada classe de factory específica deve implementar uma forma de validar os metadados do dataset para o tipo específico formato ou forma de obtenção.
        Caso os metadados do dataset não sejam coerentes com a forma de obtenção 
        """
        pass
        #if (not self.estrategia_forma_obtencao._validar_metadados()) or (self.estrategia_formato._validar_metadados()):
        #    raise Exception("Metadados contidos no arquivo são inválidos para o formato do dataset ou o tipo de obtenção. Favor entrar em contato com time de desenvolvimento para corrigir problemas no arquivo de metadados.")