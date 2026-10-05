<?php
// 模擬從產線（或前端網頁表單）取得的即時感測器數據
$sensor_data = [
    'air_temp'     => 298.1, // 空氣溫度 (K)
    'process_temp' => 308.6, // 製程溫度 (K)
    'rpm'          => 2800,  // 轉速超高 (容易發生功率或散熱故障)
    'torque'       => 55.0,  // 扭力 (Nm)
    'tool_wear'    => 210    // 刀具已磨損 210 分鐘 (接近臨界值)
];

// Python Flask API 在 Docker 內的網址 (因為在同個容器，可用 localhost)
$url = 'http://localhost:5000/predict';

$ch = curl_init($url);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($sensor_data));
curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type:application/json'));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$response = curl_exec($ch);
curl_close($ch);

// 解析 AI 回傳的 JSON 結果
$result = json_decode($response, true);

echo "========= 🏭 工業產線 AI 預測系統 (PHP 端) =========\n";
if ($result && $result['status'] === 'success') {
    echo "AI 預測結果代碼: " . $result['machine_failure'] . "\n";
    echo "系統提示訊息: " . $result['message'] . "\n";
} else {
    echo "系統錯誤: 無法連線至 AI 預測模組。\n";
}
echo "====================================================\n";
