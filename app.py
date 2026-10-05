from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

# 載入模型
model = joblib.load("predictive_maintenance_model.pkl")

# 定義嚴格的欄位映射與順序
FEATURE_MAPPING = {
    'Air temperature [K]': 'air_temp',
    'Process temperature [K]': 'process_temp',
    'Rotational speed [rpm]': 'rpm',
    'Torque [Nm]': 'torque',
    'Tool wear [min]': 'tool_wear'
}

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        # 1. 依據 FEATURE_MAPPING 的「鍵（Key）」順序動態建立字典，保證欄位順序 100% 正確
        ordered_data = {}
        for csv_col, json_key in FEATURE_MAPPING.items():
            ordered_data[csv_col] = float(data[json_key])
            
        # 2. 轉換為 DataFrame
        input_data = pd.DataFrame([ordered_data])
        
        # 3. 進行 AI 預測
        prediction = model.predict(input_data)
        
        # 4. 關鍵修正：使用 .item() 或是 [0] 將多維陣列轉換為 Python 原生純量 int
        final_pred = int(prediction[0])
        
        return jsonify({
            'status': 'success',
            'machine_failure': final_pred,
            'message': '警告：偵測到潛在故障！請停機檢查。' if final_pred == 1 else '機器運行狀態正常。'
        })
        
    except Exception as e:
        # 除錯用：如果還是出錯，會把錯誤詳細訊息印在 API 終端機上
        print(f"【API 內部出錯】: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
