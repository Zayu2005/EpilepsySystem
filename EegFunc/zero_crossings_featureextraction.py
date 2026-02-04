import numpy as np
import matplotlib.pyplot as plt
import mne
import os
import pandas as pd
import matplotlib
from matplotlib.font_manager import FontProperties
import platform

def setup_matplotlib_fonts():
    """配置matplotlib的字体设置"""
    # 根据操作系统选择默认字体
    system = platform.system()
    
    if system == 'Windows':
        font_list = ['Microsoft YaHei', 'SimHei', 'SimSun']
    elif system == 'Darwin':  # macOS
        font_list = ['Arial Unicode MS', 'Heiti TC', 'STHeiti']
    else:  # Linux等其他系统
        font_list = ['DejaVu Sans', 'WenQuanYi Micro Hei', 'Droid Sans Fallback']

    # 尝试设置字体
    font_found = False
    for font_name in font_list:
        try:
            font = FontProperties(font_name)
            if font.get_name() != 'DejaVu Sans':  # 检查是否成功加载了指定字体
                matplotlib.rcParams['font.family'] = font.get_name()
                font_found = True
                print(f"成功设置字体: {font_name}")
                break
        except:
            continue

    if not font_found:
        print("警告: 未找到合适的中文字体，将使用系统默认字体")
        matplotlib.rcParams['font.sans-serif'] = ['SimHei']

    # 其他matplotlib设置
    matplotlib.rcParams['axes.unicode_minus'] = False  # 正常显示负号
    matplotlib.rcParams['font.size'] = 12  # 默认字体大小
    matplotlib.rcParams['axes.titlesize'] = 14  # 标题字体大小
    matplotlib.rcParams['axes.labelsize'] = 12  # 轴标签字体大小
    matplotlib.rcParams['xtick.labelsize'] = 10  # x轴刻度标签字体大小
    matplotlib.rcParams['ytick.labelsize'] = 10  # y轴刻度标签字体大小
    matplotlib.rcParams['legend.fontsize'] = 10  # 图例字体大小
    matplotlib.rcParams['figure.titlesize'] = 16  # 图形标题字体大小

    # 设置DPI以获得更好的显示效果
    matplotlib.rcParams['figure.dpi'] = 100
    matplotlib.rcParams['savefig.dpi'] = 300

# 在代码开始时调用字体设置函数
setup_matplotlib_fonts()

# 读取EEG数据
def read_eeg_data(file_path):
    raw = mne.io.read_raw_edf(file_path, preload=True)
    data = raw.get_data()
    sfreq = raw.info['sfreq']
    channel_names = raw.info['ch_names']
    return data, sfreq, channel_names

#计算信号的零相交次数。
def zero_crossings(signal):
    # 去除直流分量
    signal = signal - np.mean(signal)
    # 计算零相交点
    zero_crossings = np.where(np.diff(np.sign(signal)))[0]
    return len(zero_crossings)

#实现滑动窗口计算零相交次数。参数包括信号、窗口大小和步长。
def zero_crossings_sliding_window(signal, window_size, step_size):
    num_windows = (len(signal) - window_size) // step_size + 1
    crossings_per_window = []

    for i in range(num_windows):
        start = i * step_size
        end = start + window_size
        window = signal[start:end]
        crossings = zero_crossings(window)
        crossings_per_window.append(crossings)

    return np.array(crossings_per_window)

# 多通道零交叉特征提取
def extract_zero_crossings_features(data, window_size, step_size):
    n_channels = data.shape[0]
    features = []
    
    for i in range(n_channels):
        channel_data = data[i]
        crossings = zero_crossings_sliding_window(channel_data, window_size, step_size)
        features.append(crossings)
    
    return np.array(features)

# 创建结果保存目录
def create_output_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path

