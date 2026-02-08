#!/usr/bin/env python3
"""
Script para rodar pytest programaticamente.
Equivalente a executar: python -m pytest
Compatível com Windows, macOS e Linux.
"""

import sys

import pytest


def main():
    # Permite passar argumentos para pytest (ex: --verbose, diretórios, etc)
    # Exemplo de uso:
    #   python run_tests.py --maxfail=1 -q
    # é equivalente a:
    #   python -m pytest --maxfail=1 -q
    args = sys.argv[1:]

    # Executa pytest com os argumentos recebidos
    # Retorna o código de saída para compatibilidade com CI/CD
    exit_code = pytest.main(args)

    # Finaliza o script com o mesmo código de saída do pytest
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
