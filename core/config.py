"""Configuração do processador, carregada de variáveis de ambiente (.env)."""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Set

from dotenv import load_dotenv

load_dotenv()


def _default_extensions() -> Set[str]:
    raw = os.getenv("SUPPORTED_EXTENSIONS", ".jpg,.jpeg,.png,.bmp,.tiff,.webp,.gif")
    return {ext.strip() for ext in raw.split(",")}


@dataclass
class ProcessorConfig:
    """Configuração do ImageProcessor. Valores default vêm do .env."""

    input_dir: Path = field(default_factory=lambda: Path(os.getenv("INPUT_DIR", "data/raw")))
    output_dir: Path = field(default_factory=lambda: Path(os.getenv("OUTPUT_DIR", "data/custom")))
    mapping_dir: Path = field(default_factory=lambda: Path(os.getenv("MAPPING_DIR", "data")))
    supported_extensions: Set[str] = field(default_factory=_default_extensions)
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO").upper())

    @classmethod
    def from_overrides(
        cls,
        input_dir: Optional[str] = None,
        output_dir: Optional[str] = None,
        mapping_dir: Optional[str] = None,
        supported_extensions: Optional[Set[str]] = None,
    ) -> "ProcessorConfig":
        """Cria a config priorizando valores explícitos sobre o .env."""
        cfg = cls()
        if input_dir is not None:
            cfg.input_dir = Path(input_dir)
        if output_dir is not None:
            cfg.output_dir = Path(output_dir)
        if mapping_dir is not None:
            cfg.mapping_dir = Path(mapping_dir)
        if supported_extensions is not None:
            cfg.supported_extensions = supported_extensions
        return cfg
