"""Configuração central de logging."""

import logging


def get_logger(name: str, level: str = "INFO") -> logging.Logger:
    """Cria (ou reaproveita) um logger configurado no padrão do projeto."""
    logging.basicConfig(
        level=getattr(logging, level, logging.INFO),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger(name)
