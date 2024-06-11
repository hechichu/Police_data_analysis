import pandas as pd

# 读取CSV文件
file_path = 'penalty_data.csv'
data = pd.read_csv(file_path, encoding='utf-8')

# 去除重复数据
data.drop_duplicates(inplace=True)

# 处理缺失值
# 假设处罚事由、处罚依据、处罚结果、行政执法单位名称不允许为空，若为空则填充为“未知”
data.fillna({
    '处罚事由': '未知',
    '处罚依据': '未知',
    '处罚结果': '未知',
    '行政执法单位名称': '未知',
    '处罚日期': '1970/01/01'  # 假设处罚日期如果缺失，填充为一个默认值
}, inplace=True)


# 保存清洗后的数据
cleaned_file_path = 'cleaned_data/cleaned_penalty_data.csv'
data.to_csv(cleaned_file_path, index=False, encoding='utf-8')

print("数据预处理和清洗完成。")
