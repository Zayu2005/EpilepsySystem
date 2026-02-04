"""
- 主要功能：使用短时傅里叶变换(STFT)进行时频分析
- 关键特点：
- 计算信号的时频谱
- 可视化每个通道的时频图
- 使用滑动窗口进行分析
- 提供功率谱密度的可视化
"""

import numpy as np
import seaborn as sns
from scipy.signal import butter, lfilter
from scipy import signal
import mne
import matplotlib.pyplot as plt
from scipy.signal import stft
import os
from datetime import datetime
import matplotlib
from uploadFile import upload_file  # 导入上传文件的函数

# 设置中文字体支持
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False
matplotlib.rcParams['font.family'] = 'sans-serif'

def read_eeg_data(file_path):
    raw = mne.io.read_raw_edf(file_path, preload=True)
    data = raw.get_data()
    sfreq = raw.info['sfreq']
    channel_names = raw.info['ch_names'] if 'ch_names' in raw.info else [f"Channel_{i+1}" for i in range(data.shape[0])]
    return data, sfreq, channel_names

def getSpectral_STFT(data, fs):
    # 设置STFT的参数
    window_size = 10  # 窗口大小，例如0.5秒 STFT中用于分析信号的窗口长度
    hop_length = 5  # 步长  例如0.1秒 连续两个STFT窗口之间的时间间隔
    #n_fft = 512  # FFT的点数 对每个窗口应用快速傅里叶变换（FFT）时使用的点数

    # 计算窗口的样本数和步进的样本数
    nperseg = int(window_size * fs) #1*500=500  窗口样本数 (nperseg)表示实际用于FFT的样本数。
    noverlap = int(hop_length * fs) #0.5*500=250  重叠样本数 (noverlap)表示连续两个窗口之间的重叠样本数

    # 应用STFT  功率谱密度:分析信号在不同频率上的功率分布随时间的变化
    freqs, times, Pxx = stft(data, fs=fs, nperseg=nperseg, noverlap=noverlap)#, nfft=n_fft
    
    # 确保处理复数数据 - 计算幅度谱
    Pxx = np.abs(Pxx)
    
    print("Pxx 形状:", Pxx.shape)  # (126, 2501, 1226)

    Pxx = np.transpose(Pxx, (0, 2, 1))
    # 打印Pxx的形状以确认 n_channels, n_times, n_freqs
    print("Pxx 转置后形状:", Pxx.shape)  # (126, 1226, 2501)

    # 从频谱中去除不需要的频率范围
    Pxx = np.concatenate((Pxx[:, :, 1:48], Pxx[:, :, 53:97], Pxx[:, :, 104:]), axis=-1)

    # 归一化STFT结果
    # 避免对零值取对数
    epsilon = np.finfo(float).eps  # 一个很小的数，防止log(0)
    Pxx = Pxx + epsilon
    stft_data = (10 * np.log10(Pxx) - (10 * np.log10(Pxx)).min()) / (10 * np.log10(Pxx)).ptp()

    print("STFT结果的形状为 {}".format(stft_data.shape))  #126, 1226, 2488

    return freqs, times, stft_data

# 创建保存结果的文件夹
def create_results_folder():
    # 创建带有时间戳的文件夹名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_folder = f"e:\\Code\\medicine-care\\medicine-ui\\EegFunction\\results\\stft_{timestamp}"
    
    # 确保文件夹存在
    os.makedirs(results_folder, exist_ok=True)
    return results_folder

# 处理和可视化STFT结果
def process_and_visualize_stft(file_path, max_channels=5):
    # 创建结果文件夹
    results_folder = create_results_folder()
    
    # 读取EEG数据
    data, sfreq, channel_names = read_eeg_data(file_path)
    print(f"数据形状: {data.shape}, 采样率: {sfreq}Hz")
    
    # 限制处理的通道数
    if max_channels and max_channels < data.shape[0]:
        data = data[:max_channels]
        channel_names = channel_names[:max_channels]
    
    # 计算STFT
    freqs, times, stft_data = getSpectral_STFT(data, sfreq)
    
    print(f"频率轴形状: {freqs.shape}")
    print(f"时间轴形状: {times.shape}")
    print(f"STFT数据形状: {stft_data.shape}")
    
    # 重新生成时间轴和频率轴
    t_new = np.linspace(0, (stft_data.shape[1] - 1) * (1 / sfreq), num=stft_data.shape[1])
    f_new = np.linspace(0, sfreq / 2, num=stft_data.shape[2])
    
    n_channels = stft_data.shape[0]  # 通道数
    
    # 收集所有上传的URL
    all_uploaded_urls = []
    
    # 为每个通道创建时频图并保存
    for channel_index in range(n_channels):
        channel_name = channel_names[channel_index] if channel_index < len(channel_names) else f"Channel_{channel_index+1}"
        
        plt.figure(figsize=(12, 8))
        plt.pcolormesh(t_new, f_new, stft_data[channel_index].T, shading='auto')
        plt.colorbar(label='功率谱密度 (dB/Hz)')
        plt.xlabel('时间 (秒)')
        plt.ylabel('频率 (Hz)')
        plt.title(f'通道 {channel_name} 的STFT功率谱密度')
        
        # 保存图像
        safe_channel_name = channel_name.replace('/', '_').replace('\\', '_').replace(' ', '_')
        img_path = os.path.join(results_folder, f"stft_{safe_channel_name}.png")
        plt.savefig(img_path)
        plt.close()
        
        # 上传图片
        url = upload_file(img_path)
        if url:
            all_uploaded_urls.append({"file": img_path, "url": url, "channel": channel_name})
    
    # 创建一个汇总图像，显示前几个通道的STFT
    plt.figure(figsize=(15, 10))
    
    # 确定要在汇总图中显示的通道数量
    display_channels = min(4, n_channels)  # 最多显示4个通道
    
    for i in range(display_channels):
        plt.subplot(2, 2, i+1)
        plt.pcolormesh(t_new, f_new, stft_data[i].T, shading='auto')
        plt.colorbar(label='功率谱密度 (dB/Hz)')
        plt.xlabel('时间 (秒)')
        plt.ylabel('频率 (Hz)')
        plt.title(f'{channel_names[i]}')
    
    plt.tight_layout()
    summary_img_path = os.path.join(results_folder, "stft_summary.png")
    plt.savefig(summary_img_path)
    plt.close()
    
    # 上传汇总图片
    summary_url = upload_file(summary_img_path)
    if summary_url:
        all_uploaded_urls.append({"file": summary_img_path, "url": summary_url, "channel": "汇总图"})
    
    # 打印所有上传的URL
    print(f"共上传了 {len(all_uploaded_urls)} 张图片")
    for item in all_uploaded_urls:
        print(f"通道: {item['channel']}, 文件: {item['file']} -> URL: {item['url']}")
    
    print(f"结果已保存到: {results_folder}")
    return results_folder, all_uploaded_urls

if __name__ == "__main__":
    # 示例EEG信号
    file_path = 'E:/Code/medicine-care/medicine-ui/EegFunction/data/chb01/chb01_03.edf'
    
    # 处理并可视化STFT结果
    results_folder, uploaded_urls = process_and_visualize_stft(
        file_path,
        max_channels=5  # 限制处理的通道数
    )
    
    print(f"STFT分析完成，结果保存在: {results_folder}")
    print(f"所有上传的图片URL:")
    for item in uploaded_urls:
        print(f"通道: {item['channel']} -> {item['url']}")