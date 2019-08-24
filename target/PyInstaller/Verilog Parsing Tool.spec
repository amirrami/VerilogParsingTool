# -*- mode: python -*-

block_cipher = None


a = Analysis(['D:\\VerilogParsingTool-master\\VerilogParsingTool\\src\\main\\python\\main.py'],
             pathex=['D:\\VerilogParsingTool-master\\VerilogParsingTool\\target\\PyInstaller'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=['d:\\verilogparsingtool-master\\verilogparsingtool\\fbsenv\\lib\\site-packages\\fbs\\freeze\\hooks'],
             runtime_hooks=['C:\\Users\\miro\\AppData\\Local\\Temp\\tmpqns5z9y0\\fbs_pyinstaller_hook.py'],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Verilog Parsing Tool',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=False , icon='D:\\VerilogParsingTool-master\\VerilogParsingTool\\src\\main\\icons\\Icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='Verilog Parsing Tool')
