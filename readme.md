# SSH V1 Tool

A Python-based troubleshooting and diagnostic tool for Schneider Electric CCC controllers, featuring an interactive SSH client, WiFi/network analysis, hardware info retrieval, and a Tkinter-based SSH key selector UI.

---

## Features

- **SSH Key Selection UI:** Select your SSH private key file via a graphical interface.
- **SSH Connection:** Securely connect to remote controllers using Paramiko.
- **Main Menu:** Interactive console menu for diagnostics and data retrieval.
- **WiFi Analysis:** Get signal strength, network interface, frequency band, and driver info.
- **Hardware Info:** Retrieve bootloader, firmware, and hardware details.
- **Data Logging:** Save signal strength data to CSV and plot with Matplotlib.
- **Remembers Last Key:** Remembers the last used SSH key file for convenience.

---

## Requirements

- Python 3.8+
- See `requirements.txt` for all dependencies.

---

## Setup

1. **Clone the repository:**
    ```sh
    git clone <your-repo-url>
    cd ssh_v1_tool
    ```

2. **Create and activate a virtual environment (recommended):**
    ```sh
    python -m venv myenv
    myenv\Scripts\activate
    ```

3. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

---

## Usage

1. **Run the tool:**
    ```sh
    python main.py
    ```

2. **Select your SSH key file** in the UI and click **RUN**.

3. **Follow the console prompts** to interact with the main menu and perform diagnostics.

---

## Packaging as an Executable

To build a standalone executable with PyInstaller:

```sh
pyinstaller --onefile --add-data "last_ssh_key.txt;." main.py
```

The executable will be in the `dist` folder.

---

## Security Notes

- **Never commit your SSH private key to version control.**
- The tool remembers the last used SSH key path in `last_ssh_key.txt` (not the key content).
- `.env` and key files are ignored via `.gitignore`.

---

## Project Structure

```
ssh_v1_tool/
├── main.py
├── requirements.txt
├── .gitignore
├── last_ssh_key.txt
└── ...
```

---

## License

(c) 2023 Schneider Electric SE. All rights reserved.

---

## Developed by

Gonzalo Patino  
Schneider Electric Project
