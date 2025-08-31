from brdatapy.dataset_factory.DatasetFactory import DatasetFactory
import pandas as pd
import requests
import yaml
import datetime

class OcorrenciasCriminaisMensal(DatasetFactory):

    def __init__(self, ano:str="0", escopo:str="estado", regiao:str="0"):
        """Método inicializador da classe do dataset Ocorrencias Criminais Mensal do Estado de São Paulo.
        Se nenhum parâmetro for passado são usados os parâmetros de consulta default (últimos 4 anos de dados para todo o estado).
        Como parâmetros desse inicializador temos o ano dos dados, o escopo que pode ser "região" ou "estado" e caso seja "região" o nome da região também deve ser passado.
        Para consultar quais regiões estão disponíveis consulte o parâmetro estático da classe "regioes_disponiveis", deve ser passado a chave não o valor.
        Se o ano passado for "0" significa que os dados dos 4 últimos anos serão retornados.

        Args:
            ano (str): Ano dos dados que o dataset deve conter. Se o valor desse parâmetro for "0" serão obtidos todos os dados dos últimos 4 anos.
            escopo (str): Se os dados do dataset serão de uma região específica ou de todo o estado. "região" ou "estado"
            regiao (str): Se o escopo selecionado for região deve ser preenchido com o nome da região. Valor default é 0.
        """
        anos_disponiveis = list(range(2001,datetime.date.today().year+1))
        anos_disponiveis.append(0)
        if int(ano) not in anos_disponiveis:
            raise Exception('Parâmetro inválido: Para esse dataset só temos dados entre 2001 e o último mês')
        if escopo not in ["região", "estado"]: 
            raise Exception('Parâmetro inválido: O escopo do dataset deve ser ou "região" ou "estado"')
        if (regiao != "0") and (regiao not in self.regioes_disponiveis().keys()): 
            raise Exception('Parâmetro inválido: A região passada como parâmetro não está disponível, favor consultar o parâmetro estático "regioes_disponiveis"')
        if regiao != "0":
            regiao = self.regioes_disponiveis()[regiao]
        self.parametros_query_api = {
            "ano" : ano,
            "grupoDelito" : "6",
            "tipoGrupo" : escopo.upper(),
            "idGrupo" : regiao
        }
        super().__init__()

    @staticmethod
    def regioes_disponiveis()->dict:
        """Método estático que retorna todas as regiões disponíveis para serem consultadas.
        As regiões listadas aqui podem ser usadas na inicialização de um objeto da classe caso a consulta necessária seja mais específica.
        Lembrando que a consulta default traz os últimos 4 anos das estatísticas para todo o estado de São Paulo.
        """
        return {
            "Araçatuba" : "12",
            "Bauru" : "6",
            "Campinas" : "4",
            "Capital" : "1",
            "Grande São Paulo" : "2",
            "Piracicaba" : "11",
            "Presidente Prudente" : "10",
            "Ribeirão Preto" : "5",
            "Santos" : "8",
            "São José do Rio Preto" : "7",
            "São José dos Campos" : "3",
            "Sorocaba" : "9"
        }
    
    def obter_metadados_dataset(self)->dict:
        """Método que retorna em um dicionário os metadados do dataset que são preenchidos no arquivo dataset_metadata.yml no mesmo diretório.
        Para essa classe são os metadados de obtenção do dataset de ocorrências criminais do estado de São Paulo.

        Returns:
            dict: Metadados do dataset associado à essa classe.
        """
        return self.metadados_dataset()

    def baixar_dataset_csv(self):
        """Método usado para realizar download dos dados do dataset em formato "csv".
        Para essa classe é um arquivo com o dataset de ocorrências criminais do estado de São Paulo.
        """
        self.estrategia_formato.baixar_dataset_csv()

    def baixar_dataset_xlsx(self):
        """Método usado para realizar download dos dados do dataset em formato "xlsx".
        Para essa classe é um arquivo com o dataset de ocorrências criminais do estado de São Paulo.
        """
        self.estrategia_formato.baixar_dataset_xlsx()

    def baixar_dataset_json(self):
        """Método usado para realizar download dos dados do dataset em formato "json".
        Para essa classe é um arquivo com o dataset de ocorrências criminais do estado de São Paulo.
        """
        self.estrategia_formato.baixar_dataset_json()
    
    def obter_dataframe_pandas(self)->pd.DataFrame:
        """Método que retorna os dataset com informações de ocorrências criminais do estado de São Paulo em forma de DataFrame do pandas.
        Para essa classe é um DataFrame com o dataset de ocorrências criminais do estado de São Paulo.

        Returns:
            pd.DataFrame: Dataframe com conteúdo do dataset
        """
        return self.estrategia_formato.obter_dataframe_pandas()

    def obter_dicionario_python(self)->dict:
        """Método que retorna os dataset com informações de ocorrências criminais do estado de São Paulo em forma de dicionário python.
        Para essa classe é um dicionário com o dataset de ocorrências criminais do estado de São Paulo.

        Returns:
            pd.DataFrame: Dicionário com conteúdo do dataset
        """
        return self.estrategia_formato.obter_dicionario_python()
    
