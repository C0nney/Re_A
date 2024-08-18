import os
import zlib
import hashlib
from concurrent.futures import ThreadPoolExecutor

def repairChecksum(dex_file):
    with open(dex_file, "r+b") as f:
        # 跳过文件头的8个字节读取现有校验和
        f.seek(8)
        source_checksum = f.read(4)

        # 读取用于计算校验和的DEX数据部分
        f.seek(12)
        checkdata = f.read()

        # 计算新的校验和
        checksum = zlib.adler32(checkdata)
        new_checksum = checksum & 0xFFFFFFFF
        new_checksum_bytes = new_checksum.to_bytes(4, byteorder='little')

        # 判断校验和是否有问题
        if source_checksum == new_checksum_bytes:
            print(f"{dex_file} - 校验和正确，跳过修复")
            return False
        else:
            print(f"{dex_file} - 校验和错误，修复中...")
            print(f"{dex_file} - 头部原checksum: {source_checksum.hex()}")
            print(f"{dex_file} - 计算checksum: {format(new_checksum, '08x')}")

            # 将新校验和写回文件头
            f.seek(8)
            f.write(new_checksum_bytes)
            return True

def repairSignature(dex_file):
    with open(dex_file, "r+b") as f:
        # 跳过文件头的12个字节读取现有签名
        f.seek(12)
        source_signature = f.read(20)

        # 读取用于计算签名的DEX数据部分
        f.seek(32)
        sigdata = f.read()

        # 计算新的签名
        sha1 = hashlib.sha1()
        sha1.update(sigdata)
        new_signature = sha1.digest()

        print(f"{dex_file} - 现在signature: {source_signature.hex()}")
        print(f"{dex_file} - 计算signature: {new_signature.hex()}")

        # 将新签名写回文件头
        f.seek(12)
        f.write(new_signature)

def processDexFile(dex_file_path):
    if repairChecksum(dex_file_path):
        repairSignature(dex_file_path)
    else:
        print(f"{dex_file_path} - 校验和无误，未进行任何修改")

def processDexFiles(directory):
    with ThreadPoolExecutor() as executor:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".dex"):
                    dex_file_path = os.path.join(root, file)
                    executor.submit(processDexFile, dex_file_path)

directory = "."
processDexFiles(directory)
