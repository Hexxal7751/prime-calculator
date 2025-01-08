import sys
from cx_Freeze import setup, Executable
import os

exe_metadata = {
    'copyright': 'Your Copyright Notice Here',
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Prime Calculator",
    version="2",
    description="Prime Calculator",
    executables=[Executable("Prime Calculator.py", base=base, icon="icon.ico")],  # Replace "icon.ico" with the path to your icon file
    options={
        "build_exe": {
            "includes": ["tkinter", "math", "time", "threading"],
            "include_files": ["icon.ico", "icon_PF.ico", "icon_DN.ico", "icon_CPC.ico", "icon_TPG.ico"],  # Add any additional files or directories here
        }
    }
)
