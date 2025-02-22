import os
import sys
import platform
import subprocess

print("🔧 Starting build...")

is_github = os.getenv("GITHUB_ACTIONS") == "true"

current_platform = platform.system().lower()

if current_platform == "windows":
    print("🖥️ Running on Windows - Using Pyinstaller")
    
    import PyInstaller.__main__
    
    options = [
        "src/main.py",
        "--icon=src/assets/images/icon_256x256.ico",
        f"--add-data=src/assets{os.pathsep}assets",
        "--name=wme",
        "--onefile",
    ]

    if "--debug" in sys.argv:
        options.append("--console")
    else:
        options.append("--windowed")

    print(f"🔹 Options build: {options}")
    
    PyInstaller.__main__.run(options)

elif current_platform == "linux" or current_platform == "darwin":
    print("📱 Running on Linux/Mac - Using Buildozer")

    debug = "--debug" in sys.argv
    build_command = ["buildozer", "-v", "android", "debug" if debug else "release"]

    try:
        subprocess.run(build_command, check=True)
        print("✅ Build successful!")
    except subprocess.CalledProcessError:
        print("❌ Error when build APK.")
        sys.exit(1)

else:
    print(f"⚠️ This device isn't supported: {current_platform}")
    sys.exit(1)