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
        'src.core.flash_permissions',
        'src.core.cache_proxy',
        'src.models.account',
        'src.models.game_session',
        'src.models.relog_schedule',
        'src.services.account_service',
        'src.services.feedback_service',
        'src.services.oas_api_service',
        'src.controllers.hub_controller',
        'src.controllers.game_controller',
        'src.ui.views.hub_view',
        'src.ui.views.game_view',
        'src.ui.components.title_bar',
        'src.ui.components.dialogs',
        'src.ui.components.floating_macro',
        'src.ui.components.patch_notes_dialog',
        'src.ui.components.feedback_dialog',
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
    [],
    exclude_binaries=True,
    name='BKLauncherLO_v2.4.3',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['bacon_knight.ico'],
    version='version_info.txt',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='BKLauncherLO_v2.4.3',
)
