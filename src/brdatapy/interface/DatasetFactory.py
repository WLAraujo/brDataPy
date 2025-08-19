from abc import ABC, abstractmethod
from pathlib import Path
import inspect
import yaml

class DatasetFactory(ABC):
    """Classe abstrata que define a interface que as classes que implementam datasets devem implementar e estabelece métodos comuns para todas as classes concretas que de fato implementam os datasets.
    """

    arquivo_metadados_dataset = "dataset_metadata.yaml"

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

    @abstractmethod
    def obter_dados(self):
        pass

    @abstractmethod
    def obter_schema(self):
        pass
