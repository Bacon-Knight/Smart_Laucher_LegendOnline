# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src\\main.py'],
    pathex=['.'],
    binaries=[],
    datas=[('style.qss', '.'), ('pepflashplayer.dll', '.'), ('Ferramentas', 'Ferramentas'), ('bacon_knight.ico', '.'), ('src/assets', 'src/assets')],
    hiddenimports=[
        'src.core.logger',
        'src.core.config',
        'src.core.webengine',
        'src.core.macros',
        'src.models.account',
        'src.models.game_session',
        'src.models.relog_schedule',
        'src.services.account_service',
        'src.controllers.hub_controller',
        'src.controllers.game_controller',
        'src.ui.views.hub_view',
        'src.ui.views.game_view',
        'src.ui.components.title_bar',
        'src.ui.components.dialogs',
        'src.ui.components.floating_macro',
        'src.ui.components.frameless'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='LegendOnlineLauncher_v2.2',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['bacon_knight.ico'],
)
