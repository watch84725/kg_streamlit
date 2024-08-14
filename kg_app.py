import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import os
from dotenv import load_dotenv


# Google Sheets API 授權
load_dotenv()

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file(os.environ.get("GOOGLE_CREDENTIALS_JSON"), scopes=scope)

client = gspread.authorize(creds)

# # 使用 sheet_id 打開 Google Sheet
spreadsheet = client.open_by_key("1AOjn9rvcHUeusWOmQ5xLspPa9thchQu4BCLtO-rDqz8")  # 替換成你的 sheet_id
sheet = spreadsheet.sheet1  # 選擇第一個工作表
data = sheet.get_all_records()

# # # 將數據轉換為 DataFrame
df = pd.DataFrame(data)
print(df)

# 将数据从宽表转换为长表（key-value 格式）
df_melted = df.melt(id_vars=["Name"], var_name="Date", value_name="Weight")

# 强制将 Weight 列转换为数值类型，无法转换的将设置为 NaN
df_melted["Weight"] = pd.to_numeric(df_melted["Weight"], errors='coerce')

# 排除 Weight 为 NaN 的行
df_melted = df_melted.dropna(subset=["Weight"])

# 顯示轉置後的結果
print(df_melted)

st.title("Weight Data Visualization")

# 顯示轉置並排除空值後的數據
st.subheader("Transposed Key-Value Data (Without Empty Weights)")
st.dataframe(df_melted)

# 根據需要進行視覺化
st.line_chart(df_melted.pivot(index='Date', columns='Name', values='Weight'))
