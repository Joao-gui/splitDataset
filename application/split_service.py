"""Orquestra a leitura do mapeamento e a execução do split train/val/test."""

import json
from pathlib import Path
from typing import Dict, List

from core.models import ImageRecord
from core.split_config import SplitConfig
from infra.dataset_splitter import DatasetSplitter
from infra.logger import get_logger


class SplitService:
    """Lê o image_mapping.json, reconstrói os ImageRecord e executa o split."""

    def __init__(self, config: SplitConfig) -> None:
        self.config = config
        self.logger = get_logger(__name__)
        self.splitter = DatasetSplitter(
            train_ratio=config.train_ratio,
            val_ratio=config.val_ratio,
            test_ratio=config.test_ratio,
            seed=config.seed,
        )

    def run(self) -> Dict[str, Dict[str, List[ImageRecord]]]:
        """Executa o pipeline completo: carregar mapeamento -> splitar -> copiar."""
        if not self.config.mapping_json.exists():
            raise FileNotFoundError(
                f"Arquivo de mapeamento não encontrado: {self.config.mapping_json}"
            )

        records = self._load_records()
        self.logger.info(
            "Carregados %d registros de %s", len(records), self.config.mapping_json
        )

        split_data = self.splitter.split_by_class(records)
        self.splitter.copy_split(split_data, self.config.output_dir)

        self.logger.info("✅ Split concluído em: %s", self.config.output_dir)
        return split_data

    def _load_records(self) -> List[ImageRecord]:
        """Lê o JSON e reconstrói os ImageRecord (strings viram Path de novo)."""
        with open(self.config.mapping_json, "r", encoding="utf-8") as f:
            data = json.load(f)

        records: List[ImageRecord] = []
        for item in data["images"]:
            records.append(
                ImageRecord(
                    id=item["id"],
                    timestamp=item["timestamp"],
                    new_name=item["new_name"],
                    classification=item["classification"],
                    original_path=Path(item["original_path"]),
                    original_name=item["original_name"],
                    new_path=Path(item["new_path"]),
                    extension=item["extension"],
                    size_bytes=item["size_bytes"],
                )
            )

        return records