<div align="center">

# 多币种靓号钱包生成器

**一个高性能、支持多币种（ETH/TRON）的靓号钱包地址生成器。利用您计算机的全部CPU核心，极速寻找您心仪的定制化加密货币地址。**

[English](README.md)

</div>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.7+-blue.svg" alt="Python 版本">
  <img src="https://img.shields.io/badge/License-GPL-green.svg" alt="许可证">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey" alt="平台">
</p>

<p align="center">
  <a href="#-功能特性">功能特性</a> •
  <a href="#-支持的币种">支持的币种</a> •
  <a href="#-工作原理">工作原理</a> •
  <a href="#-快速开始">快速开始</a> •
  <a href="#-安全警告">安全警告</a> •
  <a href="#-赞助">赞助</a> •
  <a href="#-许可证">许可证</a>
</p>

---

### ✨ 功能特性

*   **多币种支持**: 可同时为一个助记词生成并匹配以太坊 (EVM 兼容 ) 和波场 (TRON) 的靓号地址。
*   **高性能**: 采用多进程架构，充分利用现代多核 CPU 的全部计算能力，生成速度远超单线程脚本。
*   **安全可靠**:
    *   完全离线运行，您的私钥和助记词永远不会接触网络。
    *   基于行业标准的 `BIP39` (助记词) 和 `BIP44` (分层路径) 协议生成钱包。
    *   代码简洁开源，逻辑清晰可查，无任何后门。
*   **高度可定制**: 只需修改脚本开头的配置，即可轻松设定您想要的靓号规则。
*   **跨平台**: 基于 Python 编写，可在 Windows, macOS, 和 Linux 系统上运行。

### ⛓️ 支持的币种

*   **以太坊 (Ethereum)**: 及其所有 EVM 兼容链，如 BSC, Polygon, Arbitrum 等。
*   **波场 (TRON)**

### ⚙️ 工作原理

靓号地址的生成本质上是一个“暴力破解”的穷举过程。程序会执行以下循环：

1.  **生成**: 创建一个随机的12词助记词。
2.  **派生**: 基于该助记词，根据 `BIP44` 标准派生路径分别计算出以太坊和波场的公钥和地址。
3.  **匹配**: 检查生成的地址是否同时满足您设定的前缀规则。
4.  **重复**: 如果不匹配，则重复以上过程，直到找到符合条件的地址为止。

本项目利用 `multiprocessing` 库将这个计算密集型任务分配给计算机的每一个 CPU 核心，每个核心独立进行寻找，大大缩短了找到目标地址的期望时间。

### 🚀 快速开始

**1. 准备环境**

确保您的电脑已经安装了 Python 3.7 或更高版本。

**2. 安装依赖库**

打开终端或命令行工具，运行以下命令来安装必需的库：

```bash
pip install mnemonic bip_utils
```

**3. 配置靓号规则**

打开 `multiprocess_generator.py` (多进程版本) 文件，找到并修改文件头部的配置部分：

```python
# --- 您需要在这里设置两种币的靓号规则 ---
# 规则越简单，找到的可能性才越大！建议2-3位。
ETH_PREFIX_TO_FIND = "888"  # 以太坊地址以 0x... 开头
TRON_PREFIX_TO_FIND = "TSS" # 波场地址以 T... 开头
# ------------------------------------

# --- 多进程配置 ---
# 设置要使用的CPU核心数。mp.cpu_count() 会获取您电脑的所有核心数。
NUM_PROCESSES = mp.cpu_count()
# ------------------
```

**4. 运行程序**

在终端中运行脚本：

```bash
python multiprocess_generator.py
```

程序将启动并利用所有 CPU 核心开始搜索。找到后，它会自动停止并在屏幕上显示您的**助记词、靓号地址和私钥**。

### ⚠️ 安全警告 ⚠️

*   **立即备份**: 找到靓号后，**请立即用纸笔抄下助记词并存放在绝对安全的地方**。这是恢复您资产的唯一方式。
*   **离线操作**: 为了绝对安全，强烈建议在**断开网络连接**的计算机上运行此脚本。
*   **风险自负**: 本项目为开源工具，作者不承担任何因使用不当造成的资产损失责任。请务必谨慎操作。

### ❤️ 赞助

如果您觉得这个项目对您有帮助，并希望支持后续的开发，欢迎向以下地址捐赠。感谢您的支持！

*   **ETH:** `0x888888cFcD5aD452F18330ea2686c9389d57A32e`

### 📜 许可证

本项目基于 GPL3 许可证。详情请参阅 [LICENSE](LICENSE) 文件。
