"""Lógica pura de split estratificado (por classe) e cópia dos arquivos."""

import random
import shutil
from pathlib import Path
from typing import Dict, List

from core.models import ImageRecord

_SPLITS = ("train", "val", "test")


class DatasetSplitter:
    """Divide uma lista de ImageRecord em train/val/test, mantendo proporção por classe."""

    def __init__(self, train_ratio: float, val_ratio: float, test_ratio: float, seed: int) -> None:
        self.train_ratio = train_ratio
        self.val_ratio = val_ratio
        self.test_ratio = test_ratio
        self.seed = seed

    def split_by_class(
        self, records: List[ImageRecord]
    ) -> Dict[str, Dict[str, List[ImageRecord]]]:
        """
        Agrupa os registros por classe e divide cada grupo em train/val/test.

        Retorna algo como:
        {"Dark": {"train": [...], "val": [...], "test": [...]}, "Green": {...}}

        Nota: a divisão é feita por classe (pra manter a proporção certa),
        mas o resultado depois é misturado ao copiar (ver copy_split).
        """
        by_class: Dict[str, List[ImageRecord]] = {}
        for record in records:
            by_class.setdefault(record.classification, []).append(record)

        result: Dict[str, Dict[str, List[ImageRecord]]] = {}
        rng = random.Random(self.seed)

        for classification, items in by_class.items():
            shuffled = items[:]
            rng.shuffle(shuffled)

            n_total = len(shuffled)
            n_train = round(n_total * self.train_ratio)
            n_val = round(n_total * self.val_ratio)

            result[classification] = {
                "train": shuffled[:n_train],
                "val": shuffled[n_train : n_train + n_val],
                "test": shuffled[n_train + n_val :],
            }

        return result

    @staticmethod
    def copy_split(
        split_data: Dict[str, Dict[str, List[ImageRecord]]], output_dir: Path
    ) -> None:
        """Copia os arquivos para output_dir/<split>/arquivo.ext, todas as classes juntas."""
        for split_name in _SPLITS:
            dest_dir = output_dir / split_name
            dest_dir.mkdir(parents=True, exist_ok=True)

            for splits in split_data.values():
                for record in splits[split_name]:
                    dest_path = dest_dir / record.new_name
                    shutil.copy2(record.new_path, dest_path)