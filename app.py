from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

# 1. 載入剛剛打包的模型
model = joblib.load("predictive_maintenance_model.pkl")
feature_cols = ['Air temperature [K]', 'Process temperature [K]', 'Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]']

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # 2. 接收從 PHP 傳過來的 JSON 資料
        data = request.get_json()
        
        # 3. 轉換為 Pandas DataFrame (模型需要這種結構)
        input_data = pd.DataFrame([{
            'Air temperature [K]': float(data['air_temp']),
            'Process temperature [K]': float(data['process_temp']),
            'Rotational speed [rpm]': float(data['rpm']),
            'Torque [Nm]': float(data['torque']),
            'Tool wear [min]': float(data['tool_wear'])
        }])
        
        # 4. 進行 AI 預測 (0 或 1)
        prediction = model.predict(input_data)[0]
        
        # 5. 回傳 JSON 結果給 PHP
        return jsonify({
            'status': 'success',
            'machine_failure': int(prediction), # 0為正常，1為故障
            'message': '警告：偵測到潛在故障！請停機檢查。' if prediction == 1 else '機器運行狀態正常。'
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

if __name__ == '__main__':
    # 監聽 0.0.0.0 讓 Docker 外部或內部 Nginx 可以呼叫
    app.run(host='0.0.0.0', port=5000)
