from ultralytics import YOLO

if __name__ == '__main__':
    # 1. 载入我们之前用的基础轻量级预训练模型 (站在巨人的肩膀上)
    print("正在加载 YOLOv8 初始权重...")
    model = YOLO(r"C:\Users\admin\PycharmProjects\-EcoNexus-\backend\yolov8n.pt")

    # 2. 启动训练引擎
    print(" 天衍中枢垂直大模型训练启动...")
    results = model.train(
        data="datasets/pests_data/data.yaml",  # 你的 yaml 配置文件路径
        epochs=50,  # 训练轮数（测试可以先填 50，追求高精度建议 100-300）
        imgsz=640,  # 图像输入尺寸
        batch=16,  # 批次大小（如果显存/内存爆了，改成 8 或 4）
        device="cuda",  # 留空会自动检测，如果有N卡会自动调用 GPU (CUDA)
        project="runs/detect",  # 训练结果保存的目录
        name="tianyan_pest_v1"  # 本次训练的模型代号
    )

    print(" 训练完成！专属权重已生成！")