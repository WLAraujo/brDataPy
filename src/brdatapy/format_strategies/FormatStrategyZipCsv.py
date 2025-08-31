from brdatapy.format_strategies.FormatStrategy import FormatStrategy
import csv
import json
import zipfile
from io import BytesIO
from io import StringIO
import pandas as pd
from pathlib import Path

class FormatStrategyZipCsv(FormatStrategy):
    """Classe concreta que implementa a estratégia com utilitários quando o formato do dataset que foi definido no arquivo de metadados for "zip_csv".
    Esse formato indica que o conteúdo do dataset está dentro de um ou mais arquivos "csv" compactados dentro de um único arquivo "zip".
    Essa estratégia concreta contém utilitários para tratar o dataset de acordo com seu formato, como baixar arquivo csv, obter dataframe pandas do dataset, obter schema do dataset.
    Por "csv" se tratar de um formato de text conversões para string geralmente são necessárias.
    """

    def __init__(self, metadados_dataset:dict, conteudo_dataset:StringIO):
        """Método inicializador da estratégia de leitura de arquivos "zip" que contenham um ou mais arquivos "csv".
        Esse método sobrescreve o inicializador da classe mãe para fazer uma validação da quantidade e dos nomes de arquivos no "zip".

        Args:
            metadados_dataset (dict): Dicionário com todos os metadados do dataset que estão contidos no yaml de configuração.
            conteudo_dataset (StringIO): Conteúdo do dataset em memória para ser tratado com os utilitários da estratégia. 
        """
        self.metadados_dataset = metadados_dataset
        self._conteudo_dataset = conteudo_dataset

    @property
    def metadados_obrigatorios(self)->set:
        """Método que retorna os nomes dos metadados obrigatórios para o formato do dataset.

        Returns:
            set: Conjunto de nomes dos metadados obrigatórios para o formato dataset.
        """
        return {"formato_dataset", "forma_obtencao_dataset", "descricao_dataset", "tags_dataset", "nome_arquivo_dataset", "caractere_separacao"}
    
    @property
    def conteudo_dataset(self)->BytesIO:
        """Método que retorna o conteúdo do dataset no formato BytesIO. 
        O método retorna o conteúdo do dataset em memória.
        Esse atributo é inicializado sempre junto com criação do objeto mas em uma variável privada, esse método apenas expõe o conteúdo da variável.

        Returns:
            BytesIO: Conteúdo do dataset em memória no formato BytesIO
        """
        return self._conteudo_dataset
            
    def _validar_existencia_arquivo(self, arquivo_no_zip:str):
        """Método privado que deve ser usado para validar se existe no "zip" sendo tratado algum arquivo "csv" com o nome passado de parâmetro.
        Caso não existe arquivo com nome igual ao passado como parâmetro o método lança um erro.

        Args:
            arquivo_no_zip (str): Nome de arquivo no "zip", igual ao que estiver registrado no arquivo "yaml" de metadados.
        """
        with zipfile.ZipFile(self.conteudo_dataset) as zf:
            try:
                assert arquivo_no_zip in [Path(nome_arquivo).stem for nome_arquivo in zf.namelist() if nome_arquivo.endswith(".csv")]
            except:
                raise Exception("Arquivo com nome passado como parâmetro do método não está contido no zip, favor reveja o nome usado na chamada do método.\nA extensão não deve ser usada no parâmetro.")

    def _string_conteudo_arquivo(self, arquivo_no_zip)->str:
        """Método que realiza decodificação do conteúdo de um dos arquivos contidos no zip, que está em formato BytesIO, para uma string que possa ser usada pelos métodos da classe.

        Args:
            arquivo_no_zip (str): Nome de arquivo no zip, igual ao que estiver registrado no arquivo "yaml" de metadados.

        Returns:
            str: String com conteúdo do dataset decodificado.
        """
        with zipfile.ZipFile(self.conteudo_dataset) as zf:
            self._validar_existencia_arquivo(arquivo_no_zip)
            conteudo_arquivo_no_zip = zf.read(f"{arquivo_no_zip}.csv")
            try:
                string_conteudo = conteudo_arquivo_no_zip.decode("utf-8")
            except UnicodeDecodeError:
                string_conteudo = conteudo_arquivo_no_zip.decode("latin1")
            return string_conteudo
    
    def baixar_arquivo_zip(self):
        """Método que realiza o download do arquivo "zip" original com todos seus arquivos.
        O método converte o conteúdo de BytesIO para "zip" e realiza o download com o nome do arquivo disponibilizado no arquivo de metadados no parâmetro "nome_dataset".
        """
        nome_dataset = self.metadados_dataset["nome_dataset"]
        with open(f"{nome_dataset}.zip", "wb") as zf:
            zf.write(self.conteudo_dataset.getvalue())
        print(f"Arquivo {nome_dataset}.zip gerado com sucesso!")

    def baixar_arquivo_csv(self, arquivo_no_zip:str):
        """Método que realiza o download de apenas um dos arquivos "csv" contidos no "zip".
        O nome de um dos arquivos contidos no parâmetro "nome_dataset" deve ser passado como parâmetro desse método.

        Args:
            arquivo_no_zip (str): Nome de arquivo no zip, igual ao que estiver registrado no arquivo "yaml" de metadados.
        """
        string_conteudo = self._string_conteudo_arquivo(arquivo_no_zip)
        nome_dataset = arquivo_no_zip
        with open(f"{nome_dataset}.csv", "w", newline="", encoding="utf-8") as csvf:
            csvf.write(string_conteudo)
        print(f"Arquivo {nome_dataset}.csv gerado com sucesso!")
        self.conteudo_dataset.seek(0)        
            
    
    def baixar_todo_arquivo_csv(self):
        """Método que realiza o download do arquivo, ou dos arquivos, "csv" que estiverem contidos no arquivo "zip" e tiverem seu nome registrado no arquivo "yaml" de metadados.
        O método converte o conteúdo de BytesIO para "zip" e itera pelos arquivos contidos nele, baixando todos os arquivos "csv" que forem identificados no "zip".
        """
        with zipfile.ZipFile(self.conteudo_dataset) as zf:
            for arquivo_csv_no_zip in self.metadados_dataset["nome_arquivo_dataset"]:
                self.baixar_arquivo_csv(arquivo_csv_no_zip)
        self.conteudo_dataset.seek(0)

    def baixar_arquivo_xlsx(self, arquivo_no_zip:str):
        """Método que recebe o nome de um dos arquivos "csv" que esteja contido dentro do arquivo "zip" e faz o download desse arquivo no formato "xlsx".
        O nome do arquivo deve ser passado como parâmetro do método mas sem a extensão.
        Deve ser um dos nomes contidos no parâmetro "nome_arquivo_dataset" dentro do "yaml" de metadados.

        Args:
            arquivo_no_zip (str): Nome de arquivo no zip, igual ao que estiver registrado no arquivo "yaml" de metadados.
        """
        nome_dataset = arquivo_no_zip
        string_conteudo = self._string_conteudo_arquivo(arquivo_no_zip)
        stringio_conteudo = StringIO(string_conteudo)
        csv_intermediario = csv.reader(stringio_conteudo, delimiter=self.metadados_dataset["caractere_separacao"], quoting=csv.QUOTE_NONE)
        colunas_dataset = next(csv_intermediario)
        df_intermediario = pd.DataFrame(csv_intermediario, columns=colunas_dataset)
        df_intermediario.to_excel(f"{nome_dataset}.xlsx", index=False, engine="openpyxl")
        print(f"Arquivo {nome_dataset}.xlsx gerado com sucesso!")
        self.conteudo_dataset.seek(0)

    def baixar_arquivo_json(self, arquivo_no_zip:str):
        """Método que recebe o nome de um dos arquivos "csv" que esteja contido dentro do arquivo "zip" e faz o download desse arquivo no formato "json".
        O nome do arquivo deve ser passado como parâmetro do método mas sem a extensão.
        Deve ser um dos nomes contidos no parâmetro "nome_arquivo_dataset" dentro do "yaml" de metadados.

        Args:
            arquivo_no_zip (str): Nome de arquivo no zip, igual ao que estiver registrado no arquivo "yaml" de metadados.
        """
        nome_dataset = arquivo_no_zip
        string_conteudo = self._string_conteudo_arquivo(arquivo_no_zip)
        stringio_conteudo = StringIO(string_conteudo)
        csv_intermediario = csv.reader(stringio_conteudo, delimiter=self.metadados_dataset["caractere_separacao"], quoting=csv.QUOTE_NONE)
        colunas_dataset = next(csv_intermediario)
        schema_dataset = {indice_coluna: nome_coluna for indice_coluna, nome_coluna in enumerate(colunas_dataset)}
        dados_dataset = [linha for linha in csv_intermediario]
        dict_intermediario = {"schema":schema_dataset, "dados":dados_dataset}
        json_dataset = json.dumps(dict_intermediario, ensure_ascii=False, indent=4)
        with open(f"{nome_dataset}.json", "w", newline="", encoding="utf-8") as jf:
            jf.write(json_dataset)
        print(f"Arquivo {nome_dataset}.json gerado com sucesso!")
        self.conteudo_dataset.seek(0)

    def obter_dataframe_pandas(self, arquivo_no_zip)->pd.DataFrame:
        """Método usado para retornar um DataFrame pandas com o conteúdo de um dos datasets listados no arquivo de metadados.
        Deve ser passado como parâmetro o nome do arquivo de um dos datasets contidos no "zip" que também deve estar registrado no parâmetro "nome_arquivo_dataset" do arquivo "yaml" de metadados.

        Args:
            arquivo_no_zip (str): Nome do arquivo "csv" contido no "zip" que possui o conteúdo do dataset que deseja obter.

        Returns:
            pd.DataFrame: Dataframe pandas com conteúdo do dataset passado como parâmetro.
        """
        string_conteudo = self._string_conteudo_arquivo(arquivo_no_zip)
        stringio_conteudo = StringIO(string_conteudo)
        csv_intermediario = csv.reader(stringio_conteudo, delimiter=self.metadados_dataset["caractere_separacao"], quoting=csv.QUOTE_NONE)
        colunas_dataset = next(csv_intermediario)
        df_dataset = pd.DataFrame(csv_intermediario, columns=colunas_dataset)
        self.conteudo_dataset.seek(0)
        return df_dataset

    def obter_todo_dataframe_pandas(self)->dict[pd.DataFrame]:
        """Método que retorna um DataFrame pandas para cada arquivo "csv" contido no "zip" e que tenha seu nome registrado no parâmetro "nome_arquivo_dataset" do arquivo de metadados.
        O formato de retorno é um dicionário, onde cada chave é um nome de arquivo registrado no arquivo de metadados e leva para o DataFrame pandas do respectivo arquivo.

        Returns:
            dict[pd.DataFrame]: Dicionário onde cada chave retorna um DataFrame pandas de um arquivo com nome registrado no arquivo de metadados e esteja contido no arquivo "zip".
        """
        dict_datasets_zip = {}
        for arquivo_no_zip in self.metadados_dataset["nome_arquivo_dataset"]:
            df_dataset = self.obter_dataframe_pandas(arquivo_no_zip)
            dict_datasets_zip[arquivo_no_zip] = df_dataset
        return  dict_datasets_zip

    def obter_dicionario_python(self, arquivo_no_zip:str)->dict:
        """Método usado para retornar um dicionário Python com o conteúdo de um dos datasets listados no arquivo de metadados.
        Deve ser passado como parâmetro o nome do arquivo de um dos datasets contidos no "zip" que também deve estar registrado no parâmetro "nome_arquivo_dataset" do arquivo "yaml" de metadados.

        Args:
            arquivo_no_zip (str): Nome do arquivo "csv" contido no "zip" que possui o conteúdo do dataset que deseja obter.

        Returns:
            dict: Dicionário Python com conteúdo do dataset passado como parâmetro.
        """
        string_conteudo = self._string_conteudo_arquivo(arquivo_no_zip)
        stringio_conteudo = StringIO(string_conteudo)
        csv_intermediario = csv.reader(stringio_conteudo, delimiter=self.metadados_dataset["caractere_separacao"], quoting=csv.QUOTE_NONE)
        colunas_dataset = next(csv_intermediario)
        schema_dataset = {indice_coluna: nome_coluna for indice_coluna, nome_coluna in enumerate(colunas_dataset)}
        dados_dataset = [linha for linha in csv_intermediario]
        dict_dataset = {"schema":schema_dataset, "dados":dados_dataset}
        self.conteudo_dataset.seek(0)
        return dict_dataset

    def obter_todo_dicionario_python(self)->dict[dict]:
        """Método que retorna uma lista com um dicionário Python para cada arquivo "csv" contido no "zip" e que tenha seu nome registrado no parâmetro "nome_arquivo_dataset" do arquivo de metadados.
        O formato de retorno é uma lista, onde cada elemento é um dicionário com o conteúdo do respectivo arquivo.

        Returns:
            dict[dict]: Lista onde cada elemento é um dicionário Python com o conteúdo de um arquivo com nome registrado no arquivo de metadados e esteja contido no arquivo "zip".
        """
        dict_datasets_zip = {}
        for arquivo_no_zip in self.metadados_dataset["nome_arquivo_dataset"]:
            dict_dataset = self.obter_dicionario_python(arquivo_no_zip)
            dict_datasets_zip[arquivo_no_zip] = dict_dataset
        return dict_datasets_zip

    def _validar_metadados(self)->bool:
        """Método privado que valida se o arquivo yaml de metadados do dataset contém todos os metadados necessários para o tipo específico de estratégia de formato.

        Returns:
            bool: Caso os metadados obrigatórios estejam contidos no arquivo yaml de metadados retorna True, caso contrário retorna False.
        """
        if self.metadados_obrigatorios.issubset(self.metadados_dataset.keys()):
            return True
        else:
            return False