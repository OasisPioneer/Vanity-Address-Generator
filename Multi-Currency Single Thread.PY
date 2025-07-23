# 导入我们需要的、正确的库
from mnemonic import Mnemonic
from bip_utils import (
    Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
)
import time

# --- 您需要在这里设置两种币的靓号规则 ---
# 规则越简单，找到的可能性才越大！建议2-3位。
ETH_PREFIX_TO_FIND = "777"  # 以太坊地址以 0x... 开头
TRON_PREFIX_TO_FIND = "TSS" # 波场地址以 T... 开头
# ------------------------------------

# 初始化助记词生成器
mnemo = Mnemonic("english")

# 准备好要匹配的完整前缀
eth_vanity_prefix = "0x" + ETH_PREFIX_TO_FIND.lower()
# 波场地址区分大小写，所以我们直接用设定的前缀
tron_vanity_prefix = TRON_PREFIX_TO_FIND

print("正在努力寻找能同时满足 ETH 和 TRON 的靓号助记词...")
print(f"ETH 规则: 地址以 '{eth_vanity_prefix}' 开头")
print(f"TRON 规则: 地址以 '{tron_vanity_prefix}' 开头")
print("找到后会自动停止。这会非常非常慢，请有极大的耐心...")

# 初始化计数器和计时器
count = 0
start_time = time.time()

# 开始无限循环
while True:
    # 1. 生成一个高度兼容的12词助记词
    words = mnemo.generate(strength=128)
    
    # 2. 从助记词生成种子 (这是所有派生的基础)
    seed_bytes = Bip39SeedGenerator(words).Generate()

    # 3. 派生以太坊钱包 (路径: m/44'/60'/0'/0/0)
    bip44_eth_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.ETHEREUM)
    bip44_eth_acc = bip44_eth_mst.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
    eth_address = bip44_eth_acc.PublicKey().ToAddress()
    
    # 4. 派生波场钱包 (路径: m/44'/195'/0'/0/0)
    bip44_tron_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.TRON)
    bip44_tron_acc = bip44_tron_mst.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
    tron_address = bip44_tron_acc.PublicKey().ToAddress()

    # 5. 【核心】同时检查两个地址是否都满足条件
    if eth_address.lower().startswith(eth_vanity_prefix) and tron_address.startswith(tron_vanity_prefix):
        # 如果两个都找到了！
        end_time = time.time()
        
        # 获取私钥
        eth_private_key = bip44_eth_acc.PrivateKey().Raw().ToHex()
        tron_private_key = bip44_tron_acc.PrivateKey().Raw().ToHex()

        print("\n\n🎉🎉🎉 超级幸运星！找到了同时满足两个币种的靓号助记词！🎉🎉🎉")
        print("-" * 60)
        print(f"🔑 助记词 (Mnemonic): {words}")
        print("-" * 60)
        print(f"💼 以太坊 (EVM) 靓号地址: {eth_address}")
        print(f"🔐 以太坊 (EVM) 私钥: 0x{eth_private_key}")
        print("-" * 60)
        print(f"💼 波场 (TRON) 靓号地址: {tron_address}")
        print(f"🔐 波场 (TRON) 私钥: {tron_private_key}") # 波场私钥通常不带0x
        print("-" * 60)
        print(f"总共尝试了 {count+1} 次, 耗时 {end_time - start_time:.2f} 秒。")
        
        # 停止循环
        break
        
    # 打印状态
    count += 1
    if count % 1000 == 0:
        elapsed_time = time.time() - start_time
        hashes_per_second = count / elapsed_time if elapsed_time > 0 else 0
        print(f"\r已尝试 {count} 次... 当前速度: {hashes_per_second:.0f} 次/秒", end="")
