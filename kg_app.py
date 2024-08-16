import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 设置页面的基本样式
st.markdown("""
    <style>
    body {
        font-family: 'Roboto', sans-serif;
        background-color: #f5f5f5;
    }
    .main {
        background-color: #ffffff;
        padding: 10px;  /* 减少内边距，默认是20px */
        border-radius: 8px;
        max-width: 100%; /* 确保主容器最大宽度 */
    }
    h1, h2, h3 {
        color: #333;
    }
    .stButton button {
        background-color: #2b7fb8;
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
        font-size: 16px;
    }
    .stButton button:hover {
        background-color: #f8af23;
        color: white;
    }
    .chart {
        margin-bottom: 40px;
    }
    </style>
""", unsafe_allow_html=True)

# 显示大标题并置中
st.markdown("<h1 style='text-align: center; margin-bottom: 10px;'>第一屆康健增重大賽🍰</h1>", unsafe_allow_html=True)

# 在右上角添加超链接，并进行美化
st.markdown(
    """
    <div style="text-align: right; padding: 20px;">
        <a href="https://docs.google.com/spreadsheets/d/1AOjn9rvcHUeusWOmQ5xLspPa9thchQu4BCLtO-rDqz8/edit?gid=0#gid=0" target="_blank" 
        style="text-decoration: none; font-size: 18px; color: #2b7fb8; font-weight: bold; background-color: #e0f7fa; padding: 10px; border-radius: 10px;">
            體重紀錄表 📊
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

# 从 Streamlit Secrets 中获取 Google Sheets API 凭证
creds_dict = st.secrets["GCP_SERVICE_ACCOUNT"]

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(creds_dict, scopes=scope)

client = gspread.authorize(creds)

# 使用 sheet_id 打開 Google Sheet
spreadsheet = client.open_by_key("1AOjn9rvcHUeusWOmQ5xLspPa9thchQu4BCLtO-rDqz8")  # 替換成你的 sheet_id
sheet = spreadsheet.sheet1  # 選擇第一個工作表
data = sheet.get_all_records()

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
perry_df = kg_longer_df[kg_longer_df['Name'] == 'Perry']
alan_df = kg_longer_df[kg_longer_df['Name'] == 'Alan']


# 选手一 Steven
col1, col2 = st.columns([2, 5], gap="large")  # 适当调整 gap 以平衡左右间距
with col1:
    st.markdown("""
        <style>
        .steven-container {
            display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: center;
        }
        .steven-title {
            margin-right: 10px;
            font-size: 20px;
            font-weight: bold;
            text-align: right;
        }
        </style>
        <div class="steven-container">
            <div class="steven-title">選手一 Steven</div>
        </div>
    """, unsafe_allow_html=True)
    st.image("Steven.PNG", use_column_width=True)
with col2:
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    ax1.plot(steven_df['Date'], steven_df['Weight'], color='#2b7fb8', label='Steven')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Weight (kg)')
    ax1.set_title('Steven Weight')
    
    # 正确设置 y 轴的范围和刻度
    ax1.set_ylim(51.2, 54.4)
    ax1.set_yticks([51.3, 51.8, 52.3, 52.8, 53.3, 53.8, 54.3])

    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    fig1.autofmt_xdate()
    st.pyplot(fig1)


# 选手二 Grace
col1, col2 = st.columns([2, 5], gap="large")  # 适当调整 gap 以平衡左右间距
with col1:
    st.markdown("""
        <style>
        .grace-container {
            display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: center;
        }
        .grace-title {
            margin-right: 10px;
            font-size: 20px;
            font-weight: bold;
            text-align: right;
        }
        </style>
        <div class="grace-container">
            <div class="grace-title">選手二 Grace</div>
        </div>
    """, unsafe_allow_html=True)
    st.image("Yoz.PNG", use_column_width=True)
with col2:
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    ax2.plot(grace_df['Date'], grace_df['Weight'], color='#f8af23', label='Grace')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Weight (kg)')
    ax2.set_title('Grace Weight')
    
    # 正确设置 y 轴的范围和刻度
    ax2.set_ylim(43.7, 46.9)
    ax2.set_yticks([43.8, 44.3, 44.8, 45.3, 45.8, 46.3, 46.8])

    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    fig2.autofmt_xdate()
    st.pyplot(fig2)

# 选手三 Perry
col1, col2 = st.columns([2, 5], gap="large")  # 适当调整 gap 以平衡左右间距
with col1:
    st.markdown("""
        <style>
        .perry-container {
            display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: center;
        }
        .perry-title {
            margin-right: 10px;
            font-size: 20px;
            font-weight: bold;
            text-align: right;
        }
        </style>
        <div class="perry-container">
            <div class="perry-title">選手三 Perry</div>
        </div>
    """, unsafe_allow_html=True)
    st.image("Perry.PNG", use_column_width=True)
with col2:
    fig3, ax3 = plt.subplots(figsize=(8, 4))
    ax3.plot(perry_df['Date'], perry_df['Weight'], color='#f8af23', label='Perry')
    ax3.set_xlabel('Date')
    ax3.set_ylabel('Weight (kg)')
    ax3.set_title('Perry Weight')
    
    # 正确设置 y 轴的范围和刻度
    ax3.set_ylim(43.7, 46.9)
    ax3.set_yticks([43.8, 44.3, 44.8, 45.3, 45.8, 46.3, 46.8])

    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    fig3.autofmt_xdate()
    st.pyplot(fig3)

# 見證人 Alan
col1, col2 = st.columns([2, 5], gap="large")  # 适当调整 gap 以平衡左右间距
with col1:
    st.markdown("""
        <style>
        .alan-container {
            display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: center;
        }
        .alan-title {
            margin-right: 10px;
            font-size: 20px;
            font-weight: bold;
            text-align: right;
        }
        </style>
        <div class="alan-container">
            <div class="alan-title">見證人 Alan</div>
        </div>
    """, unsafe_allow_html=True)
    st.image("Alan.PNG", use_column_width=True)
with col2:
    fig4, ax4 = plt.subplots(figsize=(8, 4))
    ax4.plot(alan_df['Date'], alan_df['Weight'], color='#53592dff', label='Alan')
    ax4.set_xlabel('Date')
    ax4.set_ylabel('Weight (kg)')
    ax4.set_title('Alan Weight')
    
    # 正确设置 y 轴的范围和刻度
    ax4.set_ylim(70.3, 72.7)
    ax4.set_yticks([70.6, 71.1, 71.6, 72.1, 72.6, 73.1, 72.6])

    ax4.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    fig4.autofmt_xdate()
    st.pyplot(fig4)

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
st.markdown(f"<h2 style='text-align: center; color: #2b7fb8;'>目前領先者 🥇{leading_participant}</h2>", unsafe_allow_html=True)
