from brdatapy.interface.DatasetFactory import DatasetFactory
import requests
import yaml

class CadastroFundosNaoAdaptado175(DatasetFactory):

    def obter_dados(self):
        pass

    def obter_schema(self):
        pass

ds = CadastroFundosNaoAdaptado175()
print(ds.metadados_dataset)

