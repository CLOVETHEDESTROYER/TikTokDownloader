#!/usr/bin/env python3
import os
import sys
import subprocess


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def check_requirements():
    """Check if required packages are installed"""
    try:
        import yt_dlp
        return True
    except ImportError:
        print("⚠️ Required package 'yt-dlp' is not installed.")
        choice = input(
            "Do you want to install required packages now? (y/n): ").strip().lower()
        if choice == 'y':
            subprocess.run([sys.executable, "-m", "pip",
                           "install", "-r", "requirements.txt"])
            return True
        else:
            return False


def main_menu():
    """Display the main menu"""
    clear_screen()
    print("=" * 50)
    print("📥 TikTok Video Downloader - Launcher")
    print("=" * 50)
    print("\nChoose a version to run:")
    print("1. 🖥️  Single Video Downloader (Command Line)")
    print("2. 📋 Batch Video Downloader (Command Line)")
    print("3. 🎮 Tkinter GUI")
    print("4. 🌐 Flask Web UI")
    print("5. 📊 CSV Export Version")
    print("6. 📚 Install Requirements")
    print("0. ❌ Exit")

    choice = input("\nEnter your choice (0-6): ").strip()
    return choice


def run_script(script_name):
    """Run a Python script"""
    try:
        subprocess.run([sys.executable, script_name])
    except Exception as e:
        print(f"Error running {script_name}: {e}")
        input("Press Enter to continue...")


if __name__ == "__main__":
    # Ensure downloads directory exists
    os.makedirs("downloads", exist_ok=True)

    while True:
        choice = main_menu()

        if choice == '0':
            print("Goodbye! 👋")
            sys.exit(0)

        elif choice == '1':
            if check_requirements():
                run_script("tiktok_downloader.py")

        elif choice == '2':
            if check_requirements():
                run_script("batch_tiktok_downloader.py")

        elif choice == '3':
            if check_requirements():
                run_script("tkinter_gui.py")

        elif choice == '4':
            if check_requirements():
                try:
                    import flask
                    run_script("flask_web_ui.py")
                except ImportError:
                    print("⚠️ Flask is required for the web UI.")
                    choice = input(
                        "Do you want to install Flask now? (y/n): ").strip().lower()
                    if choice == 'y':
                        subprocess.run(
                            [sys.executable, "-m", "pip", "install", "flask"])
                        run_script("flask_web_ui.py")

        elif choice == '5':
            if check_requirements():
                run_script("tiktok_downloader_with_csv.py")

        elif choice == '6':
            subprocess.run([sys.executable, "-m", "pip",
                           "install", "-r", "requirements.txt"])
            print("✅ Requirements installed successfully!")
            input("Press Enter to continue...")

        else:
            print("⚠️ Invalid choice. Please try again.")
            input("Press Enter to continue...")
