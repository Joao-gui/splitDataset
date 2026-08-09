# splitDataset

Ferramenta para organizar datasets de imagens classificadas: renomeia os arquivos com o padrão `data_hora_id`, copia para uma pasta de saída padronizada e gera um mapeamento completo em JSON e CSV.

## Estrutura do projeto

```
splitDataset/
├── application/        # Orquestração e regras de negócio
│   ├── image_processor.py   # Classe principal (ImageProcessor)
│   └── report_writer.py     # Geração dos relatórios JSON/CSV
├── core/                # Modelos e configuração do domínio
│   ├── models.py             # Dataclasses (ImageRecord, ProcessingStats)
│   └── config.py             # ProcessorConfig (lê o .env)
├── infra/                # Acesso a recursos externos (I/O)
│   ├── file_repository.py    # Encontrar/copiar arquivos em disco
│   └── logger.py             # Configuração de logging
├── src/
│   └── image_dataset.py     # Ponto de entrada (main)
├── data/
│   ├── raw/              # Imagens originais, organizadas em subpastas por classe
│   └── custom/            # Imagens processadas (saída)
├── scripts/
├── .env
└── README.md
```

Cada subpasta de `data/raw/` é tratada como uma classificação (ex: `Dark`, `Green`, `Light`, `Medium`). As imagens dentro delas são copiadas para `data/custom/` com nome padronizado, e o mapeamento completo é salvo em `data/image_mapping.json` e `data/image_mapping.csv`.

## Requisitos

- Python 3.12.4
- Ambiente virtual gerenciado via miniforge3

## Instalação

Priorizando mamba, depois conda, depois pip:

```bash
mamba install tqdm python-dotenv
# ou
conda install tqdm python-dotenv
# ou
pip install tqdm python-dotenv
```

## Configuração (.env)

Crie um arquivo `.env` na raiz do projeto (opcional — há valores padrão para tudo):

```env
# Configurações do ImageProcessor
INPUT_DIR=data/raw
OUTPUT_DIR=data/custom
MAPPING_DIR=data

# Extensões suportadas (separadas por vírgula)
SUPPORTED_EXTENSIONS=.jpg,.jpeg,.png,.bmp,.tiff,.webp,.gif

# Configurações de logging
LOG_LEVEL=INFO

# Configurações do splitamento e seed para reprodução
SPLIT_TRAIN_RATIO=0.70
SPLIT_VAL_RATIO=0.15
SPLIT_TEST_RATIO=0.15
SPLIT_SEED=42
```

## Uso

Execute sempre a partir da raiz do projeto, como módulo, para que os imports de `core`, `infra` e `application` sejam resolvidos corretamente:

```bash
python -m src.image_dataset
```

### Saída esperada

- `data/custom/`: imagens copiadas e renomeadas no padrão `AAAA_MM_DD_HHMMSS_NNNN.ext`
- `data/image_mapping.json`: metadados completos (data do processamento, diretórios, resumo por classificação e lista de todas as imagens)
- `data/image_mapping.csv`: mesma informação em formato tabular

Ao final, um resumo é impresso no terminal com o total de imagens, tamanho total em MB e a distribuição por classificação e extensão.

## Notas de arquitetura

- **`core`**: dataclasses e configuração — não sabe nada sobre disco ou I/O.
- **`infra`**: só lida com sistema de arquivos (encontrar, copiar, criar diretórios).
- **`application`**: conecta `core` e `infra` para executar o processamento e gerar os relatórios.
- **`src`**: ponto de entrada, sem lógica de negócio.

Dicionários (`dict`) só aparecem na borda, na hora de serializar para JSON/CSV — internamente os dados trafegam como dataclasses (`ImageRecord`, `ProcessingStats`, `ProcessorConfig`), com type hints em todas as assinaturas, para aproveitar a checagem do pylint.
