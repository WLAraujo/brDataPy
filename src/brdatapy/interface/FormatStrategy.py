from abc import ABC, abstractmethod

class FormatStrategy(ABC):

    def __init__(self, metadados_dataset:dict):
        self.metadados_dataset = metadados_dataset

    @property
    @abstractmethod
    def metadados_obrigatorios(self)->set:
        pass

    @abstractmethod
    def obter_dados(self):
        pass

    @abstractmethod
    def _validar_metadados(self)->bool:
        pass
