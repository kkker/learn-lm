import joblib

# 載入原本的 pkl
model = joblib.load("predictive_maintenance_model.pkl")

# 轉換為 ONNX 格式 (必須指定輸入的特徵數量，我們有 5 個特徵)
import numpy as np
from skl2onnx import to_onnx
from skl2onnx.common.data_types import FloatTensorType
# onx = to_onnx(model, X_train.astype(np.float32))
# 告訴 ONNX：未來的輸入資料規格是 [任意列數(None), 5個特徵欄位] 且型態為 Float
initial_type = [('float_input', FloatTensorType([None, 5]))]
# 直接轉換，完全不需要 X_train
onx = to_onnx(model, initial_types=initial_type)

with open("predictive_maintenance_model.onnx", "wb") as f:
    f.write(onx.SerializeToString())
