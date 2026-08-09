"""Modelos de dados (dataclasses) usados no domínio de processamento de imagens."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict


@dataclass
class ImageRecord:
    """Registro de uma imagem processada (substitui o antigo dict solto)."""

    id: int
    timestamp: str
    new_name: str
    classification: str
    original_path: Path
    original_name: str
    new_path: Path
    extension: str
    size_bytes: int


@dataclass
class ProcessingStats:
    """Estatísticas agregadas de um processamento."""

    total: int = 0
    classifications: Dict[str, int] = field(default_factory=dict)
    extensions: Dict[str, int] = field(default_factory=dict)
    total_size_mb: float = 0.0
