from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import onnxruntime as ort

app = Flask(__name__)

# 1. 改用微軟 ONNX Runtime 載入模型 (替代 joblib)
print("正在載入 ONNX 高速推論大腦...")
onnx_path = "predictive_maintenance_model.onnx"
session = ort.InferenceSession(onnx_path)

# 取得 ONNX 模型要求的輸入節點名稱 (通常預設叫 'float_input' 或 'input')
input_name = session.get_inputs()[0].name

# 2. 定義嚴格的欄位映射與順序 (保護產線數據不對調)
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
        
        # 3. 依據 FEATURE_MAPPING 的 Key 順序動態建立二維陣列
        # ONNX 引擎不吃 DataFrame，它最喜歡二進位的 NumPy Array
        raw_features = []
        for csv_col, json_key in FEATURE_MAPPING.items():
            raw_features.append(float(data[json_key]))
            
        # 將資料包裝成二維矩陣，並強制指定型態為 np.float32 (必須符合 ONNX 轉檔時的宣告)
        input_data = np.array([raw_features], dtype=np.float32)
        
        # 4. 進行 ONNX 預測
        # session.run 會吐出一個包含多個輸出的 List，我們取第一個輸出 [0]
        # 隨機森林模型會吐出兩個東西：[預測標籤, 各類別機率]
        onnx_outputs = session.run(None, {input_name: input_data})
        
        # 5. 取得預測標籤結果 (0 或 1)
        # 結構為數組，我們使用 .item() 或 [0] 將其轉為 Python 原生純量 int
        prediction = onnx_outputs[0]
        final_pred = int(prediction[0])
        
        # 6. 回傳標準 JSON 結果
        return jsonify({
            'status': 'success',
            'machine_failure': final_pred,
            'message': '警告：偵測到潛在故障！請停機檢查。' if final_pred == 1 else '機器運行狀態正常。'
        })
        
    except Exception as e:
        print(f"【ONNX API 內部出錯】: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
