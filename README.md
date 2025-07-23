<div align="center">

# Multi-Coin Vanity Wallet Generator

**A high-performance, multi-coin (ETH/TRON) vanity wallet address generator. It leverages all CPU cores of your computer to rapidly search for your desired custom cryptocurrency addresses.**

[简体中文](README.zh-CN.md)

</div>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.7+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey" alt="Platform">
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-supported-coins">Supported Coins</a> •
  <a href="#-how-it-works">How It Works</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-security-warning">Security Warning</a> •
  <a href="#-donation">Donation</a> •
  <a href="#-license">License</a>
</p>

---

### ✨ Features

*   **Multi-Coin Support**: Simultaneously generate and match vanity addresses for Ethereum (EVM-compatible ) and TRON from a single mnemonic phrase.
*   **High Performance**: Utilizes a multiprocessing architecture to leverage the full power of modern multi-core CPUs, significantly outperforming single-threaded scripts.
*   **Secure & Reliable**:
    *   Runs completely offline. Your private keys and mnemonics never touch the internet.
    *   Generates wallets based on industry standards `BIP39` (Mnemonic) and `BIP44` (Hierarchical Path).
    *   The code is concise, open-source, and auditable, with no backdoors.
*   **Highly Customizable**: Easily define your desired vanity patterns by modifying the configuration at the top of the script.
*   **Cross-Platform**: Written in Python, it runs on Windows, macOS, and Linux.

### ⛓️ Supported Coins

*   **Ethereum**: And all EVM-compatible chains like BSC, Polygon, Arbitrum, etc.
*   **TRON**

### ⚙️ How It Works

Generating a vanity address is essentially a brute-force process. The program executes the following loop:

1.  **Generate**: Create a random 12-word mnemonic phrase.
2.  **Derive**: Based on this mnemonic, derive the public keys and addresses for Ethereum and TRON according to the `BIP44` standard paths.
3.  **Match**: Check if the generated addresses simultaneously meet the prefix rules you've set.
4.  **Repeat**: If there's no match, repeat the process until a qualifying address is found.

This project uses the `multiprocessing` library to distribute this computationally intensive task across all CPU cores of your computer. Each core searches independently, drastically reducing the expected time to find your target address.

### 🚀 Quick Start

**1. Prepare Your Environment**

Ensure you have Python 3.7 or newer installed on your system.

**2. Install Dependencies**

Open your terminal or command prompt and run the following command to install the required libraries:

```bash
pip install mnemonic bip_utils
```

**3. Configure Your Vanity Rules**

Open the `multiprocess_generator.py` (the multi-process version) file and modify the configuration section at the top:

```python
# --- Configure your vanity rules for both coins here ---
# Simpler rules are much more likely to be found! 2-3 characters are recommended.
ETH_PREFIX_TO_FIND = "888"  # Ethereum address starts with 0x...
TRON_PREFIX_TO_FIND = "TSS" # TRON address starts with T...
# ------------------------------------

# --- Multi-process Configuration ---
# Set the number of CPU cores to use. mp.cpu_count() gets all cores.
NUM_PROCESSES = mp.cpu_count()
# ------------------
```

**4. Run the Generator**

Run the script from your terminal:

```bash
python multiprocess_generator.py
```

The program will start and begin searching using all your CPU cores. Once a match is found, it will automatically stop and display the **Mnemonic Phrase, Vanity Addresses, and Private Keys** on the screen.

### ⚠️ SECURITY WARNING ⚠️

*   **BACK UP IMMEDIATELY**: Once a vanity wallet is found, **immediately write down the mnemonic phrase on paper and store it in a physically secure location**. This is the only way to recover your assets.
*   **OPERATE OFFLINE**: For maximum security, it is strongly recommended to run this script on a computer that is **disconnected from the internet**.
*   **USE AT YOUR OWN RISK**: This is an open-source tool. The author is not responsible for any loss of assets resulting from improper use. Please proceed with caution.

### ❤️ Donation

If you find this project helpful and would like to support its development, you can send a donation to the following addresses. Thank you for your support!

*   **ETH/BSC/Polygon (EVM):** `0x...`
*   **TRON (TRC20):** `T...`
*   **BTC:** `bc1...`

### 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
