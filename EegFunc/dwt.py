# 导入必要的库
import mne
import numpy as np
import pandas as pd
import pywt
import os
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.font_manager import FontProperties
import seaborn as sns

# 设置matplotlib的全局样式
def setup_plot_style():
    plt.style.use('seaborn-v0_8-whitegrid')
    
    # 设置字体和样式
    font_list = ['Microsoft YaHei', 'SimHei', 'Arial']
    font_found = False
    for font_name in font_list:
        try:
            font = FontProperties(font_name)
            matplotlib.rcParams['font.family'] = font.get_name()
            font_found = True
            break
        except:
            continue
    
    if not font_found:
        matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    
    # 设置全局样式
    matplotlib.rcParams.update({
        'axes.unicode_minus': False,
        'font.size': 12,
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.titlesize': 16,
        'figure.dpi': 100,
        'savefig.dpi': 300,
        'axes.grid': True,
        'grid.alpha': 0.3,
        'axes.axisbelow': True,
        'axes.linewidth': 1.5
    })

# 调用样式设置函数
setup_plot_style()

# 读取EEG数据
def read_eeg_data(file_path):
    raw = mne.io.read_raw_edf(file_path, preload=True)
    data = raw.get_data()
    sfreq = raw.info['sfreq']
    return data, sfreq

# 小波分解函数
def wavelet_decompose(signal, sfreq):
    wavelet = 'db4'
    max_level = pywt.dwt_max_level(len(signal), wavelet)
    coeffs = pywt.wavedec(signal, wavelet, level=max_level)

    # 定义频带
    delta_band = [0.5, 4]
    theta_band = [4, 8]
    alpha_band = [8, 13]
    beta_band = [13, 30]
    gamma_band = [30, 250]

    freq_bands = [delta_band, theta_band, alpha_band, beta_band, gamma_band]
    freq_band_names = ['Delta', 'Theta', 'Alpha', 'Beta', 'Gamma']

    decomposed_signals = {}

    # 计算小波系数的频率范围
    for i, band in enumerate(freq_bands):
        band_coeffs = [np.zeros_like(c) for c in coeffs]
        for j in range(len(coeffs)):
            f_min = sfreq / (2 ** (j + 1))
            f_max = sfreq / (2 ** j)
            if f_min < band[1] and f_max > band[0]:
                band_coeffs[j] = coeffs[j]
        decomposed_signals[freq_band_names[i]] = pywt.waverec(band_coeffs, wavelet)

    return decomposed_signals

# 滑动窗口特征提取函数
def sliding_window_wavelet(data, window_size, step_size, sfreq):
    n_samples = int(window_size * sfreq)
    step = int(step_size * sfreq)
    n_channels = data.shape[0]

    features = []

    for start in range(0, data.shape[1] - n_samples + 1, step):
        end = start + n_samples
        segment = data[:, start:end]

        segment_features = {}
        for i in range(n_channels):
            # 小波分解
            decomposed_signals = wavelet_decompose(segment[i], sfreq)

            # 提取每个频带的特征
            for band_name, decomposed_signal in decomposed_signals.items():
                # 1. 频带能量
                energy = np.sum(np.square(decomposed_signal))

                # 2. 频带的统计特征
                mean = np.mean(decomposed_signal)
                std = np.std(decomposed_signal)
                min_val = np.min(decomposed_signal)
                max_val = np.max(decomposed_signal)
                range_val = max_val - min_val

                # 3. 小波系数的分布特征
                kurtosis = pd.Series(decomposed_signal).kurtosis()
                skewness = pd.Series(decomposed_signal).skew()

                # 保存特征
                segment_features[f'Channel_{i + 1}_{band_name}_Energy'] = energy
                segment_features[f'Channel_{i + 1}_{band_name}_Mean'] = mean
                segment_features[f'Channel_{i + 1}_{band_name}_Std'] = std
                segment_features[f'Channel_{i + 1}_{band_name}_Min'] = min_val
                segment_features[f'Channel_{i + 1}_{band_name}_Max'] = max_val
                segment_features[f'Channel_{i + 1}_{band_name}_Range'] = range_val
                segment_features[f'Channel_{i + 1}_{band_name}_Kurtosis'] = kurtosis  #峰度
                segment_features[f'Channel_{i + 1}_{band_name}_Skewness'] = skewness   #偏度

        features.append(segment_features)

    return features

# 文件路径
file_path = 'E:/Code/medicine-care/EegFunc/chb01/chb01_03.edf'
data, sfreq = read_eeg_data(file_path)

# 滑动窗口参数
window_size = 5  # 窗口大小，以秒为单位
step_size = 3  # 步长，以秒为单位

# 提取滑动窗口中的小波分解特征
features = sliding_window_wavelet(data, window_size, step_size, sfreq)

# 创建结果保存目录
result_dir = 'E:/Code/medicine-care/EegFunc/dwtResult'
if not os.path.exists(result_dir):
    os.makedirs(result_dir)

# 转换为DataFrame并保存
df_features = pd.DataFrame(features)
output_csv_file = os.path.join(result_dir, 'dwt_features.csv')
df_features.to_csv(output_csv_file, index=False)

# 保存特征为npy文件
output_npy_file = os.path.join(result_dir, 'dwt_features.npy')
np.save(output_npy_file, features)

