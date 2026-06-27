from ultralytics import YOLO

if __name__ == '__main__':
    print("🚀 正在加载 YOLOv8 目标检测引擎 (找虫大脑)...")
    # 注意：这里是 .pt，没有任何后缀，代表这是目标检测模型
    model = YOLO("yolov8n.pt")

    print("🔥 天衍·区域化害虫检测大脑 V2.0 稳健性训练启动...")

    results = model.train(
        # 1. 指向你的害虫数据集 YAML 配置文件 (请确认路径正确)
        data=r"C:\Users\admin\PycharmProjects\-EcoNexus-\datasets\pests_data\data.yaml",

        # 2. 基础控制 (目标检测通常需要更长的时间和更高的分辨率)
        epochs=100,  # 轮数拉长，由早停机制把关
        imgsz=640,  # 找虫子必须用高分辨率，224太模糊了！
        batch=16,  # 显存不够可改为 8
        project="runs/detect",
        name="tianyan_pest_v2_robust",

        # ================== 优化器与早停==================

        val=True,
        patience=15,  # 早停：连续 15 轮验证集没提升，立刻拔电源，防止死记硬背
        optimizer='auto',  # 自动优化器：YOLO底层会智能分析数据量，通常为你分配 AdamW
        cos_lr=True,  # 余弦退火学习率：后期平滑收敛，让边界框咬得更紧
        lr0=0.01,  # 初始学习率 (保持官方推荐最佳值)
        lrf=0.01,  # 最终学习率 (降至初始的 1%)

        # ================== 光影增强 ==================

        mosaic=1.0,  # 100% 开启！将4张图拼成1张，微小目标检测的绝对核心！
        mixup=0.1,  # 10% 概率将两张图透明度混合，极大增强背景抗干扰能力
        degrees=15.0,  # 随机旋转（模拟无人机/手机随手拍倾斜）
        translate=0.1,  # 随机平移（防止模型以为虫子永远在画面正中间）
        scale=0.5,  # 随机缩放 50%（模拟摄像头的远近拉伸）
        hsv_h=0.015,  # 色差干扰
        hsv_s=0.7,  # 饱和度干扰
        hsv_v=0.4,  # 亮度干扰 (模拟大棚里的阴影与高光)
        fliplr=0.5,  # 50%概率左右翻转
        erasing=0.0,
    )

    print("害虫检测 V2.0 训练完成！马赛克增强与智能早停已全功率护航！")