# 可视化零交叉特征
def visualize_zero_crossings(features, channel_names=None, save_path=None):
    n_channels = features.shape[0]
    n_windows = features.shape[1]
    
    # 设置更美观的绘图风格
    plt.style.use('seaborn-v0_8-whitegrid')
    
    # 创建多个子图，分组显示通道
    max_channels_per_plot = 5
    num_plots = (n_channels + max_channels_per_plot - 1) // max_channels_per_plot
    
    fig, axes = plt.subplots(num_plots, 1, figsize=(15, 4*num_plots), sharex=True)
    if num_plots == 1:
        axes = [axes]
    
    # 设置颜色循环
    colors = plt.cm.tab10.colors
    
    # 绘制分组的通道零交叉特征
    for plot_idx in range(num_plots):
        start_channel = plot_idx * max_channels_per_plot
        end_channel = min(start_channel + max_channels_per_plot, n_channels)
        
        for i in range(start_channel, end_channel):
            color_idx = i % len(colors)
            if channel_names is not None and i < len(channel_names):
                label = f'通道 {i+1}: {channel_names[i]}'
            else:
                label = f'通道 {i+1}'
            
            # 绘制线条并添加标记点以增强可读性
            axes[plot_idx].plot(range(n_windows), features[i], 
                               label=label, 
                               color=colors[color_idx],
                               marker='o', 
                               markersize=4, 
                               alpha=0.8)
            
            # 添加均值线
            mean_value = np.mean(features[i])
            axes[plot_idx].axhline(y=mean_value, 
                                  color=colors[color_idx], 
                                  linestyle='--', 
                                  alpha=0.5,
                                  label=f'均值: {mean_value:.1f}' if i == start_channel else None)
        
        # 设置子图标题和标签
        axes[plot_idx].set_title(f'通道组 {plot_idx+1} 的零交叉特征', fontsize=14)
        axes[plot_idx].set_ylabel('零交叉次数', fontsize=12)
        axes[plot_idx].legend(loc='upper right', fontsize=9)
        axes[plot_idx].grid(True, linestyle='--', alpha=0.7)
    
    # 设置最后一个子图的x轴标签
    axes[-1].set_xlabel('窗口索引', fontsize=12)
    
    # 添加总标题
    fig.suptitle('EEG信号各通道的零交叉特征分析', fontsize=16, y=0.98)
    
    # 调整子图之间的间距
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    # 添加统计信息文本框
    stats_text = "统计信息:\n"
    stats_text += f"总通道数: {n_channels}\n"
    stats_text += f"窗口数量: {n_windows}\n"
    stats_text += f"全局均值: {np.mean(features):.2f}\n"
    stats_text += f"全局最大值: {np.max(features):.2f}\n"
    stats_text += f"全局最小值: {np.min(features):.2f}"
    
    fig.text(0.02, 0.02, stats_text, fontsize=10,
             bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.5'))
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()
    
    # 额外创建热图显示所有通道的零交叉特征
    plt.figure(figsize=(15, 8))
    plt.imshow(features, aspect='auto', cmap='viridis')
    plt.colorbar(label='零交叉次数')
    plt.xlabel('窗口索引', fontsize=12)
    plt.ylabel('通道索引', fontsize=12)
    plt.title('零交叉特征热图', fontsize=14)
    
    # 添加y轴刻度标签（通道名称）
    if channel_names is not None:
        # 选择合适的间隔显示通道名称，避免拥挤
        step = max(1, n_channels // 20)
        y_ticks = np.arange(0, n_channels, step)
        y_labels = [f'Ch{i+1}' for i in y_ticks]
        plt.yticks(y_ticks, y_labels)
    
    plt.tight_layout()
    
    if save_path:
        heatmap_path = save_path.replace('.png', '_heatmap.png')
        plt.savefig(heatmap_path, dpi=300, bbox_inches='tight')
    
    plt.show()

# 主函数
def main():
    # 示例EEG信号
    file_path = 'E:/Code/medicine-care/EegFunc/chb01/chb01_03.edf'
    data, sampling_rate, channel_names = read_eeg_data(file_path)
    
    # 设置窗口参数
    window_size = int(6 * sampling_rate)  # 6秒
    step_size = int(3 * sampling_rate)    # 3秒
    
    # 创建输出目录
    output_dir = create_output_directory('E:/Code/medicine-care/EegFunc/zero_crossings_result')
    
    # 提取所有通道的零交叉特征
    features = extract_zero_crossings_features(data, window_size, step_size)
    
    # 保存特征
    np.save(os.path.join(output_dir, 'zero_crossings_features.npy'), features)
    
    # 创建特征DataFrame
    feature_df = pd.DataFrame()
    for i in range(features.shape[0]):
        channel_name = channel_names[i] if i < len(channel_names) else f'Channel_{i+1}'
        feature_df[f'{channel_name}_ZeroCrossings'] = features[i]
    
    # 保存为CSV
    feature_df.to_csv(os.path.join(output_dir, 'zero_crossings_features.csv'), index=False)
    
    # 可视化结果
    visualize_zero_crossings(
        features, 
        channel_names=channel_names, 
        save_path=os.path.join(output_dir, 'zero_crossings_visualization.png')
    )
    
    # 添加额外的统计分析可视化
    plt.figure(figsize=(12, 6))
    
    # 计算每个通道的平均零交叉次数
    mean_crossings = np.mean(features, axis=1)
    
    # 创建条形图
    channel_indices = np.arange(len(mean_crossings))
    plt.bar(channel_indices, mean_crossings, alpha=0.7)
    
    # 设置图表标题和标签
    plt.title('各通道平均零交叉次数', fontsize=14)
    plt.xlabel('通道索引', fontsize=12)
    plt.ylabel('平均零交叉次数', fontsize=12)
    
    # 设置x轴刻度
    if len(channel_indices) > 20:
        plt.xticks(np.arange(0, len(channel_indices), 5))
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'zero_crossings_average.png'), dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"零交叉特征已保存到 {output_dir}")
    print(f"可视化结果已保存到 {output_dir} 目录下的PNG文件中")

if __name__ == "__main__":
    main()