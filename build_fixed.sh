#!/usr/bin/env bash
set -euo pipefail

# -------------------------------------------------
# 1️⃣  PyInstaller – gerar o pacote para Linux
# -------------------------------------------------
echo "=== Gerando aplicação com PyInstaller para Linux ..."
pyinstaller --noconfirm LegendOnlineLauncher_v2.1_linux.spec

# O aplicativo empacotado ficará em:
#   dist/LegendOnlineLauncher_v2.1_linux
# -------------------------------------------------

# -------------------------------------------------
# 2️⃣  Montar pacote .deb (Ubuntu/Debian)
# -------------------------------------------------
echo "=== Montando estrutura .deb ..."
rm -rf deb_package
mkdir -p deb_package/DEBIAN \
         deb_package/opt/legend-launcher \
         deb_package/usr/local/bin \
         deb_package/usr/share/applications \
         deb_package/usr/share/icons/hicolor/256x256/apps

# ----------------- control file -----------------
cat > deb_package/DEBIAN/control <<'EOF'
Package: legend-online-launcher
Version: 2.1.0
Section: utils
Priority: optional
Architecture: amd64
Maintainer: Mariano <mariano@example.com>
Depends: python3 (>= 3.8), python3-pyqt5, python3-pyqt5.qtwebengine
Description: Legend Online Launcher com plugin Flash embutido (v32.0.0.371)
 Launcher otimizado para Legend Online com suporte a Flash PPAPI.
EOF

# ----------------- copiar pacote -----------------
cp dist/LegendOnlineLauncher_v2.1_linux deb_package/opt/legend-launcher/legend-launcher-bin
chmod 755 deb_package/opt/legend-launcher/legend-launcher-bin

# Copiar plugin flash para uma pasta do sistema onde o Sandbox do Chromium permite leitura
mkdir -p deb_package/usr/lib/pepperflashplugin-nonfree
if [ -f libpepflashplayer.so ]; then
    cp libpepflashplayer.so deb_package/usr/lib/pepperflashplugin-nonfree/
    chmod 644 deb_package/usr/lib/pepperflashplugin-nonfree/libpepflashplayer.so
fi

# Criar atalho no bin
ln -s /opt/legend-launcher/legend-launcher-bin deb_package/usr/local/bin/legend-launcher

# ----------------- ícone -----------------
if command -v convert &>/dev/null; then
    convert bacon_knight.ico -resize 256x256 \
        deb_package/usr/share/icons/hicolor/256x256/apps/legend-launcher.png
else
    cp bacon_knight.ico deb_package/usr/share/icons/hicolor/256x256/apps/legend-launcher.png
fi

# ----------------- desktop entry -----------------
cat > deb_package/usr/share/applications/legend-launcher.desktop <<'EOF'
[Desktop Entry]
Name=Legend Online Launcher
Comment=Launcher para Legend Online (requere Flash PPAPI)
Exec=/opt/legend-launcher/legend-launcher-bin
Icon=legend-launcher
Terminal=false
Type=Application
Categories=Game;
EOF

# ----------------- criar .deb -----------------
echo "=== Construindo .deb ..."
fakeroot dpkg-deb --build deb_package legend-online-launcher_2.1.0_amd64.deb
echo "✔ .deb pronto → legend-online-launcher_2.1.0_amd64.deb"

# -------------------------------------------------
# 3️⃣  AppImage 
# -------------------------------------------------
echo "=== Montando AppImage ..."
rm -rf AppDir
mkdir -p AppDir/usr/bin/legend-launcher-app \
         AppDir/usr/share/icons/hicolor/256x256/apps \
         AppDir/usr/share/applications

# Copia o binário executável do PyInstaller
cp dist/LegendOnlineLauncher_v2.1_linux AppDir/usr/bin/legend-launcher-app/legend-launcher-bin
chmod +x AppDir/usr/bin/legend-launcher-app/legend-launcher-bin

# Copia ícone
cp deb_package/usr/share/icons/hicolor/256x256/apps/legend-launcher.png \
    AppDir/usr/share/icons/hicolor/256x256/apps/
cp deb_package/usr/share/icons/hicolor/256x256/apps/legend-launcher.png AppDir/legend-launcher.png

# Desktop file
cp deb_package/usr/share/applications/legend-launcher.desktop \
   AppDir/usr/share/applications/
# Ajusta o Exec para rodar pelo AppRun no desktop file da raiz
cat > AppDir/legend-launcher.desktop <<'EOF'
[Desktop Entry]
Name=Legend Online Launcher
Comment=Launcher para Legend Online (requere Flash PPAPI)
Exec=legend-launcher-bin
Icon=legend-launcher
Terminal=false
Type=Application
Categories=Game;
EOF

# Create AppRun script (required by AppImage)
cat > AppDir/AppRun <<'EOF'
#!/bin/sh
HERE="$(dirname "$(readlink -f "${0}")")"
export PATH="${HERE}/usr/bin/legend-launcher-app:${PATH}"
exec "${HERE}/usr/bin/legend-launcher-app/legend-launcher-bin" "$@"
EOF
chmod +x AppDir/AppRun

# Garante que o appimagetool esteja no PATH
if ! command -v appimagetool &>/dev/null; then
    echo "Downloading appimagetool..."
    mkdir -p ~/.local/bin
    wget -O ~/.local/bin/appimagetool \
        https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
    chmod +x ~/.local/bin/appimagetool
    export PATH=$HOME/.local/bin:$PATH
fi

echo "=== Gerando AppImage ..."
appimagetool AppDir Legend-Online-Launcher-v2.1-x86_64.AppImage
echo "✔ AppImage pronto → Legend-Online-Launcher-v2.1-x86_64.AppImage"
