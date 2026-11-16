import os
import pandas as pd
import json
import shutil
from sklearn.model_selection import train_test_split

# 1. 绝对路径配置 (请确保与你的实际环境一致)
base_dir = r"C:\Users\admin\PycharmProjects\-EcoNexus-\datasets\crop_disease_dataset"
csv_path = os.path.join(base_dir, "meta_deta.csv")
json_path = os.path.join(base_dir, "class_names.json")
img_dir = os.path.join(base_dir, "images")

# 2. 读取映射字典和 CSV 数据
with open(json_path, 'r', encoding='utf-8') as f:
    class_mapping = json.load(f)

df = pd.read_csv(csv_path)
print(f"✅ 成功读取病害档案，总计发现 {len(df)} 张作物切片...")

# 3. 黄金比例划分：训练集 (80%) 和 验证集 (20%)
# 使用 stratify 保证每种病害在训练集和验证集中的比例均匀
train_df, val_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df['label'])


# 4. 构建 YOLO 分类专属的独立目录树
def build_yolo_cls_dataset(data_frame, split_name):
    split_dir = os.path.join(base_dir, split_name)
    os.makedirs(split_dir, exist_ok=True)

    for index, row in data_frame.iterrows():
        img_name = str(row['image_id'])
        label_id = str(row['label'])

        # 核心：使用 JSON 中的真实病害名称作为文件夹名
        real_class_name = class_mapping.get(label_id, f"Class_{label_id}")

        class_dir = os.path.join(split_dir, real_class_name)
        os.makedirs(class_dir, exist_ok=True)

        src_path = os.path.join(img_dir, img_name)
        dst_path = os.path.join(class_dir, img_name)

        if os.path.exists(src_path):
            shutil.copy(src_path, dst_path)
        else:
            print(f"⚠️ 警告: 找不到图片 {src_path}")


print("🚀 正在构建 YOLO 病理学训练集网络 (train)...")
build_yolo_cls_dataset(train_df, "train")

print("🚀 正在构建 YOLO 病理学验证集网络 (val)...")
build_yolo_cls_dataset(val_df, "val")

print("🏆 农田病理学数据集重组完毕！")