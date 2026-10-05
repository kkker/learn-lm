import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

print("========= 🚀 工業預防性維護 AI 專案啟動 =========")

# 1. 讀取資料 (類似讀取 SQL Table)
df = pd.read_csv("ai4i2020.csv")
print(f"成功載入資料！總筆數: {len(df)} 筆")

# 檢查資料有多不平衡 (計算 Machine failure 欄位中 0 與 1 的數量)
print("\n[資料分布檢查]")
print(df['Machine failure'].value_counts()) 
# 你會看到 0 (正常) 有 9000 多筆，1 (故障) 只有 339 筆

# 2. 定義特徵 (X) 與 標籤 (y)
# X 是一張只包含感測器數值的表；y 是我們要預測的答案（0或1）
feature_cols = ['Air temperature [K]', 'Process temperature [K]', 'Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]']
X = df[feature_cols]
y = df['Machine failure']

# 3. 切割資料集 (80% 訓練，20% 測試)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. 初始化並訓練模型
# 關鍵：加入 class_weight='balanced'！這會讓 AI 自動加重對那 3% 故障樣本的學習
print("\nAI 模型訓練中 (已啟用工業資料平衡優化)...")
## n_estimators = 100: 建立 100 棵決策樹來投票
## class_weight = 'balanced' : 這個參數會告訴 AI：「看到 1 個故障樣本的損失，要等同於看到 30 個正常樣本」，強迫 AI 不能忽視少數群體。
# None（預設）：各類別權重一樣。適用於資料分布均勻的場景（例如：正常 50%、故障 50%）。
# 自訂字典，如 {0: 1, 1: 10}：適用於「漏報成本極高」的場景。比如智慧醫療中，漏看一個癌症患者的後果無法承受。你可以手動把故障（1）的權重拉得比 'balanced' 更高，寧可錯殺一百（偽陽性高），也不能漏抓一個。
## random_state = 42（亂數種子）
# 為什麼填 42：在程式語言中，亂數切割資料或初始化權重時，如果每次執行的結果都不同，你就無法評估程式碼到底是改好還是改壞。填入 42（工程師界致敬《銀河便車指南》的經典數字梗），只是為了固定亂數軌跡。
model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
model.fit(X_train, y_train)

# 5. 模型預測與評估
y_pred = model.predict(X_test)

# 印出混淆矩陣 (Confusion Matrix)
print("\n[評估結果 1] 混淆矩陣 (Confusion Matrix):")
cm = confusion_matrix(y_test, y_pred)
print(cm)
# 解讀矩陣：
# [ [真實正常且猜正常, 真實正常但猜故障],
#   [真實故障但猜正常, 真實故障且猜故障] ]

# 印出詳細報告 (看重 F1-Score)
print("\n[評估結果 2] 分類詳細報告 (Classification Report):")
print(classification_report(y_test, y_pred))

# 6. 驗證準確度
accuracy = accuracy_score(y_test, y_pred)
print(f"隨機森林模型訓練完成！測試集準確度 (Accuracy): {accuracy * 100:.2f}%")

print("==================================================")

# 7. 導出 AI 模型檔案 需要時，啟用這區塊
# import joblib
#
# # 將訓練好的隨機森林模型與特徵名稱打包存檔
# joblib.dump(model, "predictive_maintenance_model.pkl")
# print("【成功】AI 模型已成功打包為 predictive_maintenance_model.pkl！")
