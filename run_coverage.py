#!/usr/bin/env python3
"""
Script para rodar cobertura de testes com Coverage.py.
Equivalente a:
    coverage run -m pytest
    coverage report -m
Compatível com Windows, macOS e Linux.
"""

import sys
import subprocess

def main():
    python_exec = sys.executable  # Garante o uso do mesmo Python do ambiente atual

    try:
        # 1️⃣ Executa testes com coverage, equivalente a "coverage run -m pytest"
        print("🔹 Executando testes com cobertura...")
        subprocess.run(
            [python_exec, "-m", "coverage", "run", "-m", "pytest"],
            check=True
        )

        # 2️⃣ Gera o relatório no terminal, equivalente a "coverage report -m"
        print("\n🔹 Gerando relatório de cobertura:\n")
        subprocess.run(
            [python_exec, "-m", "coverage", "report", "-m"],
            check=True
        )

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erro durante a execução: {e}")
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        print("\n🛑 Execução interrompida pelo usuário.")
        sys.exit(1)

if __name__ == "__main__":
    main()
