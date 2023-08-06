from setuptools import setup, find_packages
from pathlib import Path

setup(
      name = 'pro-video-Ferramentas-teste_inicial',
      version = 1.0,
      description = 'Este pacote fornecerá ferramentas de processamento de vídeo',
      long_description = Path('README.md').read_text(),
      author = 'Lucas',
      author_email = 'lucas.edu.leme@hotmail.com',
      keywords = ['camera', 'video', 'processamento'],
      packages = find_packages()
)

