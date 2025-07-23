from eth_account import Account
from mnemonic import Mnemonic
import time

# --- 您需要在这里设置靓号规则 ---
# 比如，您想要以 "8888" 开头的地址
# 请将下面的 "8888" 替换为您想要的字符
PREFIX_TO_FIND = "8888888888"
# ------------------------------------

# 初始化助记词生成器，使用标准的英语词库
mnemo = Mnemonic("english")

# 准备好要匹配的完整前缀
vanity_prefix = "0x" + PREFIX_TO_FIND.lower()

print(f"正在努力寻找以 '{vanity_prefix}' 开头的靓号地址...")
print("找到后会自动停止并显示结果。这可能需要很长时间，请耐心等待...")

# 启用 eth_account 的HD钱包功能
Account.enable_unaudited_hdwallet_features()

# 初始化计数器和计时器
count = 0
start_time = time.time()

# 开始无限循环，直到找到为止
while True:
    # 1. 生成一个全新的、随机的、高度兼容的12词助记词
    #    strength=128 对应12个单词
    words = mnemo.generate(strength=128)
    
    # 2. 从助记词派生出第一个账户
    #    这是 eth_account 库最标准、最可靠的用法
    #    路径默认为 m/44'/60'/0'/0/0
    try:
        account = Account.from_mnemonic(words)
    except Exception:
        # 极少数情况下，生成的助记词可能存在问题，直接跳过
        continue
    
    # 3. 获取地址和私钥
    address = account.address
    private_key = account.key.hex()

    # 4. 判断地址是否是我们想要的靓号
    if address.lower().startswith(vanity_prefix):
        # 如果找到了！
        end_time = time.time()
        print("\n\n🎉 恭喜！成功找到靓号地址！🎉")
        print("-" * 50)
        # 输出最重要的助记词，请立即抄写并安全保管！
        print(f"🔑 助记词 (Mnemonic): {words}")
        print(f"💼 靓号地址 (Address): {address}")
        print(f"🔐 私钥 (Private Key): {private_key}")
        print("-" * 50)
        print(f"总共尝试了 {count+1} 次, 耗时 {end_time - start_time:.2f} 秒。")
        
        # 停止循环
        break
        
    # 只是为了让您看到程序在努力工作，每尝试1000次打印一次状态
    count += 1
    if count % 1000 == 0:
        elapsed_time = time.time() - start_time
        # 避免除以零的错误
        hashes_per_second = count / elapsed_time if elapsed_time > 0 else 0
        print(f"\r已尝试 {count} 次... 当前速度: {hashes_per_second:.0f} 次/秒", end="")