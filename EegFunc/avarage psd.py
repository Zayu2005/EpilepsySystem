import mne
import numpy as np
import matplotlib.pyplot as plt

# 10个发作的EDF文件和对应的发作时间
# seizure_files = [
#     {'file': 'G:\\Database\\XJ\\xj2\\xj2-01.edf', 'seizure_start': 3624, 'seizure_end': 3742},
#     {'file': 'G:\\Database\\XJ\\xj2\\xj2-02.edf', 'seizure_start': 1647, 'seizure_end': 1709},
#     {'file': 'G:\\Database\\XJ\\xj2\\xj2-03.edf', 'seizure_start': 4158, 'seizure_end': 4220},
#     {'file': 'G:\\Database\\XJ\\xj2\\xj2-04.edf', 'seizure_start': 3933, 'seizure_end': 4006},
#     {'file': 'G:\\Database\\XJ\\xj2\\xj2-05.edf', 'seizure_start': 3711, 'seizure_end': 3764},
#     {'file': 'G:\\Database\\XJ\\xj2\\xj2-06.edf', 'seizure_start': 1850, 'seizure_end': 1910},
#     {'file': 'G:\\Database\\XJ\\xj2\\xj2-07.edf', 'seizure_start': 4078, 'seizure_end': 4154},
#     {'file': 'G:\\Database\\XJ\\xj2\\xj2-08.edf', 'seizure_start': 2105, 'seizure_end': 2163},
#     {'file': 'G:\\Database\\XJ\\xj2\\xj2-09.edf', 'seizure_start': 2160, 'seizure_end': 2199},
#     {'file': 'G:\\Database\\XJ\\xj2\\xj2-10.edf', 'seizure_start': 3688, 'seizure_end': 3719},
# ]

seizure_files = [
    {'file': 'G:\\Database\\XJ\\xj1\\xj1-01.edf', 'seizure_start': 3614, 'seizure_end': 3623},
    {'file': 'G:\\Database\\XJ\\xj1\\xj1-02.edf', 'seizure_start': 485, 'seizure_end': 501},
   # {'file': 'G:\\Database\\XJ\\xj2\\xj2-03.edf', 'seizure_start': 4158, 'seizure_end': 4220},
    {'file': 'G:\\Database\\XJ\\xj1\\xj104-06.edf', 'seizure_start': 777, 'seizure_end': 791},
    {'file': 'G:\\Database\\XJ\\xj1\\xj104-06.edf', 'seizure_start': 3666, 'seizure_end': 3680},
    {'file': 'G:\\Database\\XJ\\xj1\\xj1-05.edf', 'seizure_start': 3714, 'seizure_end': 3734},
    #{'file': 'G:\\Database\\XJ\\xj2\\xj2-06.edf', 'seizure_start': 1850, 'seizure_end': 1910},
    {'file': 'G:\\Database\\XJ\\xj1\\xj1-07.edf', 'seizure_start': 2019, 'seizure_end': 2067},


]

# 发作前、发作后时间段的长度 (单位：秒)
pre_duration = 300  # 发作前1min 5min 10min
post_duration = 300  # 发作后1min 5min 10min

# 初始化用于存储所有发作的 PSD
psd_pre_all = []
psd_seizure_all = []
psd_post_all = []

# 遍历所有的发作文件
for seizure_info in seizure_files:
    edf_file = seizure_info['file']
    seizure_start = seizure_info['seizure_start']
    seizure_end = seizure_info['seizure_end']

    # 加载 EDF 文件
    raw = mne.io.read_raw_edf(edf_file, preload=True)
    # 计算PSD (使用 psd_array_welch 但需指定采样频率)
    sfreq = raw.info['sfreq']  # 获取采样频率

    # 保证发作前期的开始时间不小于0
    pre_start = max(0, seizure_start - pre_duration)

    # 裁剪发作前期数据
    raw_pre_seizure = raw.copy().crop(tmin=pre_start, tmax=seizure_start)

    # 裁剪发作期数据
    raw_seizure = raw.copy().crop(tmin=seizure_start, tmax=seizure_end)

    # 裁剪发作后期数据
    raw_post_seizure = raw.copy().crop(tmin=seizure_end, tmax=seizure_end + post_duration)


    # 计算PSD (使用Welch方法)
    psd_pre, freqs_pre = mne.time_frequency.psd_array_welch(raw_pre_seizure.get_data(), sfreq=sfreq, fmin=0.5, fmax=150)
    psd_seizure, freqs_seizure = mne.time_frequency.psd_array_welch(raw_seizure.get_data(), sfreq=sfreq, fmin=0.5,
                                                                    fmax=150)
    psd_post, freqs_post = mne.time_frequency.psd_array_welch(raw_post_seizure.get_data(), sfreq=sfreq, fmin=0.5,
                                                              fmax=150)

    # 对所有通道的PSD进行平均
    psd_pre_avg = np.mean(psd_pre, axis=0)
    psd_seizure_avg = np.mean(psd_seizure, axis=0)
    psd_post_avg = np.mean(psd_post, axis=0)

    # 将每次发作的PSD加入到列表中
    psd_pre_all.append(psd_pre_avg)
    psd_seizure_all.append(psd_seizure_avg)
    psd_post_all.append(psd_post_avg)

