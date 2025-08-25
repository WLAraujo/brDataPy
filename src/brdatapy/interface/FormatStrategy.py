from abc import ABC, abstractmethod
from io import StringIO

class FormatStrategy(ABC):
    """Classe abstrata usada para definir a interface comum que as estratégias concretas de tratamentos de formatos vão implementar.
    A escolha da estrátegia concreta baseia-se no parâmetro "formato_dataset" que deve estar contido no arquivo yaml de metadados.
    Os métodos contidos na estratégia de formato são diversos utilitários para tratar os dados no formato definido no arquivo de metadados.
    """

    def __init__(self, metadados_dataset:dict, conteudo_dataset:StringIO):
        """Método inicializador da estratégia de formato do dataset que cria um atributo dicionário com metadados do dataset e também um atributo com o conteúdo do dataset em formato StringIO.

        Args:
            metadados_dataset (dict): Dicionário com todos os metadados do dataset que estão contidos no yaml de configuração.
            conteudo_dataset (StringIO): Conteúdo do dataset em memória para ser tratado com os utilitários da estratégia. 
        """
        self.metadados_dataset = metadados_dataset
        self._conteudo_dataset = conteudo_dataset

    @property
    @abstractmethod
    def metadados_obrigatorios(self)->set:
        """Propriedade que obrigatóriamente deve existir em cada classe concreta e que implementa uma estratégia concreta de obtenção de dados.
        Deve retornar 
        """
        pass

    @property
    def conteudo_dataset(self)->StringIO:
        """Propriedade que é inicializada junto com a instância da classe e contém o conteúdo do dataset em formato StringIO.
        """
        return self._conteudo_dataset

    @abstractmethod
    def _validar_metadados(self)->bool:
        """Método abstrato oculto usado para validar se o arquivo yaml de configuração do dataset possui todos os metadados necessários para o tipo de obtenção dos dados especificado.

        Returns:
            bool: Se o arquivo yaml de metadados do dataset conter todos os metadados necessários para a forma de aquisição retorna True, caso contrário retorna False.
        """
        pass
