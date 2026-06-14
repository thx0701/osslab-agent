# Public-safe Chrome image

This build context creates the public-safe osslab-agent Chrome image.

It intentionally does not include:

- browser profiles
- cookies or login state
- Bitwarden vault data
- `profile-seed.tar.zst`
- local `docker-compose.yml` files

## Build

```bash
cd docker/chrome
docker build -t ghcr.io/thx0701/osslab-agent-chrome:latest .
```

## Push to GHCR

```bash
gh auth refresh -h github.com -s write:packages
gh auth token | docker login ghcr.io -u thx0701 --password-stdin

docker tag ghcr.io/thx0701/osslab-agent-chrome:latest ghcr.io/thx0701/osslab-agent-chrome:2026-06-14
docker push ghcr.io/thx0701/osslab-agent-chrome:2026-06-14
docker push ghcr.io/thx0701/osslab-agent-chrome:latest
```

Use per-container volumes for persistent browser state.
