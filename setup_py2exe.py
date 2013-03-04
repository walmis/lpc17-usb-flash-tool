from distutils.core import setup
import py2exe

setup(
    # py2exe extras
    windows=[{'script': "Flash.py", 'icon_resources': [(1,'chip.ico')]}],
    zipfile=None,
    options={'py2exe': {'bundle_files': 1, 
    							'compressed': True,
    							'dll_excludes': ['w9xpopen.exe', '_ssl', 'doctest ', 'pdb', 'inspect', 'MSVCP90.dll']}},
)
