import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 显示大标题并置中
st.markdown("<h1 style='text-align: center;'>第一屆康健增重大賽🍰</h1>", unsafe_allow_html=True)

# 从 Streamlit Secrets 中获取 Google Sheets API 凭证
creds_dict = st.secrets["GCP_SERVICE_ACCOUNT"]

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(creds_dict, scopes=scope)

client = gspread.authorize(creds)

# 使用 sheet_id 打開 Google Sheet
spreadsheet = client.open_by_key("1AOjn9rvcHUeusWOmQ5xLspPa9thchQu4BCLtO-rDqz8")  # 替換成你的 sheet_id
sheet = spreadsheet.sheet1  # 選擇第一個工作表
data = sheet.get_all_records()

# 添加图片和标题
col1, col2 = st.columns([1, 1])  # 创建两列布局
with col1:
    st.markdown("<h3 style='text-align: center;'>選手一 Steven</h3>", unsafe_allow_html=True)
    st.image("Steven.PNG", width=300)  # 使用相对路径
with col2:
    st.markdown("<h3 style='text-align: center;'>選手二 Grace</h3>", unsafe_allow_html=True)
    st.image("Yoz.PNG", width=300)  # 使用相对路径

# 將數據轉換為 DataFrame
df = pd.DataFrame(data)

# 将所有的日期列转换为数值类型，避免字符串类型影响计算
date_columns = df.columns[1:]  # 除了 "Name" 列之外的所有日期列
df[date_columns] = df[date_columns].apply(pd.to_numeric, errors='coerce')

# 原始数据的处理
# 将数据从宽表转换为长表（key-value 格式）
kg_longer_df = df.melt(id_vars=["Name"], var_name="Date", value_name="Weight")
kg_longer_df = kg_longer_df[kg_longer_df['Date'] != '基準體重']

# 清理数据：去除空字符串，确保所有列的数据类型正确
kg_longer_df['Date'] = pd.to_datetime(kg_longer_df['Date'], format="%m/%d", errors='coerce')
kg_longer_df['Weight'] = pd.to_numeric(kg_longer_df['Weight'], errors='coerce')

# 删除因转换错误产生的 NaN 值
kg_longer_df = kg_longer_df.dropna(subset=['Date', 'Weight'])

# 过滤出 Grace 和 Steven 的数据
grace_df = kg_longer_df[kg_longer_df['Name'] == 'Grace']
steven_df = kg_longer_df[kg_longer_df['Name'] == 'Steven']

# 新的 DataFrame：与 07/31 比较的体重增减
base_date = '07/31'  # 基准日期
base_weights = df[base_date]  # 07/31 的体重

# 创建一个新的 DataFrame，计算每一天与 07/31 相比的体重增减
df_change = df.copy()
for col in date_columns:
    df_change[col] = df[col] - base_weights

# 将数据从宽表转换为长表（key-value 格式）
kg_change_longer_df = df_change.melt(id_vars=["Name"], var_name="Date", value_name="WeightChange")

# 清理数据：将日期转换为 datetime 格式，去除无效数据
kg_change_longer_df['Date'] = pd.to_datetime(kg_change_longer_df['Date'], format="%m/%d", errors='coerce')

# 删除 NaN 值
kg_change_longer_df = kg_change_longer_df.dropna(subset=['Date', 'WeightChange'])

# 只保留 Grace 和 Steven 的数据
kg_change_longer_df_filtered = kg_change_longer_df[kg_change_longer_df['Name'].isin(['Grace', 'Steven'])]

# 找到最新的日期
latest_date = kg_change_longer_df_filtered['Date'].max()

# 过滤出最新日期的数据
latest_data = kg_change_longer_df_filtered[kg_change_longer_df_filtered['Date'] == latest_date]

# 判断谁增重更多
leading_participant = latest_data.loc[latest_data['WeightChange'].idxmax(), 'Name']

# 设置全局字体大小
plt.rcParams.update({'font.size': 14})  # 修改全局字体大小

# 创建双轴图和体重变化图，确保两个图表大小一致
fig, ax1 = plt.subplots(figsize=(12, 6))

# 绘制第一个图：双轴图
ax1.set_xlabel('Date', fontsize=14)  # 设置X轴标签字体大小
ax1.set_ylabel('Steven Weight (kg)', color='#2b7fb8', fontsize=14)  # 使用提供的色码 #2b7fb8
ax1.plot(steven_df['Date'], steven_df['Weight'], color='#2b7fb8', label='Steven', linewidth=2.5)  # 设置线条宽度
ax1.tick_params(axis='y', labelcolor='#2b7fb8', labelsize=12)  # 设置Y轴刻度字体大小
ax1.tick_params(axis='x', labelsize=12)  # 设置X轴刻度字体大小

# 设置左边 Y 轴范围和刻度间隔
ax1.set_ylim(51.3, 54.3)
ax1.set_yticks([i / 10 for i in range(513, 544, 5)])  # 设置刻度间隔为0.5

# 创建第二个 Y 轴，共享 X 轴，并设置线条宽度
ax1_right = ax1.twinx()
ax1_right.set_ylabel('Grace Weight (kg)', color='#f8af23', fontsize=14)  # 使用提供的色码 #f8af23
ax1_right.plot(grace_df['Date'], grace_df['Weight'], color='#f8af23', label='Grace', linewidth=2.5)  # 设置线条宽度
ax1_right.tick_params(axis='y', labelcolor='#f8af23', labelsize=12)  # 设置第二个Y轴刻度字体大小

# 设置右边 Y 轴范围和刻度间隔
ax1_right.set_ylim(43.8, 46.8)
ax1_right.set_yticks([i / 10 for i in range(438, 469, 5)])  # 设置刻度间隔为0.5

# 设置日期格式为 MM/DD
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))

# 设置图表标题
ax1.set_title('Steven vs Grace Weight Visualization', fontsize=16)  # 设置标题字体大小

# 在 Streamlit 中显示图表
st.pyplot(fig)

# 插入数据表格
st.dataframe(df)

# 第二个图：体重变化折线图
fig2, ax2 = plt.subplots(figsize=(12, 6))

ax2.plot(kg_change_longer_df_filtered[kg_change_longer_df_filtered['Name'] == 'Steven']['Date'], 
         kg_change_longer_df_filtered[kg_change_longer_df_filtered['Name'] == 'Steven']['WeightChange'], 
         marker='o', color='#2b7fb8', label='Steven')

ax2.plot(kg_change_longer_df_filtered[kg_change_longer_df_filtered['Name'] == 'Grace']['Date'], 
         kg_change_longer_df_filtered[kg_change_longer_df_filtered['Name'] == 'Grace']['WeightChange'], 
         marker='o', color='#f8af23', label='Grace')

ax2.set_xlabel('Date', fontsize=14)
ax2.set_ylabel('Weight Change (kg)', fontsize=14)
ax2.set_title('Weight Leaderboard', fontsize=16)
ax2.legend(title='Name')

# 设置日期格式为 MM/DD
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))

# 自动调整日期标签，以避免重叠
fig2.autofmt_xdate()

# 在 Streamlit 中显示新图表
st.pyplot(fig2)

# 显示当前领先者
st.markdown(f"<h2 style='text-align: center;'>目前領先者 🥇{leading_participant}</h2>", unsafe_allow_html=True)
