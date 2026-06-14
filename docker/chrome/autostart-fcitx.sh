#!/usr/bin/env bash
# kasmweb custom_startup.sh hook. Runs after Xvfb/desktop session is up.
set -e

export DISPLAY=${DISPLAY:-:1}
export GTK_IM_MODULE=fcitx
export QT_IM_MODULE=fcitx
export XMODIFIERS=@im=fcitx

fcitx -d --replace 2>/tmp/fcitx.log &

PROFILE_DIR=/home/kasm-user/chrome-profile
mkdir -p "$PROFILE_DIR"

# Remove stale singleton lock files left over by a previous container hostname.
rm -f "$PROFILE_DIR"/Singleton* 2>/dev/null || true

(
  sleep 3
  /opt/google/chrome/chrome \
      --user-data-dir="$PROFILE_DIR" \
      --no-sandbox \
      --no-first-run \
      --no-default-browser-check \
      --password-store=basic \
      --disable-features=TranslateUI \
      ${CHROME_CLI:-} \
      >/tmp/chrome.log 2>&1 &
) &

# Relay CDP from Chrome's local 9222 to container 9223 for host port mapping.
(
  sleep 6
  socat TCP-LISTEN:9223,fork,reuseaddr TCP:127.0.0.1:9222 \
      >/tmp/socat.log 2>&1 &
) &