# 添加可视化功能
# 1. 可视化原始信号和小波分解结果
# 设置matplotlib支持中文显示
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
matplotlib.rcParams['axes.unicode_minus'] = False  # 正常显示负号
matplotlib.rcParams['font.family'] = 'sans-serif'

def visualize_wavelet_decomposition(data, sfreq, channel_idx=0, time_window=10):
    """可视化指定通道的原始信号和小波分解结果"""
    signal = data[channel_idx, :int(time_window * sfreq)]
    time = np.arange(len(signal)) / sfreq
    
    decomposed_signals = wavelet_decompose(signal, sfreq)
    
    # 创建更美观的图形布局
    fig = plt.figure(figsize=(15, 12))
    gs = fig.add_gridspec(6, 1, height_ratios=[1.2, 1, 1, 1, 1, 1], hspace=0.4)
    
    # 绘制原始信号
    ax0 = fig.add_subplot(gs[0])
    ax0.plot(time, signal, 'b-', linewidth=1.5, label='原始信号')
    ax0.set_title(f'原始EEG信号 (通道 {channel_idx+1})', pad=10)
    ax0.set_ylabel('幅值')
    ax0.legend(loc='upper right')
    
    # 绘制各频带分解结果
    colors = plt.cm.viridis(np.linspace(0, 1, len(decomposed_signals)))
    for i, (band_name, decomposed_signal) in enumerate(decomposed_signals.items()):
        ax = fig.add_subplot(gs[i+1])
        ax.plot(time, decomposed_signal[:len(time)], color=colors[i], 
                linewidth=1.5, label=f'{band_name}波')
        ax.set_title(f'{band_name}频带', pad=10)
        ax.set_ylabel('幅值')
        ax.legend(loc='upper right')
        
        # 添加频带范围标注
        if band_name == 'Delta':
            freq_range = '0.5-4 Hz'
        elif band_name == 'Theta':
            freq_range = '4-8 Hz'
        elif band_name == 'Alpha':
            freq_range = '8-13 Hz'
        elif band_name == 'Beta':
            freq_range = '13-30 Hz'
        else:  # Gamma
            freq_range = '30-250 Hz'
        
        ax.text(0.02, 0.95, freq_range, transform=ax.transAxes, 
                bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
    
    # 设置最后一个子图的x轴标签
    ax.set_xlabel('时间 (秒)')
    
    # 添加整体标题
    fig.suptitle('EEG信号小波分解分析', fontsize=16, y=0.95)
    
    # 保存图形
    plt.savefig(os.path.join(result_dir, 'wavelet_decomposition.png'), 
                bbox_inches='tight', dpi=300)
    plt.show()

def visualize_features_statistics(df_features):
    """可视化提取的特征统计分布"""
    energy_cols = [col for col in df_features.columns if 'Energy' in col]
    
    fig = plt.figure(figsize=(15, 12))
    gs = fig.add_gridspec(2, 1, height_ratios=[1, 1.5], hspace=0.3)
    
    # 箱线图
    ax1 = fig.add_subplot(gs[0])
    sns.boxplot(data=df_features[energy_cols], orient='h', ax=ax1)
    ax1.set_title('各频带能量特征分布', pad=10)
    ax1.set_xlabel('能量值')
    
    # 时间序列图
    ax2 = fig.add_subplot(gs[1])
    for col in energy_cols:
        ax2.plot(df_features.index, df_features[col], 
                 label=col.split('_')[1], linewidth=1.5)
    
    ax2.set_title('各频带能量随时间变化', pad=10)
    ax2.set_xlabel('窗口索引')
    ax2.set_ylabel('能量值')
    ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.suptitle('EEG信号能量特征分析', fontsize=16, y=0.95)
    plt.tight_layout()
    plt.savefig(os.path.join(result_dir, 'features_statistics.png'), 
                bbox_inches='tight', dpi=300)
    plt.show()

def visualize_features_heatmap(df_features):
    """可视化特征相关性热图"""
    plt.figure(figsize=(20, 16))
    
    # 计算相关性矩阵
    corr = df_features.corr()
    
    # 创建掩码，只显示上三角矩阵
    mask = np.triu(np.ones_like(corr, dtype=bool))
    
    # 绘制热图
    sns.heatmap(corr, mask=mask, cmap='coolwarm', center=0,
                square=True, linewidths=0.5, cbar_kws={"shrink": .5},
                vmin=-1, vmax=1, annot=False)
    
    plt.title('特征相关性热图', pad=20)
    plt.tight_layout()
    plt.savefig(os.path.join(result_dir, 'features_correlation.png'), 
                bbox_inches='tight', dpi=300)
    plt.show()

# 执行可视化
print("正在生成小波分解可视化...")
visualize_wavelet_decomposition(data, sfreq)

print("正在生成特征统计可视化...")
visualize_features_statistics(df_features)

# 导入seaborn库用于热图可视化
try:
    import seaborn as sns
    print("正在生成特征相关性热图...")
    visualize_features_heatmap(df_features)
except ImportError:
    print("未安装seaborn库，跳过热图可视化。可以通过'pip install seaborn'安装。")

print(f"特征已保存到 {output_csv_file} 和 {output_npy_file}")
print(f"可视化结果已保存到 {result_dir} 目录下")
