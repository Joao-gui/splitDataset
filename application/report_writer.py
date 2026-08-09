"""Geração dos artefatos de saída (JSON e CSV) a partir dos registros processados."""

import csv
import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from core.models import ImageRecord

_CSV_FIELDS = [
    "id", "new_name", "classification", "original_name",
    "original_path", "extension", "size_bytes",
]


class ReportWriter:
    """Gera relatórios (JSON/CSV) a partir de uma lista de ImageRecord."""

    def __init__(self, mapping_dir: Path) -> None:
        self.mapping_dir = mapping_dir

    def write_json(self, records: List[ImageRecord], input_dir: Path, output_dir: Path) -> Path:
        """Escreve o mapeamento completo em JSON e retorna o caminho gerado."""
        output_file = self.mapping_dir / "image_mapping.json"

        summary: Dict[str, int] = {}
        for record in records:
            summary[record.classification] = summary.get(record.classification, 0) + 1

        data = {
            "metadata": {
                "processed_date": datetime.now().isoformat(),
                "input_dir": str(input_dir),
                "output_dir": str(output_dir),
                "total_images": len(records),
                "total_classifications": len(summary),
            },
            "summary": summary,
            "images": [self._record_to_dict(r) for r in records],
        }

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return output_file

    def write_csv(self, records: List[ImageRecord]) -> Path:
        """Escreve o mapeamento em CSV e retorna o caminho gerado."""
        output_file = self.mapping_dir / "image_mapping.csv"

        if not records:
            return output_file

        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=_CSV_FIELDS)
            writer.writeheader()
            for record in records:
                row = self._record_to_dict(record)
                writer.writerow({k: row.get(k, "") for k in _CSV_FIELDS})

        return output_file

    @staticmethod
    def _record_to_dict(record: ImageRecord) -> dict:
        """Converte o dataclass em dict só na hora de serializar (JSON/CSV)."""
        row = asdict(record)
        row["original_path"] = str(record.original_path)
        row["new_path"] = str(record.new_path)
        return row
