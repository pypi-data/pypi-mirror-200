from __future__ import annotations

import atexit
import re
import shlex
import subprocess
from pathlib import Path
from typing import NamedTuple

from .util import download, get_info

pattern = {
    "jprq": r"(?P<url>https?://\S+\.jprq\.live)",
    "bore": r"(?P<url>bore\.pub:\d+)",
}

argv = {"jprq": "http {port}", "bore": "local {port} --to bore.pub"}
lines = {"jprq": 5, "bore": 2}


class Urls(NamedTuple):
    tunnel: str
    process: subprocess.Popen


class Tunnel:
    def __init__(self, app: str = "bore"):
        self.app = app.lower()
        self.running: dict[int, Urls] = {}

    def __call__(
        self, port: int, token: str | None = None, verbose: bool = True
    ) -> Urls:
        if port in self.running:
            if verbose:
                self._print(self.running[port].tunnel)
            return self.running[port]

        info = get_info(self.app)
        if not Path(info.executable).exists():
            download(info)

        # if jprq, token is required
        if self.app == "jprq":
            if not token:
                raise ValueError("jprq requires token")

            # always success even if given invalid token, so no need to 'check=True'
            subprocess.run([info.executable, "auth", token])

        args = shlex.split(argv[self.app].format(port=port))
        args = [info.executable, *args]

        process = subprocess.Popen(
            args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8"
        )

        atexit.register(process.terminate)

        for _ in range(lines[self.app]):
            line = process.stdout.readline()

            # jprq: invalid token
            if "authentication failed" in line:
                raise RuntimeError("jprq: invalid token")

            # jprq: port is not running any service
            if "error: cannot reach server on port" in line:
                raise RuntimeError(f"jprq: port {port!r} is not running any service")

            match = re.search(pattern[self.app], line)
            if match:
                url = match.group("url")
                if self.app == "bore":
                    url = "http://" + url
                break
        else:
            raise RuntimeError(f"failed to start {self.app!r} on port {port!r}")

        urls = Urls(url, process)
        if verbose:
            self._print(url)
        self.running[port] = urls
        return urls

    @staticmethod
    def _print(url: str) -> None:
        print(f" * Running on {url}")

    def terminate(self, port: int) -> None:
        """
        terminates the tunnel on the given port

        Parameters
        ----------
        port : int
            port to terminate the tunnel on.

        Raises
        ------
        ValueError
            When the port is not running
        """
        if port in self.running:
            self.running[port].process.terminate()
            atexit.unregister(self.running[port].process.terminate)
            del self.running[port]
        else:
            raise ValueError(f"port {port!r} is not running.")


jprq = Tunnel("jprq")
bore = Tunnel("bore")
