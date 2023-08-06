import subprocess
import sys
from pathlib import Path

from .util import download, get_info


def _help():
    "print help message"
    print("tntn: Python wrapper library for tunneling apps")
    print()
    print("Usage: tntn <app_name> <args>")
    print()


def main():
    "main cli entrypoint"
    if len(sys.argv) <= 1 or sys.argv[1] in ["-h", "--help"]:
        _help()
        sys.exit(0)

    app = sys.argv[1].lower()
    if app not in ["bore", "jprq"]:
        print(f"tntn: {app!r} is not supported")
        sys.exit(1)

    info = get_info(app)
    if not Path(info.executable).exists():
        download(info)

    args = sys.argv[2:]
    try:
        subprocess.run([info.executable, *args])
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
