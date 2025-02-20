import PyInstaller.__main__
import os

# Create the exe in 'dist' folder
PyInstaller.__main__.run([
    'partition_manager.py',
    '--name=Windows Partition Manager',
    '--onefile',
    '--noconsole',
    '--uac-admin',  # Request admin privileges
    '--add-data=README.md;.',
    '--clean',
]) 