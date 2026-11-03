#!/usr/bin/env python3
"""Organiza os arquivos de uma pasta em subpastas por tipo.

Exemplos:
    python organizar_arquivos.py ~/Downloads --simular   # só mostra o que faria
    python organizar_arquivos.py ~/Downloads             # move os arquivos
"""

import argparse
import shutil
from pathlib import Path

CATEGORIAS = {
    "Imagens": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".heic"},
    "Documentos": {".pdf", ".doc", ".docx", ".txt", ".odt", ".rtf", ".md"},
    "Planilhas": {".xls", ".xlsx", ".csv", ".ods"},
    "Apresentacoes": {".ppt", ".pptx", ".odp"},
    "Videos": {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".webm"},
    "Audios": {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"},
    "Compactados": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Codigo": {".py", ".js", ".html", ".css", ".json", ".java", ".c", ".cpp", ".sh"},
}
OUTROS = "Outros"


def categoria_do_arquivo(arquivo: Path) -> str:
    extensao = arquivo.suffix.lower()
    for categoria, extensoes in CATEGORIAS.items():
        if extensao in extensoes:
            return categoria
    return OUTROS


def destino_sem_conflito(destino: Path) -> Path:
    """Se já existir um arquivo com o mesmo nome, adiciona ' (1)', ' (2)'..."""
    if not destino.exists():
        return destino
    contador = 1
    while True:
        candidato = destino.with_name(f"{destino.stem} ({contador}){destino.suffix}")
        if not candidato.exists():
            return candidato
        contador += 1


def organizar(pasta: Path, simular: bool = False) -> dict:
    """Move os arquivos da pasta (sem entrar em subpastas) para pastas por tipo."""
    resumo = {}
    for arquivo in sorted(pasta.iterdir()):
        if not arquivo.is_file() or arquivo.name.startswith("."):
            continue
        categoria = categoria_do_arquivo(arquivo)
        destino = destino_sem_conflito(pasta / categoria / arquivo.name)
        print(f"{'[simulação] ' if simular else ''}{arquivo.name} -> {categoria}/{destino.name}")
        if not simular:
            destino.parent.mkdir(exist_ok=True)
            shutil.move(str(arquivo), str(destino))
        resumo[categoria] = resumo.get(categoria, 0) + 1
    return resumo


def main():
    parser = argparse.ArgumentParser(description="Organiza arquivos de uma pasta por tipo.")
    parser.add_argument("pasta", type=Path, help="pasta a organizar")
    parser.add_argument("--simular", action="store_true", help="mostra o que seria feito sem mover nada")
    args = parser.parse_args()

    pasta = args.pasta.expanduser().resolve()
    if not pasta.is_dir():
        parser.error(f"'{pasta}' não é uma pasta válida")

    resumo = organizar(pasta, args.simular)
    total = sum(resumo.values())
    if total == 0:
        print("Nenhum arquivo para organizar.")
        return
    print(f"\n{total} arquivo(s) {'seriam movidos' if args.simular else 'movidos'}:")
    for categoria, quantidade in sorted(resumo.items()):
        print(f"  {categoria}: {quantidade}")


if __name__ == "__main__":
    main()
          
