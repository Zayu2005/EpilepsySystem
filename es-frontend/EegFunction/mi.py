"""
- 主要功能：计算脑电信号通道间的互信息(Mutual Information)
- 关键特点：
- 使用滑动窗口方法计算通道间的互信息
- 提取通道对之间的互信息特征
- 将结果保存为CSV和NumPy格式
- 可用于分析通道间的信息交互
"""
import os
import mne
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_selection import mutual_info_regression
from datetime import datetime


# 读取EEG数据
def read_eeg_data(file_path):
    raw = mne.io.read_raw_edf(file_path, preload=True)
    data = raw.get_data()
    sfreq = raw.info['sfreq']
    channel_names = raw.info['ch_names']
    return data, sfreq, channel_names


# 计算通道之间的互信息
def calculate_mutual_information(window_data):
    n_channels = window_data.shape[0]
    mutual_info = np.zeros((n_channels, n_channels))

    # 遍历通道对并计算互信息
    for i in range(n_channels):
        for j in range(i + 1, n_channels):  # 避免计算对角线和重复
            mi = mutual_info_regression(window_data[i].reshape(-1, 1), window_data[j])[0]
            mutual_info[i, j] = mi
            mutual_info[j, i] = mi  # 对称性
    return mutual_info


# 滑动窗口提取互信息特征
def extract_features(data, window_size, step_size, feature_func):
    n_samples = data.shape[1]
    n_windows = (n_samples - window_size) // step_size + 1
    features = []

    # 在数据上应用滑动窗口
    for start in range(0, n_samples - window_size + 1, step_size):
        end = start + window_size
        window_data = data[:, start:end]
        feature = feature_func(window_data)  # 计算特征（互信息）
        features.append(feature)

    return np.array(features), n_windows


# 提取互信息矩阵的上三角部分（非对角线元素）
def extract_upper_triangle_features(features):
    n_windows = features.shape[0]
    n_channels = features.shape[1]
    upper_triangle_features = []

    # 遍历所有窗口
    for window_idx in range(n_windows):
        upper_triangle = []
        # 提取上三角部分的互信息特征
        for i in range(n_channels):
            for j in range(i + 1, n_channels):
                upper_triangle.append(features[window_idx, i, j])
        upper_triangle_features.append(upper_triangle)

    return np.array(upper_triangle_features)


# 创建保存结果的文件夹
def create_results_folder():
    # 创建带有时间戳的文件夹名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_folder = f"e:\\Code\\medicine-care\\medicine-ui\\EegFunction\\results\\mi_{timestamp}"
    
    # 确保文件夹存在
    os.makedirs(results_folder, exist_ok=True)
    return results_folder


# 可视化互信息矩阵
def visualize_mi_matrix(mi_matrix, channel_names, window_idx, results_folder):
    plt.figure(figsize=(12, 10))
    sns.heatmap(mi_matrix, annot=False, cmap='viridis', 
                xticklabels=channel_names, yticklabels=channel_names)
    plt.title(f'互信息矩阵 - 窗口 {window_idx+1}')
    plt.tight_layout()
    plt.savefig(os.path.join(results_folder, f'mi_matrix_window_{window_idx+1}.png'))
    plt.close()


# 可视化互信息随时间变化
def visualize_mi_over_time(upper_triangle_features, channel_pairs, results_folder, max_pairs=10):
    # 选择前max_pairs个通道对进行可视化
    n_pairs = min(max_pairs, len(channel_pairs))
    selected_pairs = channel_pairs[:n_pairs]
    
    plt.figure(figsize=(15, 8))
    for i in range(n_pairs):
        plt.plot(upper_triangle_features[:, i], label=selected_pairs[i])
    
    plt.xlabel('窗口索引')
    plt.ylabel('互信息值')
    plt.title('通道对互信息随时间变化')
    plt.legend(loc='upper right', bbox_to_anchor=(1.15, 1))
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(results_folder, 'mi_over_time.png'))
    plt.close()


# 处理EEG数据并提取互信息特征
def process_eeg_data(file_path, window_size_sec=1, step_size_sec=1, visualize_windows=None):
    # 创建结果文件夹
    results_folder = create_results_folder()
    
    # 读取EEG数据
    data, sfreq, channel_names = read_eeg_data(file_path)
    print(f"数据形状: {data.shape}, 采样率: {sfreq}Hz, 通道数: {len(channel_names)}")
    
    # 转换秒到样本数
    window_size = int(sfreq * window_size_sec)
    step_size = int(sfreq * step_size_sec)
    
    # 提取特征并计算总窗口数
    features, n_windows = extract_features(data, window_size, step_size, calculate_mutual_information)
    print(f"提取了 {n_windows} 个窗口的互信息特征")
    
    # 获取通道对名称
    n_channels = len(channel_names)
    channel_pairs = []
    for i in range(n_channels):
        for j in range(i + 1, n_channels):
            channel_pairs.append(f"{channel_names[i]}-{channel_names[j]}")
    
    # 提取上三角部分的互信息特征
    upper_triangle_features = extract_upper_triangle_features(features)
    
    # 可视化部分窗口的互信息矩阵
    if visualize_windows is None:
        # 默认可视化第一个、中间和最后一个窗口
        visualize_windows = [0, n_windows//2, n_windows-1]
    
    for window_idx in visualize_windows:
        if 0 <= window_idx < n_windows:
            visualize_mi_matrix(features[window_idx], channel_names, window_idx, results_folder)
    
    # 可视化互信息随时间变化
    visualize_mi_over_time(upper_triangle_features, channel_pairs, results_folder)
    
    # 创建DataFrame并保存为CSV
    df = pd.DataFrame(upper_triangle_features, columns=channel_pairs)
    df.index = [f"Window_{i+1}" for i in range(n_windows)]
    df.to_csv(os.path.join(results_folder, 'mi_features.csv'))
    
    # 保存特征为NumPy文件
    np.save(os.path.join(results_folder, 'mi_features.npy'), features)
    
    print(f"结果已保存到: {results_folder}")
    return results_folder


if __name__ == "__main__":
    # 示例用法
    file_path = 'E:/Code/medicine-care/medicine-ui/EegFunction/data/chb01/chb01_03.edf'
    
    # 处理EEG数据并提取互信息特征
    results_folder = process_eeg_data(
        file_path,
        window_size_sec=1,    # 窗口大小(秒)
        step_size_sec=1,      # 步长(秒)
        visualize_windows=[0, 5, 10]  # 可视化第1、第6和第11个窗口
    )
    
    print(f"互信息分析完成，结果保存在: {results_folder}")
