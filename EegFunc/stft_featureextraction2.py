import numpy as np
import seaborn as sns
from scipy.signal import butter, lfilter
from scipy import signal
import mne
import matplotlib.pyplot as plt
from scipy.signal import stft

def read_eeg_data(file_path):
    raw = mne.io.read_raw_edf(file_path, preload=True)
    data = raw.get_data()
    sfreq = raw.info['sfreq']
    return data, sfreq

def getSpectral_STFT(data,fs):
    # 设置STFT的参数
    window_size = 10  # 窗口大小，例如0.5秒 STFT中用于分析信号的窗口长度
    hop_length = 5  # 步长  例如0.1秒 连续两个STFT窗口之间的时间间隔
    #n_fft = 512  # FFT的点数 对每个窗口应用快速傅里叶变换（FFT）时使用的点数

    # 计算窗口的样本数和步进的样本数
    nperseg = int(window_size * fs) #1*500=500  窗口样本数 (nperseg)表示实际用于FFT的样本数。
    noverlap =int(hop_length * fs) #0.5*500=250  重叠样本数 (noverlap)表示连续两个窗口之间的重叠样本数

    # 应用STFT  功率谱密度:分析信号在不同频率上的功率分布随时间的变化
    # 频率轴 (freqs)：这是STFT结果中用于表示频率的数组。freqs 的数值是通过 n_fft 和 fs 计算得到的。
    # 时间轴 (times)：这是STFT结果中用于表示时间的数组。times 的数值是基于窗口中心的时间点，考虑到步长和采样频率来计算的。
    # 功率谱密度 (Pxx)：这是一个二维数组，其列数对应于 times 的长度，行数对应于 freqs 的长度。Pxx 中的每个元素 [i, j] 表示在第 i 个时间点和第 j 个频率上的功率谱密度估计。
    freqs, times, Pxx = stft(data, fs=fs, nperseg=nperseg,noverlap=noverlap)#, nfft=n_fft
    #f, t, Zxx = stft(x, fs, nperseg=256)
    #打印Pxx的形状以确认（n_channels, n_freqs, n_times）
    print("Pxx 形状:", Pxx.shape)  # (126, 2501, 1226)

    Pxx = np.transpose(Pxx, (0, 2, 1))
    # 打印Pxx的形状以确认 n_channels, n_times, n_freqs
    print("Pxx 转置后形状:", Pxx.shape)  # (126, 1226, 2501)

    # 从频谱中去除不需要的频率范围
    Pxx = np.concatenate((Pxx[:, :, 1:48], Pxx[:, :, 53:97], Pxx[:, :, 104:]), axis=-1)

    # 归一化STFT结果
    stft_data = (10 * np.log10(Pxx) - (10 * np.log10(Pxx)).min()) / (10 * np.log10(Pxx)).ptp()

    print("STFT结果的形状为 {}".format(stft_data.shape))  #126, 1226, 2488

    return freqs, times, stft_data



file_path = 'G:\\Database\\XJ\\xj2\\xj2-01.edf'  #141.998 secs 2min22s
data, sfreq = read_eeg_data(file_path)
print(data.shape,sfreq)  #(126, 3062500) 500.0   (通道数，采样点数6125x500=3062500)

# 计算STFT
freqs, times, stft_data = getSpectral_STFT(data, sfreq)

print(f"频率轴形状: {freqs.shape}")   #2501
print(f"时间轴形状: {times.shape}")    #1226
print(f"STFT数据形状: {stft_data.shape}")   #(126, 1226, 2488)
# # 重新生成时间轴 t
# t_new = np.linspace(0, stft_data.shape[-1] / sfreq, num=stft_data.shape[-1] + 1)
#
# # 重新生成频率轴 f
# f_new = np.linspace(0, sfreq / 2, num=stft_data.shape[1] + 1)

# 重新生成时间轴 t
# 确保时间轴长度与STFT数据的时间轴长度一致
t_new = np.linspace(0, (stft_data.shape[1] - 1) * (1 / sfreq), num=stft_data.shape[1])

# 重新生成频率轴 f
# 确保频率轴长度与STFT数据的频率轴长度一致
f_new = np.linspace(0, sfreq / 2, num=stft_data.shape[2])


