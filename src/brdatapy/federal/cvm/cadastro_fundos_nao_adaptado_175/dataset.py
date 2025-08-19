from brdatapy.interface.padrao_datasets import PadraoClasseDataset
import requests
import yaml
from pathlib import Path

class CadastroFundosAdaptado175(PadraoClasseDataset):

    def __init__(self):
        self.path_arquivo_metadados = self.diretorio_pai / self.arquivo_metadados_dataset

    def obter_dados(self):
        pass

    def obter_metadados(self):
        with open(self.path_arquivo_metadados, 'r') as file:
            dados = yaml.safe_load(file)
        print(dados)

    def obter_schema(self):
        pass

ds = CadastroFundosAdaptado175()
ds.obter_metadados()