#!/usr/bin/env python3
"""
Script para rodar o linter Ruff de forma agnóstica ao sistema operacional.
Equivalente a: ruff check [ARGS...]
Exemplo de uso:
    python run_linter.py .
    python run_linter.py --fix .
    python run_linter.py src/ --select E,F
Compatível com Windows, macOS e Linux.
"""

import subprocess
import sys


def main():
    python_exec = sys.executable  # Usa o mesmo Python do ambiente atual

    # Todos os argumentos após o nome do script são repassados ao Ruff
    args = sys.argv[1:] or ["."]
    cmd = [python_exec, "-m", "ruff", "check", *args]

    try:
        print(f"🔹 Executando: {' '.join(cmd)}\n")
        subprocess.run(cmd, check=True)
        print("\n✅ Nenhum problema encontrado pelo Ruff!")
    except subprocess.CalledProcessError as e:
        # Ruff retorna código diferente de 0 se encontrar problemas
        print("\n⚠️  Ruff encontrou problemas no código.")
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        print("\n🛑 Execução interrompida pelo usuário.")
        sys.exit(1)


if __name__ == "__main__":
    main()