'''
n_channels = stft_data.shape[0]  # 通道数
time_window_size = 1000  # 每次显示的时间窗口大小   100/500=# 0.5s
n_time_steps = stft_data.shape[1]

# 设置每个通道的图表
for channel_index in range(n_channels):
    start_index = 0
    while start_index < n_time_steps:
        end_index = min(start_index + time_window_size, n_time_steps)

        plt.figure(figsize=(12, 8))
        plt.pcolormesh(t_new[start_index:end_index], f_new, stft_data[channel_index, start_index:end_index, :].T, shading='auto')
        plt.colorbar(label='Power Spectral Density (dB/Hz)')
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        plt.title('STFT Power Spectral Density for Channel {} (Time Window: {} to {})'.format(channel_index + 1, start_index, end_index))

        # 显示当前窗口的图表
        plt.show()

        # 等待用户输入以继续查看下一个时间窗口
        input("Press Enter to continue to the next time window...")

        start_index += time_window_size

# 提示完成所有通道的查看
print("All channels and time windows have been displayed.")
'''

n_channels = stft_data.shape[0]  # 通道数

# 设置每个通道的图表
for channel_index in range(n_channels):
    plt.figure(figsize=(12, 8))
    plt.pcolormesh(t_new, f_new, stft_data[channel_index], shading='auto')
    plt.colorbar(label='Power Spectral Density(Hz)')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.title('STFT Power Spectral Density for Channel {}'.format(channel_index + 1))

    # 显示当前通道的图表，并暂停以供查看
    plt.show()


'''

def getSpectral_STFT(data, fs, window_size_sec, hop_length_sec):
    nperseg = int(window_size_sec * fs)
    noverlap = int(hop_length_sec * fs)
    freqs, times, Pxx = signal.spectrogram(data, fs=fs, nperseg=nperseg, noverlap=noverlap)
    print("Pxx 形状 :", Pxx.shape)   #(161, 501, 141) c,f,t
    Pxx = np.transpose(Pxx, (0, 2, 1))
    Pxx = np.concatenate((Pxx[:, :, 1:48], Pxx[:, :, 53:97], Pxx[:, :, 104:]), axis=-1)
    #stft_data = 10 * np.log10(Pxx)  # 归一化功率谱密度
    stft_data = (10 * np.log10(Pxx) - (10 * np.log10(Pxx)).min()) / (10 * np.log10(Pxx)).ptp()
    print("STFT结果的形状为 {}".format(stft_data.shape))  #(161, 141, 488) c,t,f

    return freqs, times, stft_data


# 读取EEG数据
file_path = 'G:\\Database\\XJ\\xj1\\xj1-08.edf'
data, sfreq = read_eeg_data(file_path)
print(data.shape,sfreq)  #(161, 71000) 500.0   (通道数，采样点数142sx500HZ=71000)

# STFT参数
window_size_sec = 2  # 窗口大小，单位秒
hop_length_sec = 1  # 步长，单位秒

# 计算STFT
freqs, times, stft_data = getSpectral_STFT(data, sfreq, window_size_sec, hop_length_sec)

# 可视化STFT结果，使用滑动窗口
n_channels, n_time_steps, n_freqs = stft_data.shape
t_new = np.linspace(0, (stft_data.shape[1] - 1) * (1 / sfreq), num=stft_data.shape[1])
f_new = np.linspace(0, sfreq / 2, num=stft_data.shape[2])

for channel_index in range(n_channels):
    start_time = 0  # 以秒为单位的起始时间
    while start_time < ((n_time_steps - 1) * hop_length_sec):
        end_time = start_time + window_size_sec

        # 计算当前窗口的起始和结束样本索引
        start_sample = int(start_time * sfreq)
        end_sample = int(np.minimum(end_time * sfreq, len(t_new)))

        plt.figure(figsize=(12, 8))
        plt.pcolormesh(t_new,
                       f_new,
                       stft_data[channel_index, start_sample:end_sample, :].T,
                       shading='auto')
        plt.colorbar(label='Power Spectral Density (dB/Hz)')
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        plt.title(f'STFT Power Spectral Density for Channel {channel_index + 1}')

        plt.show()
        #plt.close()  # 关闭当前图像，防止内存问题

        # 等待用户输入以继续查看下一个时间窗口
        input("按 Enter 键继续查看下一个时间窗口...")

        # 更新到下一个时间窗口
        start_time += hop_length_sec / sfreq

print("All channels and time windows have been displayed.")
'''