"""
- 主要功能：使用离散小波变换(DWT)进行脑电信号特征提取
- 关键特点：
- 使用db4小波基函数进行信号分解
- 分析不同频带(Delta, Theta, Alpha, Beta, Gamma)的特征
- 提取每个频带的统计特征(能量、均值、标准差、峰度、偏度等)
- 使用滑动窗口方法进行特征提取
"""
# 在导入部分添加字体设置
import mne
import numpy as np
import pandas as pd
import pywt
import os
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import matplotlib
from uploadFile import upload_file  # 导入上传文件的函数

# 设置中文字体支持
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun', 'Arial Unicode MS']  # 优先使用的中文字体
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
matplotlib.rcParams['font.family'] = 'sans-serif'  # 使用无衬线字体

# 读取EEG数据
def read_eeg_data(file_path):
    raw = mne.io.read_raw_edf(file_path, preload=True)
    data = raw.get_data()
    sfreq = raw.info['sfreq']
    channel_names = raw.info['ch_names'] if 'ch_names' in raw.info else [f"Channel_{i+1}" for i in range(data.shape[0])]
    return data, sfreq, channel_names

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

    return decomposed_signals, freq_band_names

# 滑动窗口特征提取函数
def sliding_window_wavelet(data, window_size, step_size, sfreq, channel_names=None):
    n_samples = int(window_size * sfreq)
    step = int(step_size * sfreq)
    n_channels = data.shape[0]

    if channel_names is None:
        channel_names = [f"Channel_{i+1}" for i in range(n_channels)]

    features = []
    # 存储每个频带的能量随时间变化
    band_energy_over_time = {band: {ch: [] for ch in channel_names} for band in ['Delta', 'Theta', 'Alpha', 'Beta', 'Gamma']}

    for start in range(0, data.shape[1] - n_samples + 1, step):
        end = start + n_samples
        segment = data[:, start:end]

        segment_features = {}
        for i in range(n_channels):
            channel_name = channel_names[i] if i < len(channel_names) else f"Channel_{i+1}"
            
            # 小波分解
            decomposed_signals, freq_band_names = wavelet_decompose(segment[i], sfreq)

            # 提取每个频带的特征
            for band_name, decomposed_signal in decomposed_signals.items():
                # 1. 频带能量
                energy = np.sum(np.square(decomposed_signal))
                band_energy_over_time[band_name][channel_name].append(energy)

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
                segment_features[f'{channel_name}_{band_name}_Energy'] = energy
                segment_features[f'{channel_name}_{band_name}_Mean'] = mean
                segment_features[f'{channel_name}_{band_name}_Std'] = std
                segment_features[f'{channel_name}_{band_name}_Min'] = min_val
                segment_features[f'{channel_name}_{band_name}_Max'] = max_val
                segment_features[f'{channel_name}_{band_name}_Range'] = range_val
                segment_features[f'{channel_name}_{band_name}_Kurtosis'] = kurtosis
                segment_features[f'{channel_name}_{band_name}_Skewness'] = skewness

        features.append(segment_features)

    return features, band_energy_over_time

# 创建保存结果的文件夹
def create_results_folder():
    # 创建带有时间戳的文件夹名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_folder = f"e:\\Code\\medicine-care\\medicine-ui\\EegFunction\\results\\dwt_{timestamp}"
    
    # 确保文件夹存在
    os.makedirs(results_folder, exist_ok=True)
    return results_folder

# 可视化频带能量随时间变化
# 修改可视化频带能量随时间变化函数，添加上传功能
def visualize_band_energy(band_energy_over_time, results_folder, max_channels=5):
    bands = list(band_energy_over_time.keys())
    uploaded_urls = []
    
    for band in bands:
        plt.figure(figsize=(15, 8))
        channels = list(band_energy_over_time[band].keys())
        
        # 限制显示的通道数量
        display_channels = channels[:max_channels] if len(channels) > max_channels else channels
        
        for channel in display_channels:
            plt.plot(band_energy_over_time[band][channel], label=channel)
        
        plt.xlabel('窗口索引')
        plt.ylabel('能量')
        plt.title(f'{band}频带能量随时间变化')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        
        # 保存图片
        img_path = os.path.join(results_folder, f'{band}_energy_over_time.png')
        plt.savefig(img_path)
        plt.close()
        
        # 上传图片
        url = upload_file(img_path)
        if url:
            uploaded_urls.append({"file": img_path, "url": url})
    
    return uploaded_urls

