import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 1. 讀取資料 (類似 PHP 的 fgetcsv，但 Pandas 直接轉成強大的表格物件 DataFrame)
print("正在載入工業感測器資料...")
df = pd.read_csv("ai4i2020.csv")

# 2. 特徵挑選 (篩選出會影響機器故障的感測器數據欄位)
# 我們選用：空氣溫度、製程溫度、轉速、扭力、工具磨損量
feature_cols = ['Air temperature [K]', 'Process temperature [K]', 'Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]']
X = df[feature_cols] 
y = df['Machine failure'] # 目標：預測機器是否故障 (0為正常，1為故障)

# 3. 切割資料集 (80% 用來訓練 AI，20% 留著考試驗證)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. 初始化隨機森林模型 (傳統機器學習王者，在你的 2015 MBA 上跑只要 1 秒)
print("AI 模型訓練中...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. 驗證準確度
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(print(f"--- 第一天任務完成 ---"))
print(f"隨機森林模型訓練完成！測試集準確度 (Accuracy): {accuracy * 100:.2f}%")
