# Django 案件管理系統

## 📌 專案介紹
本系統為一個內部使用的 **案件管理系統**，提供 **案件搜尋、篩選、排序、管理** 等功能，幫助不同部門同步對應的案件編號，解決跨部門案件號碼對不上的問題。

## ✨ 主要功能
- **🔍 案件查詢**：
  - 支援 **`case_number` / `department` / `circuit_diagram` / `model_type` / `business_case_number` / `software_version` / `status`** 搜尋。
  - **關鍵字模糊匹配**（如：搜尋 "K42"，可找到 "TH-010-K42" 案件）。
  - **顯示匹配原因** 並標記紅色，例如："客戶編號：K42"。
- **📊 案件篩選**：
  - **部門篩選**
  - **狀態篩選**
  - **開始與結束日期篩選**
- **📌 案件管理**：
  - **新增、編輯案件**
  - **案件歷史紀錄追蹤**（顯示案件修改紀錄）
- **📅 排序功能**：
  - 可選擇 **按建立日期排序（最新 / 最舊優先）**
  - 保留使用者選擇的排序方式
- **🔑 使用者管理**：
  - **登入 / 登出**
  - **使用者可自行註冊帳號**

## 🛠️ 環境設定
### 1️⃣ 安裝必要套件
確保已安裝 Python 及 Django，然後執行：
```sh
pip install -r requirements.txt
```

### 2️⃣ 資料庫遷移
```sh
python manage.py makemigrations
python manage.py migrate
```

### 3️⃣ 建立超級管理員
```sh
python manage.py createsuperuser
```
依照提示輸入帳號、密碼。

### 4️⃣ 啟動伺服器
```sh
python manage.py runserver
```
瀏覽 `http://127.0.0.1:8000/` 來使用系統。

## 📂 專案結構
```
case_management/
│── case_management/         # Django 主專案目錄
│── case_tracker/            # 案件管理 App
│   ├── migrations/          # Django 資料庫遷移檔案
│   ├── templates/           # HTML 模板
│   │   ├── base.html        # 網站主要框架
│   │   ├── case_list.html   # 案件列表頁面
│   │   ├── case_detail.html # 案件詳情頁面
│   │   ├── register.html    # 註冊頁面
│   │   ├── login.html       # 登入頁面
│   ├── static/              # 靜態資源（CSS, JS）
│   ├── views.py             # 處理請求與邏輯
│   ├── models.py            # 定義資料庫模型
│   ├── urls.py              # 路由設定
│   ├── forms.py             # 表單處理
│── db.sqlite3               # SQLite 資料庫（可換成 MySQL/PostgreSQL）
│── manage.py                # Django 管理指令
│── requirements.txt         # 依賴套件列表
```

## 🚀 未來計畫
- **📊 使用 Docker 部署到伺服器**
- **📂 附件管理**（支援案件附檔上傳）
- **👥 權限管理**（修改/新增/查看案件，支援設置不同權限）