# 修改可视化频带分解信号函数，添加上传功能
def visualize_decomposed_signals(signal, decomposed_signals, sfreq, channel_name, results_folder):
    plt.figure(figsize=(15, 12))
    
    # 原始信号
    plt.subplot(6, 1, 1)
    time = np.arange(len(signal)) / sfreq
    plt.plot(time, signal)
    plt.title(f'原始信号 - {channel_name}')
    plt.xlabel('时间 (秒)')
    plt.ylabel('幅度')
    
    # 分解信号
    bands = list(decomposed_signals.keys())
    for i, band in enumerate(bands):
        plt.subplot(6, 1, i+2)
        decomposed_signal = decomposed_signals[band]
        time = np.arange(len(decomposed_signal)) / sfreq
        plt.plot(time, decomposed_signal)
        plt.title(f'{band}频带 ({band_ranges[band][0]}-{band_ranges[band][1]} Hz)')
        plt.xlabel('时间 (秒)')
        plt.ylabel('幅度')
    
    plt.tight_layout()
    
    # 保存图片
    img_path = os.path.join(results_folder, f'decomposed_signals_{channel_name}.png')
    plt.savefig(img_path)
    plt.close()
    
    # 上传图片
    url = upload_file(img_path)
    if url:
        return {"file": img_path, "url": url}
    return None

# 修改处理EEG数据并提取DWT特征函数，收集所有上传的URL
def process_eeg_data(file_path, window_size_sec=5, step_size_sec=3, max_channels=5):
    # 创建结果文件夹
    results_folder = create_results_folder()
    
    # 读取EEG数据
    data, sfreq, channel_names = read_eeg_data(file_path)
    print(f"数据形状: {data.shape}, 采样率: {sfreq}Hz, 通道数: {len(channel_names)}")
    
    # 限制处理的通道数
    if max_channels and max_channels < data.shape[0]:
        selected_data = data[:max_channels]
        selected_channels = channel_names[:max_channels]
    else:
        selected_data = data
        selected_channels = channel_names
    
    # 提取滑动窗口中的小波分解特征
    features, band_energy_over_time = sliding_window_wavelet(
        selected_data, window_size_sec, step_size_sec, sfreq, selected_channels
    )
    
    # 收集所有上传的URL
    all_uploaded_urls = []
    
    # 可视化频带能量随时间变化并上传
    energy_urls = visualize_band_energy(band_energy_over_time, results_folder)
    all_uploaded_urls.extend(energy_urls)
    
    # 可视化第一个通道的分解信号并上传
    if len(selected_data) > 0:
        # 取一小段数据进行可视化
        sample_length = int(10 * sfreq)  # 10秒数据
        sample_signal = selected_data[0, :sample_length]
        decomposed_signals, _ = wavelet_decompose(sample_signal, sfreq)
        
        # 定义频带范围用于图表标题
        global band_ranges
        band_ranges = {
            'Delta': [0.5, 4],
            'Theta': [4, 8],
            'Alpha': [8, 13],
            'Beta': [13, 30],
            'Gamma': [30, 250]
        }
        
        decomp_url = visualize_decomposed_signals(
            sample_signal, decomposed_signals, sfreq, 
            selected_channels[0], results_folder
        )
        if decomp_url:
            all_uploaded_urls.append(decomp_url)
    
    # 打印所有上传的URL
    print(f"共上传了 {len(all_uploaded_urls)} 张图片")
    for item in all_uploaded_urls:
        print(f"文件: {item['file']} -> URL: {item['url']}")
    
    print(f"结果已保存到: {results_folder}")
    return results_folder, features, all_uploaded_urls

if __name__ == "__main__":
    # 示例用法
    file_path = 'E:/Code/medicine-care/medicine-ui/EegFunction/data/chb01/chb01_03.edf'
    
    # 处理EEG数据并提取DWT特征
    results_folder, features, uploaded_urls = process_eeg_data(
        file_path,
        window_size_sec=5,  # 窗口大小(秒)
        step_size_sec=3,    # 步长(秒)
        max_channels=5      # 最多处理的通道数
    )
    
    print(f"DWT分析完成，结果保存在: {results_folder}")
    print(f"所有上传的图片URL:")
    for item in uploaded_urls:
        print(f"{item['file']} -> {item['url']}")
