import torch
import sys

print("===== Torch & GPU 环境检测 =====")
print("Python版本:", sys.version)
print("PyTorch版本:", torch.__version__)
print("\n===== GPU/CUDA 状态 =====")
print("CUDA是否可用:", torch.cuda.is_available())
print("CUDA版本:", torch.version.cuda if torch.cuda.is_available() else "无")
print("检测到GPU数量:", torch.cuda.device_count())

if torch.cuda.is_available():
    print("GPU名称:", torch.cuda.get_device_name(0))
    print("当前使用GPU: 0")
else:
    print("\n❌ 未检测到支持CUDA的NVIDIA显卡，只能使用CPU训练")
    print("原因可能：")
    print("1. 电脑没有NVIDIA独立显卡")
    print("2. 安装的是CPU版PyTorch")
    print("3. CUDA未安装")