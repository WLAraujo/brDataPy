from pathlib import Path
import yaml
from difflib import get_close_matches
import unicodedata
import re

class CatalogoMetadados():
    """Classe de dados responsável pelo busca de informações dentro do pacote.
    O conceito do brDataPy está muito relacionado a conectar pessoas que desejam analisar dados públicos a datasets que já existam e sejam fornecidos por instituições públicas.
    Essa classe contém diversos métodos para realizar busca de informação dentro do pacote.
    Podem ser realizadas buscas pela descrição dos dataset, instituições e tags.
    A classe também oferece métodos para dar uma visão ampla 
    """

    def __init__(self):
        """Inicializador da classe catálogo, busca todos os arquivos de metadados existentes e também seu conteúdo para assim possibilitar as buscas por critérios diversos.
        """
        self.arquivos_metadados = self._arquivos_metadados()
        self.conteudo_arquivos_metadados = self._conteudo_arquivos_metadados()

    def _arquivos_metadados(self)->list[str]:
        """Método que retorno em string todos os caminhos de arquivos de metadados que existem no pacote.

        Returns:
            list[str]: Lista onde cada elemento é o caminho completo para um arquivo "dataset_metadata".
        """
        raiz_base_src = Path(__file__).resolve().parents[1]
        caminho_arquivos_yaml = {str(caminho.parent)+"/dataset_metadata.yaml" for caminho in raiz_base_src.rglob("dataset_metadata.yaml")}
        caminho_arquivos_yml = {str(caminho.parent)+"/dataset_metadata.yml" for caminho in raiz_base_src.rglob("dataset_metadata.yml")}
        caminhos_arquivos_metadados = list(caminho_arquivos_yaml) + list(caminho_arquivos_yml)
        return caminhos_arquivos_metadados
    
    def _conteudo_arquivos_metadados(self)->list[dict]:
        """Método que retorna uma lista com o conteúdo de todos os arquivos de metadados dos datasets disponíveis para consumo no pacote.

        Returns:
            list[dict]: Lista de dicionários onde cada dicionário tem as mesmas informações contidas em um yaml de metadados.
        """
        conteudo_metadados_datasets = []
        for arquivo_metadados in self.arquivos_metadados:
            path_arquivo_metadados = Path(arquivo_metadados)
            with path_arquivo_metadados.open("r", encoding="utf-8") as ymlf:
                metadados_dataset = yaml.safe_load(ymlf)
                conteudo_metadados_datasets.append(metadados_dataset)
        return conteudo_metadados_datasets

    def mostrar_tags(self, mostrar_tags:bool=False)->set:
        """Método que consome a informação "tags_dataset" de todos os arquivos de metadados disponíveis no pacote e retorna um set com todas as tags existentes.
        Tags são um recurso do pacote para busca de datasets que estejam relacionados a um tópico ou instituição de interesse do usuário.
        Existe um parâmetro opcional para imprimir as tags em tela.

        Args:
            mostrar_tags (bool, optional): Se True além de devolver as tags como set também imprime seus valores na tela. Valor default é False.

        Returns:
            set: Conjunto com todas as tags existentes nos metadados dos datasets.
        """
        listas_tags_datasets = [metadados["tags_dataset"] for metadados in self.conteudo_arquivos_metadados]
        conjunto_tags_dataset = {tag for lista_tags_dataset in listas_tags_datasets for tag in lista_tags_dataset}
        if mostrar_tags:
            print(conjunto_tags_dataset)
        return conjunto_tags_dataset

    def mostrar_datasets(self, mostrar_datasets:bool=False)->set:
        """Método que consome a informação "nome_dataset" de todos os arquivos de metadados disponíveis no pacote e retorna um set com todas os datasets existentes.
        O nome do dataset é uma forma de reconhecer facilmente o seu conteúdo e seu objetivo.
        Existe um parâmetro opcional para imprimir as tags em tela.

        Args:
            mostrar_datasets (bool, optional): Se True além de devolver os nomes de datasets também imprime seus valores na tela. Valor default é False.

        Returns:
            set: Conjunto com o nome de todos os datsets disponíveis no pacote.
        """
        conjunto_nomes_datasets = {metadados["nome_dataset"] for metadados in self.conteudo_arquivos_metadados}
        if mostrar_datasets:
            print(conjunto_nomes_datasets)
        return conjunto_nomes_datasets

    def filtrar_datasets_por_tag(self, tag_buscada:str, busca_aproximada:bool=False)->set:
        """Método que busca nos metadados de todos os datasets disponíveis no pacote quais possuem uma determinada tag em seus metadados.
        Método útil para buscar datasets que atendam uma necessidade específica e estejam marcados com tags que remetam essa necessidade.
        O parâmetro opcional "busca_aproximada" quando definido como True também traz no seu resultado tags semelhantes, não apenas a tag exata.
        O método retorna um conjunto com todos os datasets que tiverem resultado positivo na busca.

        Args:
            tag_buscada (str): Tag que será usada na busca.
            busca_aproximada (bool, optional): Se True o método também devolve datasets com tags semelhantes à tag buscada, não apenas matches exatos. Valor default é False.

        Returns:
            set: Conjunto com todos os datsets que tiveram resultado positivo na busca.
        """
        conjunto_datasets_match = set()
        for metadados_dataset in self.conteudo_arquivos_metadados:
            tags_dataset = metadados_dataset["tags_dataset"]
            nome_dataset = metadados_dataset["nome_dataset"]
            if tag_buscada in tags_dataset:
                conjunto_datasets_match.add(nome_dataset)
            elif busca_aproximada:
                resultados_aproximados = get_close_matches(tag_buscada, tags_dataset, cutoff=0.75)
                if resultados_aproximados != []: conjunto_datasets_match.add(nome_dataset)
        return conjunto_datasets_match
            
    def filtrar_datasets_por_descricao(self, texto_buscado: str) -> set:
        """Método que busca nos metadados de todos os datasets disponíveis no pacote quais possuem uma determinada substring em suas descrições.
        Método útil para buscar datasets que atendam uma necessidade específica com base na descrição.
        O método retorna um conjunto com todos os datasets que tiverem resultado positivo na busca.

        Args:
            texto_buscado (str): Termo que será usado na busca. Serão retornados datasets que o parâmetro "descricao_dataset" dentro do arquivo de metadados contenha esse texto.

        Returns:
            set: Conjunto com todos os datasets que tiveram resultado positivo na busca.
        """
        conjunto_datasets_match = set()
        for metadados_dataset in self.conteudo_arquivos_metadados:
            descricao_dataset = metadados_dataset["descricao_dataset"]
            nome_dataset = metadados_dataset["nome_dataset"]
            if texto_buscado.lower() in descricao_dataset.lower():
                conjunto_datasets_match.add(nome_dataset)  
        return conjunto_datasets_match