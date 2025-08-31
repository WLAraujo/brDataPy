from brdatapy.format_strategies.FormatStrategy import FormatStrategy
import csv
import json
from io import StringIO
from io import BytesIO
import pandas as pd
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

class FormatStrategyXlsx(FormatStrategy):
    """Classe concreta que implementa a estratégia com utilitários quando o formato do dataset que foi definido no arquivo de metadados for "xlsx".
    Essa estratégia concreta contém utilitários para tratar o dataset de acordo com seu formato, como baixar arquivo xlsx, obter dataframe pandas do dataset, obter schema do dataset.
    Por "xlsx" se tratar de um formato binário conversões para string geralmente não são necessárias.
    """

    @property
    def metadados_obrigatorios(self)->set:
        """Método que retorna os nomes dos metadados obrigatórios para o formato do dataset.

        Returns:
            set: Conjunto de nomes dos metadados obrigatórios para o formato dataset.
        """
        return {"formato_dataset", "forma_obtencao_dataset", "descricao_dataset", "tags_dataset", "nome_arquivo_dataset"}
    
    def baixar_dataset_xlsx(self):
        """Método que realiza o download do arquivo no seu formato original "xlsx".
        O método realiza o download com o nome do arquivo disponibilizado no arquivo de metadados no parâmetro "nome_arquivo_dataset".
        O download realizado traz todas as abas dentro da planilha excel.
        """
        nome_dataset = self.metadados_dataset["nome_arquivo_dataset"]
        with open(f"{nome_dataset}.xlsx", "wb") as xlsxf:
            xlsxf.write(self.conteudo_dataset.read())
        print(f"Arquivo {nome_dataset}.xlsx gerado com sucesso!")
        self.conteudo_dataset.seek(0)
    
    def baixar_dataset_csv(self):
        """Método que realiza o download do arquivo no formato "csv".
        O método converte o conteúdo do dataset de BytesIO para um pandas DataFrame e depois realiza um download no formato "csv".
        Caso o arquivo original só possua uma aba o arquivo baixado terá o mesmo nome que o parâmetro "nome_arquivo_dataset" do arquivo de metadados.
        Caso o arquivo original possua várias abas será baixado um arquivo para cada aba com o parâmetro "nome_arquivo_dataset" mais o nome da aba.
        """
        nome_dataset = self.metadados_dataset["nome_arquivo_dataset"]
        dic_df_dataset = pd.read_excel(self.conteudo_dataset, sheet_name=None, engine="openpyxl")
        for df_nome, df_conteudo in dic_df_dataset.items():
            if len(dic_df_dataset) == 1:
                nome_arquivo = f"{nome_dataset}.csv"
            else:
                nome_arquivo = f"{nome_dataset}_{df_nome}.csv"
            df_conteudo.to_csv(nome_arquivo, index=False)
            print(f"Arquivo {nome_arquivo} gerado com sucesso!")
        self.conteudo_dataset.seek(0)

    def baixar_dataset_json(self):
        """Método que realiza o download do arquivo no formato "json".
        O método converte o conteúdo do dataset de BytesIO para um objeto json do Python e depois realiza um download no formato json.
        Caso o arquivo original só possua uma aba o arquivo baixado terá o mesmo nome que o parâmetro "nome_arquivo_dataset" do arquivo de metadados.
        Caso o arquivo original possua várias abas será baixado um arquivo para cada aba com o parâmetro "nome_arquivo_dataset" mais o nome da aba.
        """
        nome_dataset = self.metadados_dataset["nome_arquivo_dataset"]
        dic_df_dataset = pd.read_excel(self.conteudo_dataset, sheet_name=None, engine="openpyxl")
        for df_nome, df_conteudo in dic_df_dataset.items():
            if len(dic_df_dataset) == 1:
                nome_arquivo = f"{nome_dataset}.json"
            else:
                nome_arquivo = f"{nome_dataset}_{df_nome}.json"
            stringio_conteudo = StringIO()
            df_conteudo.to_csv(stringio_conteudo, index=False, sep=";")
            csv_intermediario = csv.reader(stringio_conteudo, delimiter=";")
            stringio_conteudo.seek(0)
            colunas_dataset = next(csv_intermediario)
            schema_dataset = {indice_coluna: nome_coluna for indice_coluna, nome_coluna in enumerate(colunas_dataset)}
            dados_dataset = [linha for linha in csv_intermediario]
            dict_intermediario = {"schema":schema_dataset, "dados":dados_dataset}
            json_dataset = json.dumps(dict_intermediario, ensure_ascii=False, indent=4)
            with open(f"{nome_arquivo}", "w", newline="", encoding="utf-8") as jf:
                jf.write(json_dataset)
            print(f"Arquivo {nome_arquivo} gerado com sucesso!")
        self.conteudo_dataset.seek(0)

    def obter_dataframe_pandas(self)->pd.DataFrame|dict[pd.DataFrame]:
        """Método que retorna um ou mais Dataframes Pandas com o conteúdo do Dataset que originalmente é um "xlsx".
        O método converte o conteúdo de BytesIO para um ou mais Dataframes pandas e retorna esses dataframes.
        Caso o arquivo original só possua uma aba será retornado apenas um DataFrame Pandas diretamente.
        Caso o arquivo original possua várias abas será um dicionário com vários DataFrames, onde a chave de cada item do dicionário é o nome da aba e o valor é um Dataframe com o conteúdo da aba em formato pandas Dataframe.

        Returns:
            pd.DataFrame|dict[pd.DataFrame]: Dataframe pandas ou dicionário de dataframes pandas com conteúdo do dataset obtido de um "xlsx".
        """
        dic_df_dataset = pd.read_excel(self.conteudo_dataset, sheet_name=None, engine="openpyxl")
        self.conteudo_dataset.seek(0)
        if len(dic_df_dataset) == 1:
            _, df_dataset = dic_df_dataset.popitem()
            return df_dataset
        else:
            return dic_df_dataset
    
    def obter_dicionario_python(self)->dict|dict[dict]:
        """Método que retorna dicionário Python com o conteúdo do Dataset que originalmente é um "xlsx".
        O método converte o conteúdo de BytesIO para um dicionário Python e retorna esse dicionário.
        Caso o arquivo original só possua uma aba será retornado apenas um DataFrame Pandas diretamente.
        Caso o arquivo original possua várias abas será um dicionário com vários DataFrames, onde a chave de cada item do dicionário é o nome da aba e o valor é um Dataframe com o conteúdo da aba em formato pandas Dataframe.
        
        Returns:
            dict|dict[dict]: Dicionário Python com conteúdo do dataset obtido de um "xlsx" caso o arquivo possua apenas uma aba. Caso tenha mais de uma aba retorna um dicionário de dicionários, onde cada dicionário vai ter o conteúdo de uma aba.
        """
        dic_df_dataset = pd.read_excel(self.conteudo_dataset, sheet_name=None, engine="openpyxl")
        len_dic_df_dataset = len(dic_df_dataset)
        dic_dics_dataset = {}
        for df_nome, df_conteudo in dic_df_dataset.items():
            stringio_conteudo = StringIO()
            df_conteudo.to_csv(stringio_conteudo, index=False, sep=";")
            csv_intermediario = csv.reader(stringio_conteudo, delimiter=";")
            stringio_conteudo.seek(0)
            colunas_dataset = next(csv_intermediario)
            schema_dataset = {indice_coluna: nome_coluna for indice_coluna, nome_coluna in enumerate(colunas_dataset)}
            dados_dataset = [linha for linha in csv_intermediario]
            dict_dataset = {"schema":schema_dataset, "dados":dados_dataset}
            if len_dic_df_dataset > 1:
                dic_dics_dataset[df_nome] = dict_dataset
            else:
                self.conteudo_dataset.seek(0)
                return dict_dataset
        self.conteudo_dataset.seek(0)
        return dic_dics_dataset

    def _validar_metadados(self)->bool:
        """Método privado que valida se o arquivo yaml de metadados do dataset contém todos os metadados necessários para o tipo específico de estratégia de formato.

        Returns:
            bool: Caso os metadados obrigatórios estejam contidos no arquivo yaml de metadados retorna True, caso contrário retorna False.
        """
        if self.metadados_obrigatorios.issubset(self.metadados_dataset.keys()):
            return True
        else:
            return False