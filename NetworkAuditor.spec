# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path


root = Path(SPECPATH)
frontend_dist = root / "frontend" / "Network-Auditor" / "dist"
frontend_datas = [
    (
        str(file),
        str(
            Path("frontend")
            / "Network-Auditor"
            / "dist"
            / file.relative_to(frontend_dist).parent
        ),
    )
    for file in frontend_dist.rglob("*")
    if file.is_file()
]

a = Analysis(
    [str(root / "run_web.py")],
    pathex=[str(root / "backend")],
    binaries=[],
    datas=frontend_datas,
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
    name='NetworkAuditor',
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
