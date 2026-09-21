"""Baixa o dataset oficial de candidatos do TSE (Portal de Dados Abertos).

O CDN do TSE (cdn.tse.jus.br) fica atrás de um WAF/Akamai que costuma
recusar clientes não-navegador (curl, requests) mesmo a partir de IPs
legítimos. Se o download automático falhar com 403, baixe o arquivo
manualmente pelo navegador e salve em data/raw/, ou rode este script de
novo depois de colocar o arquivo lá (ele pula o download se já existir).
"""
import sys

import requests

from . import config

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    ),
    "Accept": "application/zip,application/octet-stream,*/*",
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
    "Referer": config.DATASET_PAGE_URL,
}


def baixar(force: bool = False) -> bool:
    """Retorna True se o zip está disponível em disco ao final da chamada."""
    config.RAW_DIR.mkdir(parents=True, exist_ok=True)

    if config.ZIP_PATH.exists() and not force:
        print(f"Já existe: {config.ZIP_PATH} (use force=True para rebaixar)")
        return True

    print(f"Baixando {config.DATASET_ZIP_URL} ...")
    try:
        resp = requests.get(
            config.DATASET_ZIP_URL, headers=HEADERS, timeout=60
        )
    except requests.RequestException as exc:
        print(f"Falha de rede ao baixar: {exc}", file=sys.stderr)
        _instrucoes_manuais()
        return False

    if resp.status_code != 200 or not resp.content.startswith(b"PK"):
        print(
            f"Download automático bloqueado (HTTP {resp.status_code}).",
            file=sys.stderr,
        )
        _instrucoes_manuais()
        return False

    config.ZIP_PATH.write_bytes(resp.content)
    print(f"Salvo em {config.ZIP_PATH} ({len(resp.content):,} bytes)")
    return True


def _instrucoes_manuais() -> None:
    print(
        "\nBaixe manualmente pelo navegador e salve neste caminho:\n"
        f"  URL:    {config.DATASET_ZIP_URL}\n"
        f"  Página: {config.DATASET_PAGE_URL}\n"
        f"  Destino: {config.ZIP_PATH}\n",
        file=sys.stderr,
    )


if __name__ == "__main__":
    ok = baixar(force="--force" in sys.argv)
    sys.exit(0 if ok else 1)
