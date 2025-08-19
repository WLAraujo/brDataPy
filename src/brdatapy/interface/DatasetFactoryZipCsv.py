from abc import ABC, abstractmethod
from brdatapy.interface.DatasetFactory import DatasetFactory
from pathlib import Path
import inspect
import yaml

class DatasetFactoryZipCsv(DatasetFactory):
    """Classe de dados usada como implementação específica da factory de datasets para datasets em que a forma de obtenção seja um ou mais arquivos no formato csv dentro de um zip.
    Datasets em que a forma de obtenção seja
    """