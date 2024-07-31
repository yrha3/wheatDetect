import json
import matplotlib.pyplot as plt

# 读取 JSON 文件
with open('results/test_video2/test_video2.json', 'r') as file:
    data = json.load(file)

# 确保数据是列表
if isinstance(data, list):
    frame_counts = {}
    interval = 24  # 每 24 帧作为一个统计单位

    # 统计每帧的检测数量
    for detections in data:
        if isinstance(detections, list) and len(detections) > 0:  # 是列表且不为空
            frame_number = detections[0].get('frame')
            if frame_number is not None:
                if frame_number not in frame_counts:
                    frame_counts[frame_number] = 0  # 初始化
                frame_counts[frame_number] += len(detections)

    # 统计每个区间的检测数量并计算平均值
    interval_counts = {}
    interval_sums = {}
    for frame, count in frame_counts.items():
        interval_index = (frame - 1) // interval  # 计算区间索引
        if interval_index not in interval_counts:
            interval_counts[interval_index] = 0
            interval_sums[interval_index] = 0
        interval_counts[interval_index] += 1
        interval_sums[interval_index] += count

    # 计算每个区间的平均值
    interval_averages = {i: interval_sums[i] / interval_counts[i] for i in interval_counts}

    # 准备数据用于绘图
    intervals = sorted(interval_averages.keys())
    counts = [interval_averages[i] for i in intervals]

    # 生成统计单位的中间帧作为 X 轴
    x_labels = [(i * interval + interval // 2 + 1) for i in intervals]

    # 绘制折线图
    plt.figure(figsize=(12, 6))
    plt.plot(x_labels, counts, marker='o', linestyle='-', color='blue')
    plt.xlabel('Frame Number')
    plt.ylabel('Average Number of Wheat Detections')
    plt.title('Average Wheat Detection Counts per 24 Frames')
    plt.grid(True, linestyle='--', alpha=0.7)

    # 显示每个统计区间的平均检测数量
    for i, count in zip(x_labels, counts):
        plt.text(i, count, f'{count:.2f}', fontsize=12, ha='center', va='bottom')

    plt.show()

else:
    print("Top-level data is not a list.")
