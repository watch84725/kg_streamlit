import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 設定頁面的基本樣式
st.markdown("""
    <style>
    body {
        font-family: 'Roboto', sans-serif;
        background-color: #f5f5f5;
    }
    .main {
        background-color: #ffffff;
        padding: 10px;  /* 減少內邊距，默認是20px */
        border-radius: 8px;
        max-width: 100%; /* 確保主容器最大寬度 */
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

# 顯示大標題並置中
st.markdown("<h1 style='text-align: center; margin-bottom: 10px;'>第一屆康健增重大賽🍰</h1>", unsafe_allow_html=True)

# 在右上角添加超連結，並進行美化
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

# 從 Streamlit Secrets 中獲取 Google Sheets API 憑證
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

# 將所有的日期列轉換為數值類型，避免字串類型影響計算
date_columns = df.columns[1:]  # 除了 "Name" 列之外的所有日期列
df[date_columns] = df[date_columns].apply(pd.to_numeric, errors='coerce')

# 將數據從寬表轉換為長表（key-value 格式）
kg_longer_df = df.melt(id_vars=["Name"], var_name="Date", value_name="Weight")
kg_longer_df = kg_longer_df[kg_longer_df['Date'] != '基準體重']

# 清理數據：去除空字串，確保所有列的數據類型正確
kg_longer_df['Date'] = pd.to_datetime(kg_longer_df['Date'], format="%m/%d", errors='coerce')
kg_longer_df['Weight'] = pd.to_numeric(kg_longer_df['Weight'], errors='coerce')

# 刪除因轉換錯誤產生的 NaN 值
kg_longer_df = kg_longer_df.dropna(subset=['Date', 'Weight'])

# 針對特定選手進行數據過濾
grace_df = kg_longer_df[kg_longer_df['Name'] == 'Grace']
steven_df = kg_longer_df[kg_longer_df['Name'] == 'Steven']
perry_df = kg_longer_df[kg_longer_df['Name'] == 'Perry']
alan_df = kg_longer_df[kg_longer_df['Name'] == 'Alan']

# 顯示選手一 Steven 的數據圖表
col1, col2 = st.columns([2, 5], gap="large")
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
    
    # 正確設置 y 軸的範圍和刻度
    ax1.set_ylim(51.2, 54.4)
    ax1.set_yticks([51.3, 51.8, 52.3, 52.8, 53.3, 53.8, 54.3])

    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    fig1.autofmt_xdate()
    st.pyplot(fig1)

# 顯示選手二 Grace 的數據圖表
col1, col2 = st.columns([2, 5], gap="large")
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
    
    # 正確設置 y 軸的範圍和刻度
    ax2.set_ylim(43.5, 46.7)
    ax2.set_yticks([43.6, 44.1, 44.6, 45.1, 45.6, 46.1, 46.6])

    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    fig2.autofmt_xdate()
    st.pyplot(fig2)

# 顯示選手三 Perry 的數據圖表
col1, col2 = st.columns([2, 5], gap="large")
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
    ax3.plot(perry_df['Date'], perry_df['Weight'], color='#a4586aff', label='Perry')
    ax3.set_xlabel('Date')
    ax3.set_ylabel('Weight (kg)')
    ax3.set_title('Perry Weight')
    
    # 正確設置 y 軸的範圍和刻度
    ax3.set_ylim(46.7, 50.5)
    ax3.set_yticks([46.8, 47.3, 47.8, 48.3, 48.8, 49.3, 49.8])

    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    fig3.autofmt_xdate()
    st.pyplot(fig3)

# 顯示見證人 Alan 的數據圖表
col1, col2 = st.columns([2, 5], gap="large")
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
    
    # 正確設置 y 軸的範圍和刻度
    ax4.set_ylim(70.3, 73.7)
    ax4.set_yticks([70.6, 71.1, 71.6, 72.1, 72.6, 73.1, 73.6])

    ax4.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    fig4.autofmt_xdate()
    st.pyplot(fig4)

# 計算 Grace 和 Steven 與 07/31 的體重變化
base_date = '07/31'  # 基準日期
base_weights = df[base_date]  # 07/31 的體重
# 創建一個新的 DataFrame，計算每一天與 07/31 相比的體重變化
df_change = df.copy()
for col in date_columns:
    df_change[col] = df[col] - base_weights

# 將數據從寬表轉換為長表（key-value 格式）
kg_change_longer_df = df_change.melt(id_vars=["Name"], var_name="Date", value_name="WeightChange")

# 清理數據：將日期轉換為 datetime 格式，去除無效數據
kg_change_longer_df['Date'] = pd.to_datetime(kg_change_longer_df['Date'], format="%m/%d", errors='coerce')

# 刪除 NaN 值
kg_change_longer_df = kg_change_longer_df.dropna(subset=['Date', 'WeightChange'])

# 只保留 Grace 和 Steven 的數據
kg_change_longer_df_filtered = kg_change_longer_df[kg_change_longer_df['Name'].isin(['Grace', 'Steven', 'Perry'])]
kg_change_longer_df_Alan = kg_change_longer_df[kg_change_longer_df['Name'].isin(['Alan'])]
# # 計算 Perry 與 08/16 的體重變化
# Perry_base_date = '8/16'  # 基準日期
# Perry_base_weights = df[Perry_base_date]  # 08/16 的體重
# # 創建一個新的 DataFrame，計算每一天與 08/16 相比的體重變化
# Perry_df_change = df.copy()
# for col in date_columns:
#     Perry_df_change[col] = df[col] - Perry_base_weights
# # 將數據從寬表轉換為長表（key-value 格式）
# Perry_kg_change_longer_df = Perry_df_change.melt(id_vars=["Name"], var_name="Date", value_name="WeightChange")
# # 清理數據：將日期轉換為 datetime 格式，去除無效數據
# Perry_kg_change_longer_df['Date'] = pd.to_datetime(Perry_kg_change_longer_df['Date'], format="%m/%d", errors='coerce')
# # 刪除 NaN 值
# Perry_kg_change_longer_df = Perry_kg_change_longer_df.dropna(subset=['Date', 'WeightChange'])
# # 只保留 Perry 的數據
# Perry_kg_change_longer_df_filtered = Perry_kg_change_longer_df[Perry_kg_change_longer_df['Name'].isin(['Perry'])]

# # 使用 concat 將兩個 DataFrame 進行 union
# result = pd.concat([kg_change_longer_df_filtered, Perry_kg_change_longer_df_filtered])

# # 重新設置索引（可選），如果你不需要原索引值，可以用 ignore_index=True
# result.reset_index(drop=True, inplace=True)

# 找到最新的日期
latest_date = kg_change_longer_df_filtered['Date'].max()

# 過濾出最新日期的數據
latest_data = kg_change_longer_df_filtered[kg_change_longer_df_filtered['Date'] == latest_date]
# 判斷誰增重更多
leading_participant = latest_data.loc[latest_data['WeightChange'].idxmax(), 'Name']

# 設置全局字體大小
plt.rcParams.update({'font.size': 14})  # 修改全局字體大小

# 插入數據表格
st.dataframe(df)

# 第二個圖：體重變化折線圖
fig2, ax2 = plt.subplots(figsize=(12, 6))

ax2.plot(kg_change_longer_df_filtered[kg_change_longer_df_filtered['Name'] == 'Steven']['Date'], 
         kg_change_longer_df_filtered[kg_change_longer_df_filtered['Name'] == 'Steven']['WeightChange'], color='#2b7fb8', label='Steven')

ax2.plot(kg_change_longer_df_filtered[kg_change_longer_df_filtered['Name'] == 'Grace']['Date'], 
         kg_change_longer_df_filtered[kg_change_longer_df_filtered['Name'] == 'Grace']['WeightChange'], color='#f8af23', label='Grace')

ax2.plot(kg_change_longer_df_filtered[kg_change_longer_df_filtered['Name'] == 'Perry']['Date'], 
         kg_change_longer_df_filtered[kg_change_longer_df_filtered['Name'] == 'Perry']['WeightChange'], color='#a4586aff', label='Perry')

ax2.plot(kg_change_longer_df_Alan[kg_change_longer_df_Alan['Name'] == 'Alan']['Date'], 
         kg_change_longer_df_Alan[kg_change_longer_df_Alan['Name'] == 'Alan']['WeightChange'], color='#53592dff', label='Alan')

ax2.set_xlabel('Date', fontsize=14)
ax2.set_ylabel('Weight Change (kg)', fontsize=14)
ax2.set_title('Weight Leaderboard', fontsize=16)
ax2.legend(title='Name', loc='upper left')  # Move the legend to the upper left corner

# 設置日期格式為 MM/DD
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))

# 自動調整日期標籤，以避免重疊
fig2.autofmt_xdate()

# 在 Streamlit 中顯示新圖表
st.pyplot(fig2)

# 顯示當前領先者
st.markdown(f"<h2 style='text-align: center; color: #2b7fb8;'>目前領先者 🥇{leading_participant}</h2>", unsafe_allow_html=True)
