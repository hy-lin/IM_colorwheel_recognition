# -*- mode: python -*-

block_cipher = None


a = Analysis(['src\\Experiments\\Experiment3\\recallNrecognition.py'],
             pathex=['D:\\Hsuan-Yu Lin\\Documents\\GitHub\\IM_colorwheel_recognition'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='recallNrecognition',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True , icon='src\\Experiments\\Experiment3\\resources\\uzh.ico')
