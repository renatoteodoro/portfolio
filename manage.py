#!/usr/bin/env python
"""Utilitario de linha de comando Django para tarefas administrativas."""
import os
import sys


def main():
    """Executa tarefas administrativas."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Nao foi possivel importar o Django. Verifique se ele esta "
            "instalado e disponivel no ambiente virtual ativo."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
