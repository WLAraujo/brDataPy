from pathlib import Path

def validar_informacoes_basicas():
    """Esse método recebe um nome de arquivo e valida as informações básicas obrigatórias dele
    """

def test_listar_arquivos():
    # Caminho para a pasta src (relativo à raiz do projeto)
    src_path = Path(__file__).resolve().parents[1] / "src"

    # Lista todos os arquivos dentro de src (recursivamente)
    arquivos = [str(p.relative_to(src_path)) for p in src_path.rglob("*") if p.is_file()]

    print("\nArquivos encontrados em src:")
    for arquivo in arquivos:
        print(arquivo)

    # Exemplo de assert para validar que encontrou algo
    assert len(arquivos) > 0

test_listar_arquivos()