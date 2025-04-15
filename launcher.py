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
    print("📱 Social Media Video Downloader - Launcher")
    print("=" * 50)
    print("\nChoose a platform:")
    print("1. 📱 TikTok")
    print("2. 📸 Instagram")
    print("3. 📚 Install Requirements")
    print("0. ❌ Exit")

    choice = input("\nEnter your choice (0-3): ").strip()
    return choice


def tiktok_menu():
    """Display TikTok menu"""
    clear_screen()
    print("=" * 50)
    print("📱 TikTok Video Downloader")
    print("=" * 50)
    print("\nChoose a version to run:")
    print("1. 🖥️  Single Video Downloader (Command Line)")
    print("2. 📋 Batch Video Downloader (Command Line)")
    print("3. 🎮 Tkinter GUI")
    print("4. 🌐 Flask Web UI")
    print("5. 📊 CSV Export Version")
    print("0. ↩️ Back to Main Menu")

    choice = input("\nEnter your choice (0-5): ").strip()
    return choice


def instagram_menu():
    """Display Instagram menu"""
    clear_screen()
    print("=" * 50)
    print("📸 Instagram Content Downloader")
    print("=" * 50)
    print("\nChoose a version to run:")
    print("1. 🖥️  Single Post/Reel Downloader (Command Line)")
    print("2. 📋 Batch Content Downloader (Command Line)")
    print("3. 🎮 Tkinter GUI")
    print("4. 📊 CSV Export Version")
    print("0. ↩️ Back to Main Menu")

    choice = input("\nEnter your choice (0-4): ").strip()
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
    os.makedirs("downloads/instagram", exist_ok=True)

    while True:
        choice = main_menu()

        if choice == '0':
            print("Goodbye! 👋")
            sys.exit(0)

        elif choice == '1':  # TikTok
            while True:
                tiktok_choice = tiktok_menu()

                if tiktok_choice == '0':
                    break  # Back to main menu

                elif tiktok_choice == '1':
                    if check_requirements():
                        run_script("tiktok_downloader.py")

                elif tiktok_choice == '2':
                    if check_requirements():
                        run_script("batch_tiktok_downloader.py")

                elif tiktok_choice == '3':
                    if check_requirements():
                        run_script("tkinter_gui.py")

                elif tiktok_choice == '4':
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

                elif tiktok_choice == '5':
                    if check_requirements():
                        run_script("tiktok_downloader_with_csv.py")

                else:
                    print("⚠️ Invalid choice. Please try again.")
                    input("Press Enter to continue...")

        elif choice == '2':  # Instagram
            while True:
                instagram_choice = instagram_menu()

                if instagram_choice == '0':
                    break  # Back to main menu

                elif instagram_choice == '1':
                    if check_requirements():
                        run_script("instagram_downloader.py")

                elif instagram_choice == '2':
                    if check_requirements():
                        run_script("batch_instagram_downloader.py")

                elif instagram_choice == '3':
                    if check_requirements():
                        run_script("instagram_gui.py")

                elif instagram_choice == '4':
                    if check_requirements():
                        run_script("instagram_downloader_with_csv.py")

                else:
                    print("⚠️ Invalid choice. Please try again.")
                    input("Press Enter to continue...")

        elif choice == '3':  # Install Requirements
            subprocess.run([sys.executable, "-m", "pip",
                           "install", "-r", "requirements.txt"])
            print("✅ Requirements installed successfully!")
            input("Press Enter to continue...")

        else:
            print("⚠️ Invalid choice. Please try again.")
            input("Press Enter to continue...")
