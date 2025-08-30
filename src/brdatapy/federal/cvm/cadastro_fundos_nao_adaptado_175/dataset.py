from brdatapy.interface.DatasetFactory import DatasetFactory
import requests
import yaml
import pandas as pd

class CadastroFundosNaoAdaptado175(DatasetFactory):
    """Classe de dados usada para recuperar os dados Cadastrais de Fundos Não Adaptados à ICVM 175.
    A instituição responsável por esses dados é a CVM (Comissão de Valores Mobiliários).
    Para saber mais sobre a ICVM 175, que altera a estrutura de fundos de investimento, acesse https://conteudo.cvm.gov.br/legislacao/resolucoes/resol175.html.
    A classe deve ser usada como interface para obter os dados desse dataset em diversos formatos, como csv, xlsx, json, pandas ou dicionário.
    A classe também pode conter métodos úteis para o seu contexto.

    Args:
        DatasetFactory: Classe abstrata qual todos os datasets implementados em classes concretas devem herdar.
    """

    def obter_metadados_dataset(self)->dict:
        """Método que retorna em um dicionário os metadados do dataset que são preenchidos no arquivo dataset_metadata.yml no mesmo diretório.
        Para essa classe são os metadados de obtenção do dataset de informações cadastrais de fundos não adaptados à ICVM 175.

        Returns:
            dict: Metadados do dataset associado à essa classe.
        """
        return self.metadados_dataset()

    def baixar_dataset_csv(self):
        """Método usado para realizar download dos dados do dataset em formato "csv".
        Para essa classe é um arquivo com o dataset de informações cadastrais de fundos não adaptados à ICVM 175.
        """
        self.estrategia_formato.baixar_dataset_csv()

    def baixar_dataset_xlsx(self):
        """Método usado para realizar download dos dados do dataset em formato "xlsx".
        Para essa classe é um arquivo com o dataset de informações cadastrais de fundos não adaptados à ICVM 175.
        """
        self.estrategia_formato.baixar_dataset_xlsx()

    def baixar_dataset_json(self):
        """Método usado para realizar download dos dados do dataset em formato "json".
        Para essa classe é um arquivo com o dataset de informações cadastrais de fundos não adaptados à ICVM 175.
        """
        self.estrategia_formato.baixar_dataset_json()
    
    def obter_dataframe_pandas(self)->pd.DataFrame:
        """Método que retorna os dataset com informações cadastradais de fundos não adaptados à ICVM 175 em forma de DataFrame do pandas.
        Para essa classe é um DataFrame com o dataset de informações cadastrais de fundos não adaptados à ICVM 175.

        Returns:
            pd.DataFrame: Dataframe com conteúdo do dataset
        """
        return self.estrategia_formato.obter_dataframe_pandas()

    def obter_dicionario_python(self)->dict:
        """Método que retorna os dataset com informações cadastradais de fundos não adaptados à ICVM 175 em forma de dicionário python.
        Para essa classe é um dicionário com o dataset de informações cadastrais de fundos não adaptados à ICVM 175.

        Returns:
            pd.DataFrame: Dicionário com conteúdo do dataset
        """
        return self.estrategia_formato.obter_dicionario_python()
