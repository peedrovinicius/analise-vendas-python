"""Gera e valida um manifesto criptográfico dos arquivos brutos da Olist."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

from src.ingestion.olist import EXPECTED_FILES, validate_source_directory

DATASET_SLUG = "olistbr/brazilian-ecommerce"
KAGGLE_VERSION = 2
MANIFEST_FORMAT_VERSION = 1


def sha256_file(path: Path) -> str:
    """Calcula SHA-256 sem carregar o arquivo inteiro em memória."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def count_data_rows(path: Path) -> int:
    """Conta registros CSV lógicos desconsiderando o cabeçalho."""
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        row_count = sum(1 for _ in reader)
    return max(row_count - 1, 0)


def build_manifest(data_dir: str | Path) -> dict[str, object]:
    """Cria o manifesto dos nove arquivos esperados."""
    directory = Path(data_dir)
    validate_source_directory(directory)

    files: dict[str, dict[str, object]] = {}
    for file_name in EXPECTED_FILES:
        path = directory / file_name
        files[file_name] = {
            "sha256": sha256_file(path),
            "size_bytes": path.stat().st_size,
            "data_rows": count_data_rows(path),
        }

    return {
        "manifest_format_version": MANIFEST_FORMAT_VERSION,
        "dataset": DATASET_SLUG,
        "kaggle_version": KAGGLE_VERSION,
        "hash_algorithm": "sha256",
        "files": files,
    }


def write_manifest(data_dir: str | Path, manifest_path: str | Path) -> None:
    """Grava um manifesto determinístico em JSON."""
    manifest = build_manifest(data_dir)
    destination = Path(manifest_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def validate_manifest(data_dir: str | Path, manifest_path: str | Path) -> None:
    """Confere nomes, tamanho, linhas e SHA-256 contra um manifesto salvo."""
    directory = Path(data_dir)
    validate_source_directory(directory)

    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    if manifest.get("manifest_format_version") != MANIFEST_FORMAT_VERSION:
        raise ValueError("Versão do formato do manifesto não suportada.")
    if manifest.get("dataset") != DATASET_SLUG:
        raise ValueError("Manifesto pertence a outro dataset.")
    if manifest.get("kaggle_version") != KAGGLE_VERSION:
        raise ValueError("Versão do dataset Kaggle divergente.")
    if manifest.get("hash_algorithm") != "sha256":
        raise ValueError("Algoritmo de hash do manifesto não é SHA-256.")

    expected = manifest.get("files")
    if not isinstance(expected, dict):
        raise ValueError("Manifesto sem mapa válido de arquivos.")

    if set(expected) != set(EXPECTED_FILES):
        raise ValueError("Manifesto não contém exatamente os nove arquivos esperados.")

    errors: list[str] = []
    for file_name in EXPECTED_FILES:
        recorded = expected[file_name]
        if not isinstance(recorded, dict):
            errors.append(f"{file_name}: entrada inválida no manifesto")
            continue

        path = directory / file_name
        actual_size = path.stat().st_size
        actual_rows = count_data_rows(path)
        actual_sha256 = sha256_file(path)

        if recorded.get("size_bytes") != actual_size:
            errors.append(f"{file_name}: tamanho divergente")
        if recorded.get("data_rows") != actual_rows:
            errors.append(f"{file_name}: quantidade de linhas divergente")
        if recorded.get("sha256") != actual_sha256:
            errors.append(f"{file_name}: SHA-256 divergente")

    if errors:
        raise ValueError("Falha de integridade da fonte:\n- " + "\n- ".join(errors))


def _default_paths() -> tuple[Path, Path]:
    project_root = Path(__file__).resolve().parents[1]
    return project_root / "dados" / "raw", project_root / "dados" / "source-manifest.json"


def main() -> None:
    """Executa geração ou validação do manifesto pela linha de comando."""
    default_data_dir, default_manifest = _default_paths()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("generate", "validate"))
    parser.add_argument("--data-dir", type=Path, default=default_data_dir)
    parser.add_argument("--manifest", type=Path, default=default_manifest)
    args = parser.parse_args()

    if args.command == "generate":
        write_manifest(args.data_dir, args.manifest)
        print(f"Manifesto gravado em {args.manifest}")
        return

    validate_manifest(args.data_dir, args.manifest)
    print("Integridade dos arquivos brutos validada com sucesso.")


if __name__ == "__main__":
    main()
