from abc import ABC, abstractmethod
from io import StringIO

class AcquisitonStrategy(ABC):
    """Classe abstrata usada para definir a interface comum que as estratégias concretas de obtenção de dados devem seguir.
    A escolha da estrátegia concreta baseia-se no parâmetro "forma_obtencao_dataset" que deve estar contido no arquivo yaml de metadados.
    Os métodos contido na estratégia de aquisição são diversos utilitários para obtenção do dataset no formato especificado no arquivo de metadados.
    """

    def __init__(self, metadados_dataset:dict):
        """Método inicializador da estratégia de aquisição do dataset que cria um atributo dicionário com metadados do dataset.

        Args:
            metadados_dataset (dict): Dicionário com todos os metadados do dataset que estão contidos no yaml de configuração.
        """
        self.metadados_dataset = metadados_dataset

    @property
    @abstractmethod
    def metadados_obrigatorios(self)->set:
        """Propriedade que obrigatóriamente deve existir em cada classe concreta e que implementa uma estratégia concreta de obtenção de dados.
        Deve retornar 
        """
        pass

    @abstractmethod
    def obter_dados(self)->StringIO:
        """Método abstrato usado para obter os dados de um dataset. Cada estratégia de obtenção dos dados deve aplicar uma forma específica para obtenção.
        Por padrão as estratégias concretas devem retornar os dados como um StringIO para viabilizar o tratamento do dataset em memória.
        """
        pass

    @abstractmethod
    def _validar_metadados(self)->bool:
        """Método abstrato oculto usado para validar se o arquivo yaml de configuração do dataset possui todos os metadados necessários para o tipo de obtenção dos dados especificado.

        Returns:
            bool: Se o arquivo yaml de metadados do dataset conter todos os metadados necessários para a forma de aquisição retorna True, caso contrário retorna False.
        """
        pass