# tntn

Python wrapper library for tunneling apps

The main purpose is for use in my other project [Bing-su/sd-webui-tunnels](https://github.com/Bing-su/sd-webui-tunnels).

---

## Usage

```sh
❯ tntn --help
tntn: Python wrapper library for tunneling apps

Usage: tntn <app_name> <args>
```

```sh
❯ tntn jprq --help
Usage: jprq <command> [arguments]

Commands:
  auth <token>               Set authentication token from jprq.io/auth
  tcp <port>                 Start a TCP tunnel on the specified port
  http <port>                Start an HTTP tunnel on the specified port
  http <port> -s <subdomain> Start an HTTP tunnel with a custom subdomain
  --help                     Show this help message
  --version                  Show the version number
```

see [jprq](https://github.com/azimjohn/jprq)

```sh
❯ tntn bore --help
A modern, simple TCP tunnel in Rust that exposes local ports to a remote server, bypassing standard NAT connection firewalls.

Usage: bore.exe <COMMAND>

Commands:
  local   Starts a local proxy to the remote server
  server  Runs the remote proxy server
  help    Print this message or the help of the given subcommand(s)

Options:
  -h, --help     Print help information
  -V, --version  Print version information
```

see [bore](https://github.com/ekzhang/bore)
