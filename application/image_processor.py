"""Orquestra o processamento de um dataset de imagens classificadas."""

from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

from tqdm import tqdm

from application.report_writer import ReportWriter
from core.config import ProcessorConfig
from core.models import ImageRecord, ProcessingStats
from infra.file_repository import FileRepository
from infra.logger import get_logger


class ImageProcessor:
    """Processador de imagens para datasets classificados."""

    def __init__(self, config: Optional[ProcessorConfig] = None) -> None:
        self.config = config or ProcessorConfig()
        self.logger = get_logger(__name__, self.config.log_level)
        self.repository = FileRepository(self.config.supported_extensions)
        self.report_writer = ReportWriter(self.config.mapping_dir)
        self.records: List[ImageRecord] = []

        self.logger.info("📁 Diretório de entrada: %s", self.config.input_dir)
        self.logger.info("📁 Diretório de saída: %s", self.config.output_dir)
        self.logger.info("📁 Diretório de mapeamento: %s", self.config.mapping_dir)
        self.logger.info("📄 Extensões suportadas: %s", self.config.supported_extensions)

    def process(self, verbose: bool = True) -> Tuple[Path, Path]:
        """Processa todas as imagens e retorna os caminhos do JSON e CSV gerados."""
        if not self.config.input_dir.exists():
            raise FileNotFoundError(
                f"Diretório de entrada não encontrado: {self.config.input_dir}"
            )

        self.repository.ensure_dirs(self.config.output_dir, self.config.mapping_dir)

        image_files = self.repository.find_images(self.config.input_dir)
        if not image_files:
            self.logger.warning("Nenhuma imagem encontrada para processar.")
            return Path(), Path()

        self.logger.info("Encontradas %d imagens para processar.", len(image_files))

        for img_path, classification in tqdm(
            image_files, desc="Processando imagens", disable=not verbose
        ):
            self._process_image(img_path, classification)

        json_path = self.report_writer.write_json(
            self.records, self.config.input_dir, self.config.output_dir
        )
        csv_path = self.report_writer.write_csv(self.records)

        self.logger.info("✅ Processamento concluído!")
        self.logger.info("📄 JSON: %s", json_path)
        self.logger.info("📄 CSV: %s", csv_path)

        return json_path, csv_path

    def _process_image(self, img_path: Path, classification: str) -> None:
        """Copia, renomeia e registra uma única imagem."""
        timestamp = datetime.now().strftime("%Y_%m_%d_%H%M%S")
        extension = img_path.suffix.lower()
        counter = len(self.records) + 1
        new_name = f"{timestamp}_{str(counter).zfill(4)}{extension}"
        dest_path = self.config.output_dir / new_name

        try:
            self.repository.copy_image(img_path, dest_path)
            self.records.append(
                ImageRecord(
                    id=counter,
                    timestamp=timestamp,
                    new_name=new_name,
                    classification=classification,
                    original_path=img_path,
                    original_name=img_path.name,
                    new_path=dest_path,
                    extension=extension,
                    size_bytes=img_path.stat().st_size,
                )
            )
        except OSError as exc:
            self.logger.error("❌ Erro ao processar %s: %s", img_path.name, exc)

    def get_statistics(self) -> ProcessingStats:
        """Retorna estatísticas agregadas do processamento, como dataclass."""
        if not self.records:
            return ProcessingStats()

        stats = ProcessingStats(
            total=len(self.records),
            total_size_mb=sum(r.size_bytes for r in self.records) / (1024 * 1024),
        )

        for record in self.records:
            stats.classifications[record.classification] = (
                stats.classifications.get(record.classification, 0) + 1
            )
            stats.extensions[record.extension] = stats.extensions.get(record.extension, 0) + 1

        return stats
