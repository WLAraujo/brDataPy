from brdatapy.dataset_template.DatasetTemplate import DatasetTemplate
import requests
import yaml
import pandas as pd

class SerieHistoricaMensalCrimes(DatasetTemplate):
    """Classe de dados usada para recuperar os dados da Série Histórica Mensal de Crimes no Estado do RJ desde 1991.
    A instituição responsável por esses dados é o ISP (Instituto de Segurança Pública).
    A classe deve ser usada como interface para obter os dados desse dataset em diversos formatos, como csv, xlsx, json, pandas ou dicionário.
    A classe também pode conter métodos úteis para o seu contexto.

    Args:
        DatasetTemplate: Classe abstrata qual todos os datasets implementados em classes concretas devem herdar.
    """

    def obter_metadados_dataset(self)->dict:
        """Método que retorna em um dicionário os metadados do dataset que são preenchidos no arquivo dataset_metadata.yml no mesmo diretório.
        Para essa classe são os metadados de obtenção do dataset com a série mensal de crimes no estado do Rio de Janeiro.

        Returns:
            dict: Metadados do dataset associado à essa classe.
        """
        return self.metadados_dataset()

    def baixar_dataset_csv(self):
        """Método usado para realizar download dos dados do dataset em formato "csv".
        Para essa classe é um arquivo com o dataset com a série mensal de crimes no estado do Rio de Janeiro.
        """
        self.estrategia_formato.baixar_dataset_csv()

    def baixar_dataset_xlsx(self):
        """Método usado para realizar download dos dados do dataset em formato "xlsx".
        Para essa classe é um arquivo com o dataset com a série mensal de crimes no estado do Rio de Janeiro.
        """
        self.estrategia_formato.baixar_dataset_xlsx()

    def baixar_dataset_json(self):
        """Método usado para realizar download dos dados do dataset em formato "json".
        Para essa classe é um arquivo com o dataset com a série mensal de crimes no estado do Rio de Janeiro.
        """
        self.estrategia_formato.baixar_dataset_json()
    
    def obter_dataframe_pandas(self)->pd.DataFrame:
        """Método que retorna o dataset com informações mensais dos crimes no estado do Rio de Janeiro em forma de DataFrame do pandas.
        Para essa classe é um DataFrame com o dataset com a série mensal de crimes no estado do Rio de Janeiro.

        Returns:
            pd.DataFrame: Dataframe com conteúdo do dataset
        """
        return self.estrategia_formato.obter_dataframe_pandas()

    def obter_dicionario_python(self)->dict:
        """Método que retorna o dataset com informações mensais dos crimes no estado do Rio de Janeiro em forma de dicionário python.
        Para essa classe é um dicionário com o dataset com a série mensal de crimes no estado do Rio de Janeiro.

        Returns:
            pd.DataFrame: Dicionário com conteúdo do dataset
        """
        return self.estrategia_formato.obter_dicionario_python()