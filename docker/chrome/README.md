# Public-safe Chrome image

This build context creates the public-safe osslab-agent Chrome image.

It intentionally does not include:

- browser profiles
- cookies or login state
- Bitwarden vault data
- `profile-seed.tar.zst`
- local `docker-compose.yml` files

## Pre-built image status

**No pre-built image has been uploaded to a registry yet.**

There is no published `docker pull` target (GHCR, Docker Hub, or otherwise).
Build from this directory locally.

## Build

```bash
cd docker/chrome
docker build -t osslab-agent-chrome:latest .
```

Use per-container volumes for persistent browser state.
