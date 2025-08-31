from pathlib import Path

class CatalogoMetadados():
    """Classe de dados responsável pelo busca de informações dentro do pacote.
    O conceito do brDataPy está muito relacionado a conectar pessoas que desejam analisar dados públicos a datasets que já existam e sejam fornecidos por instituições públicas.
    Essa classe contém diversos métodos para realizar busca de informação dentro do pacote.
    Podem ser realizadas buscas pela descrição dos dataset, instituições e tags.
    A classe também oferece métodos para dar uma visão ampla 
    """

    def _diretorios_com_datasets():
        base_path = Path(diretorio_base)
        diretorios = {arquivo.parent for arquivo in base_path.rglob("metadata.yml")}
        return diretorios

    def mostrar_tags():
        pass

    def mostrar_datasets():
        pass

    def mostrar_instituicoes():
        pass

    def filtrar_datasets_por_tag():
        pass

    def filtrar_datasets_por_descricao():
        pass

    def filtrar_datasets_por_instituicao():
        pass

    def filtrar_datasets_por_formato():
        pass