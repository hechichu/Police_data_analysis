import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定一个包含所需字符的中文字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号'-'显示为方块的问题

# 读取CSV文件
file_path = 'cleaned_penalty_data.csv'
data = pd.read_csv(file_path, encoding='utf-8')

# 1. 提取并统计“处罚结果”中的信息
# 假设“处罚结果”列中包含“罚款”、“拘留”等关键词
data['罚款'] = data['处罚结果'].str.contains('罚款').fillna(False)
data['拘留'] = data['处罚结果'].str.contains('拘留').fillna(False)

# 统计被行政拘留的总人数，被罚款的总人数，被同时拘留和罚款的总人数
total_detained = data['拘留'].sum()
total_fined = data['罚款'].sum()
total_both = (data['罚款'] & data['拘留']).sum()

print(f"被行政拘留的总人数: {total_detained}")
print(f"被罚款的总人数: {total_fined}")
print(f"被同时拘留和罚款的总人数: {total_both}")

# 2. 处理“处罚日期”列，按年度和月度统计处罚人数
data['处罚日期'] = pd.to_datetime(data['处罚日期'], errors='coerce')

# 按年度统计
data['年份'] = data['处罚日期'].dt.year
annual_counts = data['年份'].value_counts().sort_index()

# 按月度统计
data['月份'] = data['处罚日期'].dt.to_period('M')
monthly_counts = data['月份'].value_counts().sort_index()

print(f"每年的处罚人数:\n{annual_counts}")
print(f"每月的处罚人数:\n{monthly_counts}")

# 3. 计算罚款金额和拘留日期的统计数据
data['罚款金额'] = data['处罚结果'].str.extract(r'罚款(\d+)元').astype(float)

# 计算罚款金额总和
total_fine_amount = data['罚款金额'].sum()

# 计算拘留日期的均值和方差
detained_dates = data[data['拘留']]['处罚日期']
mean_detained_date = detained_dates.mean()
std_detained_date = detained_dates.std()

print(f"总罚款金额: {total_fine_amount}")
print(f"拘留日期均值: {mean_detained_date}")
print(f"拘留日期方差: {std_detained_date}")

# 4. 统计频数分布
# 犯罪人数随月份变化
monthly_crime_counts = data.groupby('月份').size()

# 可视化分析
plt.figure(figsize=(14, 12))

# 被行政拘留的总人数，被罚款的总人数，被同时拘留和罚款的总人数
plt.subplot(3, 2, 1)
categories = ['拘留', '罚款', '同时拘留和罚款']
counts = [total_detained, total_fined, total_both]
sns.barplot(x=categories, y=counts)
plt.title('处罚类型统计')
plt.ylabel('人数')

# 每年的处罚人数
plt.subplot(3, 2, 2)
annual_counts.plot(kind='bar')
plt.title('每年的处罚人数')
plt.xlabel('年份')
plt.ylabel('人数')

# 每月的处罚人数
plt.subplot(3, 2, 3)
monthly_counts.plot(kind='bar')
plt.title('每月的处罚人数')
plt.xlabel('月份')
plt.ylabel('人数')

# 总罚款金额
plt.subplot(3, 2, 4)
sns.histplot(data['罚款金额'].dropna(), bins=20)
plt.title('罚款金额分布')
plt.xlabel('金额（元）')
plt.ylabel('频数')

# 犯罪人数随月份变化
plt.subplot(3, 1, 3)
monthly_crime_counts.plot(kind='line', marker='o')
plt.title('犯罪人数随月份变化')
plt.xlabel('月份')
plt.ylabel('犯罪人数')

plt.tight_layout()
plt.show()
