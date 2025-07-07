# AES-256 File Encryptor/Decryptor (Python)

This is a Python-based file encryption and decryption tool using AES-256 encryption (via the `cryptography` library) with a simple GUI built in `tkinter`.

## 🔐 Features
- AES-256 encryption with PBKDF2 password-based key derivation
- Secure random salt and IV
- Simple graphical interface to encrypt and decrypt files
- Save output files with `.enc` and `.dec` extensions

## 🧱 Requirements

Install dependencies with:

```bash
pip install cryptography
```

## ▶️ How to Run

```bash
python aes_file_encryptor_gui.py
```

## 🏗️ How It Works

- **Encrypts**: `input_file → input_file.enc`
- **Decrypts**: `input_file.enc → input_file.dec`
- Password must match during decryption.
- Uses CFB mode for secure streaming encryption.

## 📦 Convert to EXE (Optional)

You can convert this script into a Windows executable using `pyinstaller`:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed aes_file_encryptor_gui.py
```

## ⚠️ Disclaimer

This tool is for educational purposes only. Use responsibly!
