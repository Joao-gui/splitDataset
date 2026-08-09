"""Ponto de entrada: divide o dataset em data/split/train, val e test."""

import sys

from application.split_service import SplitService
from core.split_config import SplitConfig


def main() -> None:
    """Executa o split e imprime um resumo por classe no terminal."""
    print("🚀 Iniciando split do dataset (train/val/test)...")
    print("=" * 50)

    config = SplitConfig()

    try:
        split_data = SplitService(config).run()

        print("\n" + "=" * 50)
        print("📊 RESUMO DO SPLIT")
        print("=" * 50)

        totals = {"train": 0, "val": 0, "test": 0}

        for classification, splits in sorted(split_data.items()):
            n_train = len(splits["train"])
            n_val = len(splits["val"])
            n_test = len(splits["test"])
            n_total = n_train + n_val + n_test

            totals["train"] += n_train
            totals["val"] += n_val
            totals["test"] += n_test

            print(f"\n📂 {classification} ({n_total} imagens)")
            print(f"   • train: {n_train}")
            print(f"   • val:   {n_val}")
            print(f"   • test:  {n_test}")

        print("\n" + "-" * 50)
        print(f"✅ Total train: {totals['train']}")
        print(f"✅ Total val:   {totals['val']}")
        print(f"✅ Total test:  {totals['test']}")
        print(f"📁 Saída: {config.output_dir}")
        print("=" * 50)

    except (FileNotFoundError, ValueError) as exc:
        print(f"\n❌ ERRO: {exc}")
        print("\n🔧 Verifique se:")
        print("   1. O arquivo data/image_mapping.json existe")
        print("      (rode antes: python -m src.image_dataset)")
        print("   2. As proporções em SplitConfig somam 1.0")
        sys.exit(1)


if __name__ == "__main__":
    main()