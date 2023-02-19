import PyInstaller.__main__

PyInstaller.__main__.run([
    'rumpify.py',
    '--onefile',
    '--windowed',
    '--clean'
])