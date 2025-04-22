# scielo-file-report

Script em Python para gerar relatórios CSV com informações de arquivos `.xml`, `.pdf` presentes em estruturas de diretórios da SciELO.

## Estrutura esperada de diretórios

```bash
# Para arquivos XML:
<base_dir>/<acronimo>/<volume_numero>/file.xml

# Para arquivos PDF:
<base_dir>/<acronimo>/<volume_numero>/file.pdf
```

---

## Funcionalidades

- Percorre diretórios base por acrônimos (`bwho`, `csc`, etc.)
- Filtra arquivos pela extensão desejada (`.xml` ou `.pdf`)
- Cria o diretório `output/` automaticamente (se não existir)
- Gera nome de arquivo CSV automaticamente com base na extensão e data/hora
- Extrai:
  - Acrônimo
  - Caminho completo
  - Volume (nome da pasta de volume)
  - Nome do arquivo
  - Data de modificação (YYYY-MM-DD)
  - Tamanho em bytes

---

## Como usar

### Pré-requisitos

- Python 3.6+
- Nenhuma dependência externa

### Parâmetros

| Parâmetro      | Obrigatório | Descrição                                                           |
|----------------|-------------|---------------------------------------------------------------------|
| `--base-dir`   | Sim         | Caminho até a pasta `/bases` (ex: `/var/www/site_scielo/bases`)     |
| `--ext`        | Não         | Extensão dos arquivos desejados (`xml` ou `pdf`) — padrão: `xml`    |
| `--acron-file` | Não         | Arquivo `.txt` com acrônimos (um por linha).                        |

Se `--acron-file` não for informado o script detecta automaticamente os acrônimos de `<root>`

### Exemplo com lista de acrônimos

```bash
python3 scielo-file-report.py --base-dir /var/www/site_scielo/bases/xml --acron-file acrons.txt --ext xml --output relatorio_xml.csv
```

### Exemplo automático (sem lista de acrônimos)

```bash
python3 scielo-file-report.py --base-dir /var/www/site_scielo/bases/pdf --ext pdf --output relatorio_pdf.csv
```

### Exemplo para excecução em Crontab

```bash
nohup python3 scielo-file-report.py --base-dir var/www/site_scielo/bases/ --ext xml > /tmp/log-scielo-file-report.txt 2>&1 &
```
---

## Formato de saída do CSV

O arquivo CSV será salvo automaticamente no diretório `output/`, com nome como:

`xml_2025-04-22__1911.csv` ou `pdf_2025-04-22__1911.csv`

```csv
acron;path;vol_num;file_name;file_date;file_size
bwho;/var/www/site_scielo/bases/xml/bwho/v91n10/;v91n10;0042-9686-bwho-91-10-718.xml;2015-08-04;18213
```
