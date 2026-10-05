# 測試 Docker 內的 AI 套件是否安裝成功
try:
    import pandas as pd
    import sklearn
    import flask
    print("【成功】所有 AI 開發套件（Pandas, Scikit-learn, Flask）均已正確載入！")
    print(f"Pandas 版本: {pd.__version__}")
    print(f"Scikit-learn 版本: {sklearn.__version__}")
except ImportError as e:
    print(f"【失敗】有套件未正確安裝，錯誤訊息: {e}")
