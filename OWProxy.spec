# -*- mode: python ; coding: utf-8 -*-
from distutils.dir_util import copy_tree
import os
import json

#copy outfits folder to dist
fromDirectory = "outfits"
toDirectory = os.path.join(DISTPATH, fromDirectory)
copy_tree(fromDirectory, toDirectory)

#get hidden imports list
with open('plugins.json') as f:
    data = json.load(f)
hiddenimports = [f"{plugin_type}.{plugin_name}"
                     for plugin_type, plugin_names in data.items() 
                                     for plugin_name in plugin_names]
block_cipher = None


a = Analysis(['app.py'],
             pathex=['.'],
             binaries=[],
             datas=[('gui/thumbnail.png', 'gui/'), ('plugins.json', '.'), ('gui/color.png', 'gui/')],
             hiddenimports=['plugins.outfit', 'plugins.shield', 'core_plugins.session_userid'],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='OWProxy',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , uac_admin=True, icon='gui\\icon.ico')

