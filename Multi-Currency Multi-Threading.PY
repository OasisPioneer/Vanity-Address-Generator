# 导入我们需要的库
import time
import multiprocessing as mp
from mnemonic import Mnemonic
from bip_utils import (
    Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
)

# --- 您需要在这里设置两种币的靓号规则 ---
# 规则越简单，找到的可能性才越大！建议2-3位。
ETH_PREFIX_TO_FIND = "888888"  # 以太坊地址以 0x... 开头
TRON_PREFIX_TO_FIND = "Styx8888" # 波场地址以 T... 开头
# ------------------------------------

# --- 多进程配置 ---
# 设置要使用的CPU核心数。mp.cpu_count() 会获取您电脑的所有核心数。
# 如果您想保留一些CPU给其他任务，可以写成 mp.cpu_count() - 1
NUM_PROCESSES = mp.cpu_count()
# ------------------

def worker(result_queue, stop_event, process_id, eth_prefix, tron_prefix):
    """
    每个“工人”进程执行的函数
    """
    # 每个进程都拥有自己的助记词生成器
    mnemo = Mnemonic("english")
    count = 0
    start_time = time.time()

    print(f"进程 #{process_id} 已启动，开始计算...")

    while not stop_event.is_set():
        # 1. 生成助记词和种子
        words = mnemo.generate(strength=128)
        seed_bytes = Bip39SeedGenerator(words).Generate()

        # 2. 派生以太坊钱包并检查
        bip44_eth_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.ETHEREUM)
        bip44_eth_acc = bip44_eth_mst.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
        eth_address = bip44_eth_acc.PublicKey().ToAddress()

        # 3. 派生波场钱包并检查
        bip44_tron_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.TRON)
        bip44_tron_acc = bip44_tron_mst.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
        tron_address = bip44_tron_acc.PublicKey().ToAddress()

        # 4. 核心检查
        if eth_address.lower().startswith(eth_prefix) and tron_address.startswith(tron_prefix):
            # 找到了！设置停止事件并把结果放入队列
            stop_event.set()
            
            eth_private_key = bip44_eth_acc.PrivateKey().Raw().ToHex()
            tron_private_key = bip44_tron_acc.PrivateKey().Raw().ToHex()
            
            result_queue.put({
                "words": words,
                "eth_address": eth_address,
                "eth_pk": f"0x{eth_private_key}",
                "tron_address": tron_address,
                "tron_pk": tron_private_key,
                "found_by": process_id
            })
            break # 找到后工人退出循环

        count += 1
        # 每个工人可以独立报告自己的进度，但为了界面干净，可以注释掉
        # if count % 10000 == 0:
        #     elapsed = time.time() - start_time
        #     hps = count / elapsed if elapsed > 0 else 0
        #     print(f"\r进程 #{process_id} 已尝试 {count} 次, 速度: {hps:.0f} H/s", end="")


if __name__ == '__main__':
    # 准备好要匹配的完整前缀
    eth_vanity_prefix = "0x" + ETH_PREFIX_TO_FIND.lower()
    tron_vanity_prefix = TRON_PREFIX_TO_FIND

    print("="*60)
    print("多进程靓号地址生成器已启动！")
    print(f"目标CPU核心数: {NUM_PROCESSES}")
    print(f"ETH 规则: 地址以 '{eth_vanity_prefix}' 开头")
    print(f"TRON 规则: 地址以 '{tron_vanity_prefix}' 开头")
    print("找到后会自动停止。这会非常非常慢，请有极大的耐心...")
    print("="*60)

    # 创建用于通信的队列和事件
    result_queue = mp.Queue()
    stop_event = mp.Event()
    
    # 创建并启动所有工人进程
    processes = []
    for i in range(NUM_PROCESSES):
        p = mp.Process(target=worker, args=(result_queue, stop_event, i + 1, eth_vanity_prefix, tron_vanity_prefix))
        processes.append(p)
        p.start()

    # 主进程等待结果
    start_time = time.time()
    try:
        result = result_queue.get() # 这会阻塞，直到队列中有东西
        
        # 找到了！
        end_time = time.time()
        
        print("\n\n🎉🎉🎉 超级幸运星！找到了同时满足两个币种的靓号助记词！🎉🎉🎉")
        print(f"(由进程 #{result['found_by']} 找到)")
        print("-" * 60)
        print(f"🔑 助记词 (Mnemonic): {result['words']}")
        print("-" * 60)
        print(f"💼 以太坊 (EVM) 靓号地址: {result['eth_address']}")
        print(f"🔐 以太坊 (EVM) 私钥: {result['eth_pk']}")
        print("-" * 60)
        print(f"💼 波场 (TRON) 靓号地址: {result['tron_address']}")
        print(f"🔐 波场 (TRON) 私钥: {result['tron_pk']}")
        print("-" * 60)
        print(f"总耗时 {end_time - start_time:.2f} 秒。")

    except KeyboardInterrupt:
        print("\n用户手动中断程序。")
    finally:
        # 确保所有进程都被终止
        print("正在停止所有工人进程...")
        stop_event.set() # 通知所有进程停止
        for p in processes:
            p.join(timeout=1) # 等待进程结束
            if p.is_alive():
                p.terminate() # 如果还没结束，强制终止
        print("所有进程已停止。")