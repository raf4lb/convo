#!/usr/bin/env python3
"""
Script para formatar o código usando Ruff.
Equivalente a: ruff format [ARGS...]
Exemplo de uso:
    python run_formatter.py .
    python run_formatter.py --check .
    python run_formatter.py --diff src/
Compatível com Windows, macOS e Linux.
"""

import subprocess
import sys


def main():
    python_exec = sys.executable  # Garante o uso do mesmo Python do ambiente atual

    # Repassa todos os argumentos fornecidos para o Ruff
    args = sys.argv[1:] or ["."]
    cmd = [python_exec, "-m", "ruff", "format", *args]

    try:
        print(f"🔹 Executando: {' '.join(cmd)}\n")
        subprocess.run(cmd, check=True)
        print("\n✅ Código formatado com sucesso!")

    except subprocess.CalledProcessError as e:
        # Ruff retorna código diferente de 0 se detectar problemas ou rodar com --check
        print("\n⚠️  Ruff detectou diferenças de formatação.")
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        print("\n🛑 Execução interrompida pelo usuário.")
        sys.exit(1)


if __name__ == "__main__":
    main()
