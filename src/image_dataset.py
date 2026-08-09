"""Ponto de entrada: executa o pipeline de organização do dataset de imagens."""

import sys

from application.image_processor import ImageProcessor
from core.config import ProcessorConfig


def main() -> None:
    """Executa o processamento completo e imprime um resumo no terminal."""
    print("🚀 Iniciando processamento de imagens...")
    print("=" * 50)
    print("📄 Usando configurações do arquivo .env")
    print("=" * 50)

    config = ProcessorConfig()
    processor = ImageProcessor(config)

    try:
        json_path, csv_path = processor.process(verbose=True)
        stats = processor.get_statistics()

        print("\n" + "=" * 50)
        print("📊 RESUMO DO PROCESSAMENTO")
        print("=" * 50)
        print(f"✅ Total de imagens: {stats.total}")
        print(f"💾 Tamanho total: {stats.total_size_mb:.2f} MB")
        print(f"📁 Classificações: {len(stats.classifications)}")

        if stats.classifications:
            print("\n📂 Distribuição por classificação:")
            for cls, count in sorted(stats.classifications.items()):
                print(f"   • {cls}: {count} imagens")

        if stats.extensions:
            print("\n📄 Extensões:")
            for ext, count in sorted(stats.extensions.items()):
                print(f"   • {ext}: {count} arquivos")

        print("\n" + "=" * 50)
        print("✅ Processamento concluído com sucesso!")
        print(f"📄 JSON: {json_path}")
        print(f"📄 CSV: {csv_path}")
        print("=" * 50)

    except (FileNotFoundError, OSError) as exc:
        print(f"\n❌ ERRO: {exc}")
        print("\n🔧 Verifique se:")
        print("   1. A pasta 'data/raw' existe")
        print("   2. Há subpastas com imagens dentro de 'data/raw'")
        print("   3. As extensões são suportadas")
        print("   4. O arquivo .env está configurado corretamente")
        sys.exit(1)


if __name__ == "__main__":
    main()
