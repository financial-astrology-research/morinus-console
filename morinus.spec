# -*- mode: python -*-
a = Analysis([os.path.join(HOMEPATH,'support\\_mountzlib.py'), os.path.join(HOMEPATH,'support\\useUnicode.py'), 'Morinus\\morinus.py'],
             pathex=['C:\\pyinstaller-1.5.1'])
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('build\\pyi.win32\\morinus', 'morinus.exe'),
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='Morinus.ico')
coll = COLLECT( exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name=os.path.join('dist', 'morinus'))
app = BUNDLE(coll,
             name=os.path.join('dist', 'morinus.app'))
