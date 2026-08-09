"""Operações de I/O em disco: encontrar, copiar e organizar imagens."""

import shutil
from pathlib import Path
from typing import List, Set, Tuple


class FileRepository:
    """Encapsula todo o acesso ao sistema de arquivos usado pelo processador."""

    def __init__(self, supported_extensions: Set[str]) -> None:
        self.supported_extensions = supported_extensions

    def find_images(self, input_dir: Path) -> List[Tuple[Path, str]]:
        """Encontra imagens nas subpastas de input_dir; cada subpasta é uma classe."""
        images: List[Tuple[Path, str]] = []

        for item in input_dir.iterdir():
            if not item.is_dir():
                continue
            classification = item.name
            for file_path in item.rglob("*"):
                if file_path.is_file() and file_path.suffix.lower() in self.supported_extensions:
                    images.append((file_path, classification))

        return images

    @staticmethod
    def ensure_dirs(*dirs: Path) -> None:
        """Cria os diretórios informados caso não existam."""
        for directory in dirs:
            directory.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def copy_image(src: Path, dest: Path) -> None:
        """Copia a imagem preservando metadados."""
        shutil.copy2(src, dest)
