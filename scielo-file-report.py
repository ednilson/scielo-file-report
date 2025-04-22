import os
import csv
import datetime
import argparse
import sys


def ler_acronimos_arquivo(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            return [linha.strip() for linha in f if linha.strip()]
    except FileNotFoundError:
        print(f"Arquivo de acrônimos não encontrado: {caminho_arquivo}")
        sys.exit(1)


def listar_acronimos_automaticamente(root_dir):
    try:
        return [d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))]
    except Exception as e:
        print(f"Erro ao listar diretórios em {root_dir}: {e}")
        sys.exit(1)


def gerar_nome_csv(ext, output_dir="output"):
    now = datetime.datetime.now().strftime('%Y-%m-%d__%H%M')
    print("Data e hora: ", now)
    filename = f"{ext.lower()}_{now}.csv"
    os.makedirs(output_dir, exist_ok=True)
    return os.path.join(output_dir, filename)


def coletar_dados(root_dir, list_acron, output_csv, file_ext):
    ext_with_dot = f".{file_ext.lower().strip().lstrip('.')}"

    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(['acron', 'path', 'vol_num', 'file_name', 'file_date', 'file_size'])

        for acron in list_acron:
            acron_path = os.path.join(root_dir, acron)
            if not os.path.isdir(acron_path):
                print(f"[!] Diretório não encontrado para acrônimo: {acron}")
                continue

            print(f"Processando acrônimo: {acron}")
            for dirpath, _, filenames in os.walk(acron_path):
                for file in filenames:
                    if file.lower().endswith(ext_with_dot):
                        full_path = os.path.join(dirpath, file)
                        try:
                            relative_path = os.path.relpath(full_path, start=root_dir)
                            parts = relative_path.split(os.sep)
                            volume_num = parts[1] if len(parts) >= 3 else ''
                            stats = os.stat(full_path)
                            creation_date = datetime.datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d')
                            file_size = stats.st_size

                            writer.writerow([
                                acron,
                                os.path.dirname(full_path) + '/',
                                volume_num,
                                file,
                                creation_date,
                                file_size
                            ])
                        except Exception as e:
                            print(f"Erro ao processar {full_path}: {e}")

    print(f"Relatório gerado com sucesso: {output_csv}")


def main():
    parser = argparse.ArgumentParser(description='scielo-file-reporter: Gera relatório de arquivos .xml ou .pdf por acrônimo e volume.')
    parser.add_argument('--base-dir', required=True, help='Diretório base até "/bases" (ex: /var/www/scielosp_org/bases).')
    parser.add_argument('--ext', required=True, help='Extensão dos arquivos desejados (ex: xml ou pdf).')
    parser.add_argument('--acron-file', help='Arquivo .txt contendo acrônimos (um por linha).')

    args = parser.parse_args()

    ext = args.ext.lower().strip().lstrip('.')
    if ext not in ['xml', 'pdf']:
        print(f"Extensão '{ext}' não suportada. Use 'xml' ou 'pdf'.")
        sys.exit(1)

    root_dir = os.path.join(args.base_dir, ext)

    output_csv = gerar_nome_csv(ext)

    if args.acron_file:
        list_acron = ler_acronimos_arquivo(args.acron_file)
    else:
        print(f"Nenhum arquivo de acrônimos informado. Detectando todos os diretórios diretamente em: {root_dir}")
        list_acron = listar_acronimos_automaticamente(root_dir)

    coletar_dados(root_dir, list_acron, output_csv, ext)


if __name__ == '__main__':
    main()
