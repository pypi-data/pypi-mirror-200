from __future__ import annotations

import platform
import shutil
from dataclasses import dataclass
from pathlib import Path
from urllib.request import urlopen

from tqdm.auto import tqdm

try:
    import tomllib
except ImportError:
    import tomli as tomllib


urls_file = Path(__file__).parent / "urls.toml"
with urls_file.open("rb") as f:
    all_urls = tomllib.load(f)


@dataclass
class Info:
    app: str
    system: str
    machine: str

    def __post_init__(self):
        self.app = self.app.lower()
        self.system = self.system.lower()
        self.machine = self.machine.lower()

        if self.app not in ["bore", "jprq"]:
            raise ValueError(f"{self.app!r} is not supported.")

        download_url = all_urls[self.app]

        if self.system not in download_url:
            raise RuntimeError(f"{self.app}: {self.system!r} is not supported.")

        urls = download_url[self.system]
        if self.machine not in urls:
            raise RuntimeError(
                f"{self.app}: {self.machine!r} is not supported on {self.system}."
            )

        self.url: str = urls[self.machine]["url"]
        root = Path(__file__).parent

        if "name" in urls[self.machine]:
            self.executable = str(root / urls[self.machine]["name"])
        else:
            self.executable = str(root / self.app)


def get_info(app: str) -> Info:
    return Info(app, platform.system(), platform.machine())


def download(info: Info | str) -> str:
    """
    Downloads the binary from the github.

    Parameters
    ----------
        info: Info | str
            information about the system and machine architecture

    Returns
    -------
        str
            The path to the excutable file
    """
    if isinstance(info, str):
        info = get_info(info)

    dest = Path(__file__).parent / info.url.split("/")[-1]

    with urlopen(info.url) as resp:
        total = int(resp.headers.get("Content-Length", 0))
        with tqdm.wrapattr(
            resp, "read", total=total, desc=f"Download {info.app}..."
        ) as src, dest.open("wb") as dst:
            shutil.copyfileobj(src, dst)

    if info.url.endswith((".gz", ".zip")):
        shutil.unpack_archive(dest, dest.parent)
        dest.unlink()
    excutable = info.executable
    Path(excutable).chmod(0o777)

    return excutable


def remove_executable(info: Info | str) -> None:
    """
    Removes the executable
    """
    if isinstance(info, str):
        info = get_info(info)
    if Path(info.executable).exists():
        Path(info.executable).unlink()
