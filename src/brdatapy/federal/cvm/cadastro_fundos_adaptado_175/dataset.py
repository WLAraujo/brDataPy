from brdatapy.interface.DatasetFactory import DatasetFactory
import requests
import yaml

class CadastroFundosAdaptado175(DatasetFactory):

    def obter_dados(self):
        pass

    def obter_schema(self):
        pass

ds = CadastroFundosAdaptado175()
print(ds.tags_dataset)

