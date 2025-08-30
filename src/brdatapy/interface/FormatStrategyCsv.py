from brdatapy.interface.FormatStrategy import FormatStrategy
import csv
import json
from io import StringIO
import pandas as pd

class FormatStrategyCsv(FormatStrategy):
    """Classe concreta que implementa a estratégia com utilitários quando o formato do dataset que foi definido no arquivo de metadados for "csv".
    Essa estratégia concreta contém utilitários para tratar o dataset de acordo com seu formato, como baixar arquivo csv, obter dataframe pandas do dataset, obter schema do dataset.
    """

    @property
    def metadados_obrigatorios(self)->set:
        """Método que retorna os nomes dos metadados obrigatórios para o formato do dataset.

        Returns:
            set: Conjunto de nomes dos metadados obrigatórios para o tipo de obtenção do dataset.
        """
        return {"formato_dataset", "forma_obtencao_dataset", "descricao_dataset", "tags_dataset", "nome_arquivo_dataset", "caracter_separacao"}
    
    def baixar_dataset_csv(self):
        """Método que realiza o download do arquivo no seu formato original "csv".
        O método converte o conteúdo de StringIO para csv e realiza o download com o nome do arquivo disponibilizado no arquivo de metadados no parâmetro "nome_arquivo_dataset".
        """
        nome_dataset = self.metadados_dataset["nome_arquivo_dataset"]
        with open(f"{nome_dataset}.csv", "w", newline="", encoding="utf-8") as f:
            f.write(self.conteudo_dataset.getvalue())
        print(f"Arquivo {nome_dataset}.csv gerado com sucesso!")
    
    def baixar_dataset_xlsx(self):
        """Método que realiza o download do arquivo no formato "xlsx".
        O método converte o conteúdo de StringIO para um dataframe pandas e depois usa métodos do pacote para realizar um download no formato xlsx.
        O arquivo baixado vai ter o nome do parâmetro "nome_arquivo_dataset".
        """
        nome_dataset = self.metadados_dataset["nome_arquivo_dataset"]
        csv_intermediario = csv.reader(self.conteudo_dataset, delimiter=self.metadados_dataset["caracter_separacao"])
        colunas_dataset = next(csv_intermediario)
        df_intermediario = pd.DataFrame(csv_intermediario, columns=colunas_dataset)
        df_intermediario.to_excel(f"{nome_dataset}.xlsx", index=False, engine="openpyxl")
        print(f"Arquivo {nome_dataset}.xlsx gerado com sucesso!")
        self.conteudo_dataset.seek(0)

    def baixar_dataset_json(self):
        """Método que realiza o download do arquivo no formato "json".
        O método converte o conteúdo do dataset de StringIO para um objeto json do Python e depois realiza um download no formato json.
        O arquivo baixado vai ter o nome do parâmetro "nome_arquivo_dataset".
        """
        nome_dataset = self.metadados_dataset["nome_arquivo_dataset"]
        csv_intermediario = csv.reader(self.conteudo_dataset, delimiter=self.metadados_dataset["caracter_separacao"])
        colunas_dataset = next(csv_intermediario)
        schema_dataset = {indice_coluna: nome_coluna for indice_coluna, nome_coluna in enumerate(colunas_dataset)}
        dados_dataset = [linha for linha in csv_intermediario]
        dict_intermediario = {"schema":schema_dataset, "dados":dados_dataset}
        json_dataset = json.dumps(dict_intermediario, ensure_ascii=False, indent=4)
        with open(f"{nome_dataset}.json", "w", newline="", encoding="utf-8") as f:
            f.write(json_dataset)
        print(f"Arquivo {nome_dataset}.json gerado com sucesso!")
        self.conteudo_dataset.seek(0)

    def obter_dataframe_pandas(self)->pd.DataFrame:
        """Método que retorna Dataframe Pandas com o conteúdo do Dataset que originalmente é um "csv".
        O método converte o conteúdo de StringIO para um dataframe pandas e retorna esse dataframe.

        Returns:
            pd.DataFrame: Dataframe pandas com conteúdo do dataset obtido de um "csv".
        """
        df_dataset = pd.read_csv(self.conteudo_dataset, sep=self.metadados_dataset["caracter_separacao"], low_memory=False)
        self.conteudo_dataset.seek(0)
        return df_dataset
    
    def obter_dicionario_python(self)->dict:
        """Método que retorna dicionário Python com o conteúdo do Dataset que originalmente é um "csv".
        O método converte o conteúdo de StringIO para um dicionário Python e retorna esse dicionário.

        Returns:
            dict: Dicionário Python com conteúdo do dataset obtido de um "csv".
        """
        csv_intermediario = csv.reader(self.conteudo_dataset, delimiter=self.metadados_dataset["caracter_separacao"])
        colunas_dataset = next(csv_intermediario)
        schema_dataset = {indice_coluna: nome_coluna for indice_coluna, nome_coluna in enumerate(colunas_dataset)}
        dados_dataset = [linha for linha in csv_intermediario]
        dict_dataset = {"schema":schema_dataset, "dados":dados_dataset}
        self.conteudo_dataset.seek(0)
        return dict_dataset

    def _validar_metadados(self)->bool:
        """Método privado que valida se o arquivo yaml de metadados do dataset contém todos os metadados necessários para o tipo específico de estratégia de formato.

        Returns:
            bool: Caso os metadados obrigatórios estejam contidos no arquivo yaml de metadados retorna True, caso contrário retorna False.
        """
        if self.metadados_obrigatorios.issubset(self.metadados_dataset.keys()):
            return True
        else:
            return False