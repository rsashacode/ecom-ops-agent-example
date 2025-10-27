import os
import shutil
import tomllib
from pathlib import Path

import kagglehub

from pipelines._manifest import FILES


def load_cfg():
    with open("configs/settings.toml", "rb") as f:
        return tomllib.load(f)


def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)


def download(slug: str, raw_dir: Path) -> dict[str, str]:
    abs_path = str(Path(raw_dir).resolve())
    os.environ["KAGGLEHUB_CACHE"] = abs_path
    saved_path = kagglehub.dataset_download("olistbr/brazilian-ecommerce")

    saved_set = set([fn for fn in os.listdir(saved_path)])
    manifest_set = set(FILES.keys())
    if not saved_set == manifest_set:
        raise RuntimeError(
            f"Download is not successful. {saved_set}!={manifest_set}. Check manifest"
        )

    for file_name in os.listdir(saved_path):
        full_file_name = os.path.join(saved_path, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, raw_dir)

    to_del = Path(*Path(saved_path).relative_to(abs_path).parts[:1])
    shutil.rmtree(Path.joinpath(Path(abs_path), to_del))

    saved = {fn: str(raw_dir / fn) for fn in FILES.keys()}
    return saved


def download_all() -> dict[str, str]:
    cfg = load_cfg()
    raw_dir = Path(cfg["data"]["raw_dir"])
    ensure_dir(raw_dir)
    return download(cfg["data"]["kaggle_slug"], raw_dir)


if __name__ == "__main__":
    download_all()
