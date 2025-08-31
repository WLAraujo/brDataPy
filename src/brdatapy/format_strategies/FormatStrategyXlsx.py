from brdatapy.format_strategies.FormatStrategy import FormatStrategy
import requests
import csv
from io import StringIO
import pandas as pd

class FormatStrategyXlsx(FormatStrategy):
    """Classe concreta que implementa a estratégia com utilitários quando o formato do dataset que foi definido no arquivo de metadados for "xlsx".
    Essa estratégia concreta contém utilitários para tratar o dataset de acordo com seu formato, como baixar arquivo xlsx, obter dataframe pandas do dataset, obter schema do dataset.
    """

    @property
    def metadados_obrigatorios(self)->set:
        """Método que retorna os nomes dos metadados obrigatórios para o formato do dataset.

        Returns:
            set: Conjunto de nomes dos metadados obrigatórios para o tipo de obtenção do dataset.
        """
        return {"formato_dataset", "forma_obtencao_dataset", "descricao_dataset", "tags_dataset", "nome_arquivo_dataset"}
    
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
        df_intermediario = pd.read_csv(self.conteudo_dataset)
        df_intermediario.to_excel(f"{nome_dataset}.xlsx", index=False)

    def pandas_dataframe(self)->pd.DataFrame:
        """Método que retorna Dataframe Pandas

        Returns:
            pd.DataFrame: _description_
        """

    def _validar_metadados(self)->bool:
        """Método privado que valida se o arquivo yaml de metadados do dataset contém todos os metadados necessários para o tipo específico de estratégia de formato.

        Returns:
            bool: Caso os metadados obrigatórios estejam contidos no arquivo yaml de metadados retorna True, caso contrário retorna False.
        """
        if self.metadados_obrigatorios.issubset(self.metadados_dataset.keys()):
            return True
        else:
            return False