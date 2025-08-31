from brdatapy.dataset_factory.DatasetFactory import DatasetFactory
import pandas as pd
import requests
import yaml

class CadastroFundos(DatasetFactory):
    """Classe de dados usada para recuperar os dados Cadastrais de Fundos de Investimento.
    A instituição responsável por esses dados é a CVM (Comissão de Valores Mobiliários).
    Esse dataset está relacionado à ICVM175. Para saber mais sobre a ICVM 175, que altera a estrutura de fundos de investimento, acesse https://conteudo.cvm.gov.br/legislacao/resolucoes/resol175.html.
    A classe deve ser usada como interface para obter os dados desse dataset em diversos formatos, como csv, xlsx, json, pandas ou dicionário.
    A classe também pode conter métodos úteis para o seu contexto.

    Args:
        DatasetFactory: Classe abstrata qual todos os datasets implementados em classes concretas devem herdar.
    """

    def obter_metadados_dataset(self)->dict:
        """Método que retorna em um dicionário os metadados do dataset que são preenchidos no arquivo dataset_metadata.yml no mesmo diretório.
        Para essa classe são os metadados de obtenção do dataset de informações cadastrais de fundos.

        Returns:
            dict: Metadados do dataset associado à essa classe.
        """
        return self.metadados_dataset()
    
    def baixar_zip_registro_fundo_classe(self):
        """Método usado para realizar download do arquivo "zip" completo conforme disponibilizado pela CVM em seu site.
        O arquivo "zip" contém dentro dele três arquivos "csv" com as informações cadastrais de fundos de investimento, classes e subclasse.
        """
        self.estrategia_formato.baixar_arquivo_zip()

    def baixar_dataset_fundos_csv(self):
        """Método usado para realizar download do dataset com informações cadastrais de fundos de investimento em formato "csv".
        """
        self.estrategia_formato.baixar_arquivo_csv("registro_fundo")

    def baixar_dataset_classes_csv(self):
        """Método usado para realizar download do dataset com informações cadastrais de classes de fundos de investimento em formato "csv".
        """
        self.estrategia_formato.baixar_arquivo_csv("registro_classe")

    def baixar_dataset_subclasses_csv(self):
        """Método usado para realizar download do dataset com informações cadastrais de subclasses de fundos de investimento em formato "csv".
        """
        self.estrategia_formato.baixar_arquivo_csv("registro_subclasse")

    def baixar_dataset_fundos_xlsx(self):
        """Método usado para realizar download do dataset com informações cadastrais de fundos de investimento em formato "xlsx".
        """
        self.estrategia_formato.baixar_arquivo_xlsx("registro_fundo")

    def baixar_dataset_classes_xlsx(self):
        """Método usado para realizar download do dataset com informações cadastrais de classes de fundos de investimento em formato "xlsx".
        """
        self.estrategia_formato.baixar_arquivo_xlsx("registro_classe")

    def baixar_dataset_subclasses_xlsx(self):
        """Método usado para realizar download do dataset com informações cadastrais de subclasses de fundos de investimento em formato "xlsx".
        """
        self.estrategia_formato.baixar_arquivo_xlsx("registro_subclasse")

    def baixar_dataset_fundos_json(self):
        """Método usado para realizar download do dataset com informações cadastrais de fundos de investimento em formato "json".
        """
        self.estrategia_formato.baixar_arquivo_json("registro_fundo")

    def baixar_dataset_classes_json(self):
        """Método usado para realizar download do dataset com informações cadastrais de classes de fundos de investimento em formato "json".
        """
        self.estrategia_formato.baixar_arquivo_json("registro_classe")

    def baixar_dataset_subclasses_json(self):
        """Método usado para realizar download do dataset com informações cadastrais de subclasses de fundos de investimento em formato "json".
        """
        self.estrategia_formato.baixar_arquivo_json("registro_subclasse")
    
    def obter_dataframe_pandas_fundos(self)->pd.DataFrame:
        """Método que retorna o dataset com informações cadastrais de fundos de investimento em forma de DataFrame do pandas.

        Returns:
            pd.DataFrame: Dataframe com conteúdo do dataset
        """
        return self.estrategia_formato.obter_dataframe_pandas("registro_fundo")

    def obter_dataframe_pandas_classes(self)->pd.DataFrame:
        """Método que retorna o dataset com informações cadastrais de classes de fundos de investimento em forma de DataFrame do pandas.

        Returns:
            pd.DataFrame: Dataframe com conteúdo do dataset
        """
        return self.estrategia_formato.obter_dataframe_pandas("registro_classe")
    
    def obter_dataframe_pandas_subclasses(self)->pd.DataFrame:
        """Método que retorna o dataset com informações cadastrais de subclasses de fundos de investimento em forma de DataFrame do pandas.

        Returns:
            pd.DataFrame: Dataframe com conteúdo do dataset
        """
        return self.estrategia_formato.obter_dataframe_pandas("registro_subclasse")

    def obter_dicionario_python_fundos(self)->dict:
        """Método que retorna o dataset com informações cadastrais de fundos em forma de dicionário python.

        Returns:
            pd.DataFrame: Dicionário com conteúdo do dataset
        """
        return self.estrategia_formato.obter_dicionario_python("registro_fundo")
    
    def obter_dicionario_python_classes(self)->dict:
        """Método que retorna o dataset com informações cadastrais de classes de fundos em forma de dicionário python.

        Returns:
            pd.DataFrame: Dicionário com conteúdo do dataset
        """
        return self.estrategia_formato.obter_dicionario_python("registro_classe")
    
    def obter_dicionario_python_subclasses(self)->dict:
        """Método que retorna o dataset com informações cadastrais de subclasses de fundos em forma de dicionário python.

        Returns:
            pd.DataFrame: Dicionário com conteúdo do dataset
        """
        return self.estrategia_formato.obter_dicionario_python("registro_subclasse")