# 计算所有发作的平均PSD
psd_pre_mean = np.mean(psd_pre_all, axis=0)
psd_seizure_mean = np.mean(psd_seizure_all, axis=0)
psd_post_mean = np.mean(psd_post_all, axis=0)

# 绘图
plt.figure(figsize=(16, 8))

# 发作前期的平均PSD对比
plt.subplot(3, 1, 1)
for i, psd in enumerate(psd_pre_all):
    plt.plot(freqs_pre, psd, label=f'Seizure{i + 1}', linestyle='--')
plt.plot(freqs_pre, psd_pre_mean, label='All Seizure Average', color='black', linestyle='-')
plt.title('Pre-Seizure - Average PSD Compare')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power Spectral Density (V^2/Hz)')
plt.legend()

# 发作期的平均PSD对比
plt.subplot(3, 1, 2)
for i, psd in enumerate(psd_seizure_all):
    plt.plot(freqs_seizure, psd, label=f'Seizure{i + 1}', linestyle='--')
plt.plot(freqs_seizure, psd_seizure_mean, label='All Seizure Average', color='black', linestyle='-')
plt.title('Seizure - Average PSD Compare')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power Spectral Density (V^2/Hz)')
plt.legend()

# 发作后期的平均PSD对比
plt.subplot(3, 1, 3)
for i, psd in enumerate(psd_post_all):
    plt.plot(freqs_post, psd, label=f'Seizure{i + 1}', linestyle='--')
plt.plot(freqs_post, psd_post_mean, label='All Seizure Average', color='black', linestyle='-')
plt.title('Post-Seizure - Average PSD Compare')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power Spectral Density (V^2/Hz)')
plt.legend()

plt.tight_layout()
plt.show()


# # 预定义时间窗口长度
# pre_seizure_window = 60  # 60秒
# post_seizure_window = 60  # 60秒
#
# # 存储所有PSD的结果
# psd_pre_all = []
# psd_seizure_all = []
# psd_post_all = []
#
# # 定义n_fft参数以确保PSD的频率点一致
# n_fft = 2048  # 设定为固定值，以保证频率分辨率一致
#
# for edf_file, seizure_start, seizure_end in seizure_files:
#     # 加载EDF文件
#     raw = mne.io.read_raw_edf(edf_file, preload=True)
#
#     # 计算发作前、发作中、发作后的时间窗口
#     pre_start = seizure_start - pre_seizure_window
#     post_end = seizure_end + post_seizure_window
#
#     # 提取不同阶段的数据
#     raw_pre_seizure = raw.copy().crop(tmin=pre_start, tmax=seizure_start)
#     raw_seizure = raw.copy().crop(tmin=seizure_start, tmax=seizure_end)
#     raw_post_seizure = raw.copy().crop(tmin=seizure_end, tmax=post_end)
#
#     # 计算各阶段的PSD，指定n_fft确保频率点一致
#     psd_pre, freqs_pre = mne.time_frequency.psd_array_welch(raw_pre_seizure.get_data(), sfreq=raw.info['sfreq'],
#                                                             fmin=0.5, fmax=150, n_fft=n_fft)
#     psd_seizure, freqs_seizure = mne.time_frequency.psd_array_welch(raw_seizure.get_data(), sfreq=raw.info['sfreq'],
#                                                                     fmin=0.5, fmax=150, n_fft=n_fft)
#     psd_post, freqs_post = mne.time_frequency.psd_array_welch(raw_post_seizure.get_data(), sfreq=raw.info['sfreq'],
#                                                               fmin=0.5, fmax=150, n_fft=n_fft)
#
#     # 将PSD叠加到列表中
#     psd_pre_all.append(psd_pre)
#     psd_seizure_all.append(psd_seizure)
#     psd_post_all.append(psd_post)
#
# # 计算平均PSD
# psd_pre_avg = np.mean(psd_pre_all, axis=0)
# psd_seizure_avg = np.mean(psd_seizure_all, axis=0)
# psd_post_avg = np.mean(psd_post_all, axis=0)
#
# # 绘制平均PSD
# plt.figure(figsize=(10, 8))
#
# # 发作前
# plt.subplot(311)
# plt.semilogy(freqs_pre, psd_pre_avg.mean(axis=0))
# plt.title('Avarage PSD - Pre-Seizure')
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('Power Spectral Density (V^2/Hz)')
#
# # 发作中
# plt.subplot(312)
# plt.semilogy(freqs_seizure, psd_seizure_avg.mean(axis=0))
# plt.title('Avarage PSD - Seizure Period')
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('Power Spectral Density (V^2/Hz)')
#
# # 发作后
# plt.subplot(313)
# plt.semilogy(freqs_post, psd_post_avg.mean(axis=0))
# plt.title('Avarage PSD - Post-Seizure')
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('Power Spectral Density (V^2/Hz)')
#
# plt.tight_layout()
# plt.show()
