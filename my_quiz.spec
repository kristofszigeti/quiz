# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['my_quiz.py'],
    pathex=[],
    binaries=[],
    datas=[('./data/quiz_sport.json', 'data'), ('./data/quiz_movie.json', 'data'), ('./data/quiz_geography.json', 'data'), ('./data/quiz_football.json', 'data'), ('./data/quiz_darts.json', 'data'), ('./data/quiz_boardgames.json', 'data'), ('./logo/logo_sport.png', 'logo'), ('./logo/logo_movie.png', 'logo'), ('./logo/logo_geography.png', 'logo'), ('./logo/logo_football.png', 'logo'), ('./logo/logo_darts.png', 'logo'), ('./logo/logo_boardgames.png', 'logo')],
    hiddenimports=[],
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
    name='my_quiz',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
