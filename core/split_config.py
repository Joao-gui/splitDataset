"""Configuração do split de dataset em train/val/test."""

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass
class SplitConfig:
    """Configuração para dividir o dataset classificado em train/val/test."""

    mapping_json: Path = field(
        default_factory=lambda: Path(os.getenv("MAPPING_JSON", "data/image_mapping.json"))
    )
    output_dir: Path = field(
        default_factory=lambda: Path(os.getenv("SPLIT_OUTPUT_DIR", "data/split"))
    )
    train_ratio: float = field(
        default_factory=lambda: float(os.getenv("SPLIT_TRAIN_RATIO", "0.70"))
    )
    val_ratio: float = field(
        default_factory=lambda: float(os.getenv("SPLIT_VAL_RATIO", "0.15"))
    )
    test_ratio: float = field(
        default_factory=lambda: float(os.getenv("SPLIT_TEST_RATIO", "0.15"))
    )
    seed: int = field(default_factory=lambda: int(os.getenv("SPLIT_SEED", "42")))

    def __post_init__(self) -> None:
        total = round(self.train_ratio + self.val_ratio + self.test_ratio, 4)
        if total != 1.0:
            raise ValueError(
                f"As proporções train+val+test devem somar 1.0 (soma atual: {total})"
            )