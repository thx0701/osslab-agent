# Public-safe Chrome image with Traditional Chinese IME, CDP relay, and Bitwarden.
# No browser profile, cookies, login state, vault data, or profile seed is baked in.
FROM kasmweb/chrome:1.16.0

USER root

# Locale + Chinese fonts + IME.
# fcitx-ui-classic provides the candidate window UI.
# xdotool is useful for UI automation tests; socat relays Chrome CDP.
RUN apt-get update && apt-get install -y --no-install-recommends \
        locales \
        fonts-noto-cjk \
        fonts-noto-cjk-extra \
        fcitx \
        fcitx-chewing \
        fcitx-ui-classic \
        fcitx-config-gtk \
        fcitx-frontend-gtk3 \
        fcitx-frontend-gtk2 \
        fcitx-frontend-qt5 \
        im-config \
        xdotool \
        socat \
    && locale-gen zh_TW.UTF-8 \
    && update-locale LANG=zh_TW.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

COPY autostart-fcitx.sh /dockerstartup/custom_startup.sh
RUN chmod +x /dockerstartup/custom_startup.sh && \
    chown 1000:0 /dockerstartup/custom_startup.sh

# Chrome managed policy: install Bitwarden from the Chrome Web Store.
COPY bitwarden-policy.json /etc/opt/chrome/policies/managed/bitwarden.json

ENV LANG=zh_TW.UTF-8 \
    LC_ALL=zh_TW.UTF-8 \
    LANGUAGE=zh_TW:zh \
    GTK_IM_MODULE=fcitx \
    QT_IM_MODULE=fcitx \
    XMODIFIERS=@im=fcitx \
    CHROME_CLI="--lang=zh-TW --remote-debugging-port=9222 --remote-debugging-address=127.0.0.1 --remote-allow-origins=*"

USER 1000
