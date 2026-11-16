import os
from pathlib import Path

# ==========================================
# 1. 配置你的害虫数据集路径 (请根据实际情况微调)
# ==========================================
# 这里放你刚刚拷进去的“纯病害叶片（无虫）”图片的文件夹
IMAGE_DIR = Path(r"D:\-EcoNexus-\ai_training\datasets\pests_data\train\images")

# 这里是对应的标签文件夹（脚本会在这里面自动生成空 txt）
LABEL_DIR = Path(r"D:\-EcoNexus-\ai_training\datasets\pests_data\train\labels")

print("🚀 天衍·负样本空标签全自动生成器启动...")

# 确保标签文件夹存在，没有就自动建一个
LABEL_DIR.mkdir(parents=True, exist_ok=True)

valid_extensions = {'.jpg', '.jpeg', '.png'}
create_count = 0
skip_count = 0

# 2. 扫描图片并生成空 txt
for img_path in IMAGE_DIR.iterdir():
    if img_path.is_file() and img_path.suffix.lower() in valid_extensions:
        # 提取图片文件名（不要后缀），比如 '3.jpg' 变成 '3'
        txt_filename = f"{img_path.stem}.txt"
        txt_path = LABEL_DIR / txt_filename

        # 核心逻辑：只有当 txt 不存在时才创建（防止覆盖你之前真正标了虫子的有效标签）
        if not txt_path.exists():
            with open(txt_path, 'w', encoding='utf-8') as f:
                pass  # pass 意味着不写入任何内容，直接生成 0KB 的空文件
            create_count += 1
        else:
            skip_count += 1

print("\n=========================================")
print("✅ 负样本标签注入完成！")
print(f"📄 成功新建空标签 : {create_count} 个")
print(f"⏭️ 跳过已有标签   : {skip_count} 个 (保护原有数据不被破坏)")
print("=========================================")
print("现在，请直接去运行 train_pest.py 重新淬炼你的找虫大脑吧！")