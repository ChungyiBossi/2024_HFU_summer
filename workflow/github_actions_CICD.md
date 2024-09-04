### Goal
利用github actions, 學習持續整合/持續開發，也可以方便你做單元測試以利提早找出bug

### 步驟
1. 到你的git repository，新增一個workflow
2. 選擇你的Actions 範本，[參考](https://github.com/marketplace?type=actions)
3. 細部範本調整內容，以及觸發的方式(通常是特定branch被push的時候會觸發。)
4. 設定你會用到的secret & api key，可以設定在repository的環境變數內，方便單元測試使用
5. 串接不同的step，確保你可以在不同的作業系統下運行。
6. (optional) 透過actions主動部屬到 GCP / Azure / AWS 等等的雲端平台服務。
7. (optional) 設定smoke test，在部屬到雲端完畢之後確保服務正常被運形。