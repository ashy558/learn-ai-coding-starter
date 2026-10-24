---
description: Start the SlopLang playground server, reusing an already-running one
---

Start the SlopLang playground server for this project.

Requested port: $ARGUMENTS — if this is blank, use the default port 8080. If it is not a whole number between 1 and 65535, stop and say so instead of starting anything.

Ports currently listening on this machine (from `lsof -nP -iTCP -sTCP:LISTEN`):

!`lsof -nP -iTCP -sTCP:LISTEN`

Before starting anything, check for an existing SlopLang playground server:

1. Run `pgrep -af 'playground/server\.py'` and confirm any match with `ps -p <pid> -o args=`. A listener running `python3 .../playground/server.py` is a SlopLang playground server.
2. If one is already running, do not start a second one. Check that `http://127.0.0.1:<its-port>/` responds (for example with `curl -fsS -o /dev/null -w '%{http_code}' http://127.0.0.1:<its-port>/`), then report the URL and stop.
3. If the requested port is held by some other process, do not kill it and do not silently pick a different port. Report which process owns the port and ask how to proceed.

When no playground server is running and the port is free, start it in the background so it keeps serving:

```bash
uv run playground/server.py <port>
```

Then confirm it answers at `http://127.0.0.1:<port>/` and report that URL. Leave the server running after you reply; do not stop it.
