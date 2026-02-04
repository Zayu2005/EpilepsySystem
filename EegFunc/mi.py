import os
import mne
import numpy as np
from sklearn.feature_selection import mutual_info_regression
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import FontProperties
import matplotlib
from tqdm import tqdm  # 添加进度条显示


# 读取EEG数据
def read_eeg_data(file_path):
    raw = mne.io.read_raw_edf(file_path, preload=True)
    data = raw.get_data()
    sfreq = raw.info['sfreq']
    channel_names = raw.info['ch_names']
    return data, sfreq, channel_names


# 计算通道之间的互信息
def calculate_mutual_information(window_data):
    """优化的互信息计算函数"""
    n_channels = window_data.shape[0]
    mutual_info = np.zeros((n_channels, n_channels))
    
    # 使用向量化操作计算互信息
    for i in range(n_channels):
        for j in range(i + 1, n_channels):
            # 确保数据是一维的
            x = window_data[i].reshape(-1)
            y = window_data[j].reshape(-1)
            mi = mutual_info_regression(x.reshape(-1, 1), y)[0]
            mutual_info[i, j] = mi
            mutual_info[j, i] = mi  # 对称性
    
    return mutual_info


# 滑动窗口提取互信息特征
def extract_features(data, window_size, step_size, feature_func):
    """优化的特征提取函数"""
    n_samples = data.shape[1]
    n_windows = (n_samples - window_size) // step_size + 1
    features = np.zeros((n_windows, data.shape[0], data.shape[0]))
    
    # 使用tqdm显示进度
    for i in tqdm(range(n_windows), desc="计算互信息"):
        start = i * step_size
        end = start + window_size
        window_data = data[:, start:end]
        features[i] = feature_func(window_data)
    
    return features, n_windows

def main():
    # 读取数据
    file_path = 'E:/Code/medicine-care/EegFunc/chb01/chb01_03.edf'
    data, sfreq, channel_names = read_eeg_data(file_path)
    
    # 设置参数
    window_size = int(sfreq * 1)  # 1s
    step_size = int(sfreq * 1)
    
    # 创建输出目录
    output_dir = 'E:/Code/medicine-care/EegFunc/miResult'
    os.makedirs(output_dir, exist_ok=True)
    
    # 提取特征
    print("开始提取特征...")
    features, n_windows = extract_features(data, window_size, step_size, calculate_mutual_information)
    
    # 设置绘图样式
    setup_plot_style()
    
    # 直接进行可视化
    print("正在生成可视化结果...")
    
    # 选择要展示的通道对数量
    n_display_channels = min(10, len(channel_names))
    
    # 创建综合可视化图
    fig = plt.figure(figsize=(20, 15))
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.2])
    
    # 1. 热图
    ax1 = fig.add_subplot(gs[0, 0])
    sns.heatmap(features[0], 
                xticklabels=channel_names,
                yticklabels=channel_names,
                cmap='coolwarm',
                center=np.mean(features[0]),
                ax=ax1)
    ax1.set_title('互信息矩阵热图 (第一个时间窗口)')
    
    # 2. 时间序列图
    ax2 = fig.add_subplot(gs[0, 1])
    for i in range(n_display_channels):
        for j in range(i+1, n_display_channels):
            label = f'{channel_names[i]}-{channel_names[j]}'
            ax2.plot(range(n_windows), features[:, i, j], 
                    label=label, alpha=0.7)
    ax2.set_title('互信息时间序列 (前10个通道对)')
    ax2.set_xlabel('时间窗口')
    ax2.set_ylabel('互信息值')
    ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # 3. 分布图
    ax3 = fig.add_subplot(gs[1, :])
    data_to_plot = []
    labels = []
    for i in range(n_display_channels):
        for j in range(i+1, n_display_channels):
            data_to_plot.append(features[:, i, j])
            labels.append(f'{channel_names[i]}-{channel_names[j]}')
    
    ax3.boxplot(data_to_plot, labels=labels)
    ax3.set_xticklabels(labels, rotation=45)
    ax3.set_title('互信息分布')
    ax3.set_ylabel('互信息值')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'mi_analysis.png'), dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"分析结果已保存到 {output_dir}")

if __name__ == "__main__":
    main()
