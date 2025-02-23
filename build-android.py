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
    
    android_main = "src/main-android.py"
    if os.path.exists(android_main):
        print("✅ Found main-android.py, copying to main.py")
        os.rename(android_main, "src/main-android.py")
    else:
        print("❌ ERROR: main-android.py not found!")
        sys.exit(1)
        
    icon_path = "src/assets/images/icon_256x256.ico"
    if os.path.exists("buildozer.spec"):
        with open("buildozer.spec", "r") as f:
            spec_lines = f.readlines()

        with open("buildozer.spec", "w") as f:
            for line in spec_lines:
                if line.startswith("android.icon ="):
                    f.write(f"android.icon = {icon_path}\n")
                else:
                    f.write(line)
    else:
        print("⚠️ WARNING: buildozer.spec not found, running `buildozer init`...")
        subprocess.run(["buildozer", "init"], check=True)

    build_command = ["buildozer", "-v", "android", "debug" if debug else "release"]

    try:
        subprocess.run(build_command, check=True)
        print("✅ Build successful!")
    except subprocess.CalledProcessError:
        print("❌ Error when build APK.")
        sys.exit(1)
