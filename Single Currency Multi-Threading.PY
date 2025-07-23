import threading
import time
import os
from eth_account import Account
from mnemonic import Mnemonic
# 比如，您想要以 "8888" 开头的地址
# 请将下面的 "8888" 替换为您想要的字符
PREFIX_TO_FIND = "888888"
# ------------------------------------

# 全局变量和锁
found_event = threading.Event()  # 用于通知所有线程找到结果
result_lock = threading.Lock()   # 用于保护结果和计数器

found_mnemonic = None
found_address = None
found_private_key = None

total_attempts = 0
start_time = time.time()

# 启用 eth_account 的HD钱包功能
Account.enable_unaudited_hdwallet_features()

def generate_vanity_address(vanity_prefix):
    global total_attempts, found_mnemonic, found_address, found_private_key
    mnemo = Mnemonic("english")

    while not found_event.is_set():
        words = mnemo.generate(strength=128)
        try:
            account = Account.from_mnemonic(words)
        except Exception:
            continue

        address = account.address
        private_key = account.key.hex()

        with result_lock:
            total_attempts += 1
            if address.lower().startswith(vanity_prefix):
                found_mnemonic = words
                found_address = address
                found_private_key = private_key
                found_event.set()  # 设置事件，通知其他线程停止
                break

def main():
    global total_attempts, start_time

    vanity_prefix = "0x" + PREFIX_TO_FIND.lower()
    print(f"正在努力寻找以 '{vanity_prefix}' 开头的靓号地址...")
    print("找到后会自动停止并显示结果。这可能需要很长时间，请耐心等待...")

    num_threads = max(1, os.cpu_count() - 1) # 使用CPU核心数-1作为线程数，至少1个
    print(f"将启动 {num_threads} 个线程进行搜索...")

    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=generate_vanity_address, args=(vanity_prefix,))
        threads.append(thread)
        thread.start()

    # 实时显示进度
    while not found_event.is_set():
        with result_lock:
            current_attempts = total_attempts
        elapsed_time = time.time() - start_time
        hashes_per_second = current_attempts / elapsed_time if elapsed_time > 0 else 0
        print(f"\r已尝试 {current_attempts} 次... 当前速度: {hashes_per_second:.0f} 次/秒", end="", flush=True)
        time.sleep(1) # 每秒更新一次

    # 等待所有线程结束
    for thread in threads:
        thread.join()

    end_time = time.time()
    print("\n\n🎉 恭喜！成功找到靓号地址！🎉")
    print("-" * 50)
    print(f"🔑 助记词 (Mnemonic): {found_mnemonic}")
    print(f"💼 靓号地址 (Address): {found_address}")
    print(f"🔐 私钥 (Private Key): {found_private_key}")
    print("-" * 50)
    print(f"总共尝试了 {total_attempts} 次, 耗时 {end_time - start_time:.2f} 秒。")

if __name__ == "__main__":
    main()

import os