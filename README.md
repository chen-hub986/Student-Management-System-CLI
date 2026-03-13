# 🎓 Intelligent Student Management System
> 一個基於 Python 開發、具備企業級架構思維的終端機學生管理系統。

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![Architecture](https://img.shields.io/badge/Architecture-Repository%20Pattern-success)
![Design Pattern](https://img.shields.io/badge/Design_Pattern-Singleton%20|%20Decorator-orange)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)

## 📝 專案簡介
本專案跳脫傳統高中的結構化腳本寫法，完全採用 **強型別 (Type Hints)** 與 **物件導向設計 (OOP)** 進行開發。系統實現了 UI 介面與核心業務邏輯的徹底解耦，導入自訂例外處理、裝飾器攔截、介面隔離與自動化日誌追蹤，具備極高的穩定性與軟體工程水準。

### 🎯 專題動機
我在學習 Python 的過程中，發現許多入門作品停留在「功能能跑就好」的階段，較少思考後續維護、錯誤處理與擴充性。
因此我把這個題目當成一次完整軟體開發練習：

* 從「單檔腳本」進化成「可分層、可測試、可擴充」的專案。
* 練習把真實情境（學生成績管理）轉成可維護的程式架構。
* 培養面對錯誤輸入與資料一致性時的工程思維。

### ✨ 核心技術亮點

#### 🛡️ 防禦性編程與嚴格封裝 (Defensive Programming)
* **實體保護**：在 `Student` 資料實體中運用 `@property` 與 `@scores.setter` 攔截異常輸入（包含型別驗證與 0-100 邊界檢查），實現「永遠有效的實體」。
* **自訂例外系統**：精準定義 `StudentNotFoundException`, `DuplicateStudentException` 等領域錯誤，使業務邏輯語意極度清晰。

#### ⚙️ 全局錯誤攔截與單例日誌 (AOP & Singleton)
* **裝飾器攔截**：實作 `@MenuErrorHandler` 類別型裝飾器，完美攔截底層業務邏輯拋出的例外，保護主程式不崩潰，實現物件導向的面向切面編程 (AOP)。
* **單例日誌 (Singleton Logger)**：透過覆寫 `__new__` 確保 Logger 實例全域唯一。內建 `RotatingFileHandler` 自動輪轉機制，分離 `activity.log` 與 `errors.log`，避免記憶體與硬碟溢位。

#### 🗄️ 儲存庫模式與介面隔離 (Repository Pattern & ABC)
* **依賴反轉**：透過 `BaseRepository` 抽象基底類別 (ABC) 定義持久化介面，`StudentManager` 僅依賴抽象而不依賴實作。
* **無縫存取**：實作 `StudentRepository`，並支援 `utf-8-sig` 編碼的 CSV 匯出，完美解決 Windows Excel 開啟亂碼問題。

#### 🚀 現代化語法與高階函數應用
* **字典分派 (Dictionary Dispatch)**：徹底消滅臃腫的 `if-else` 選單，提升系統查找效能與可擴充性。
* **函數式編程 (Functional Programming)**：大量結合 `lambda`, `filter`, `sorted`, `zip` 等高階函數處理多維度資料排序、優等生查詢與班級統計。

---

## 🏗️ 系統架構目錄

專案嚴格遵守「關注點分離 (Separation of Concerns)」原則：

```text
📦 python-30days (Intelligent-Student-Manager)
 ┣ 📂 history/         # 專案演進軌跡 (保留 v1 到 v6 的迭代重構歷史)
 ┣ 📂 src/             # 核心原始碼
 ┃ ┣ 📜 base_repository.py # 資料儲存庫介面 (ABC)
 ┃ ┣ 📜 repository.py      # JSON/CSV 資料持久化實作
 ┃ ┣ 📜 student.py         # 核心資料實體與封裝
 ┃ ┣ 📜 manager.py         # 業務邏輯中樞 (CRUD, 統計, 排序)
 ┃ ┣ 📜 exceptions.py      # 自訂例外類別
 ┃ ┣ 📜 decorators.py      # 錯誤攔截裝飾器
 ┃ ┗ 📜 logger.py          # 單例模式日誌系統
 ┣ 📜 main.py          # 系統進入點與互動式 CLI
 ┗ 📜 README.md        # 專案說明書
```

## 💻 CLI 範例輸入 / 輸出

以下示範實際操作流程，讓審查者可以快速理解系統互動方式。

### 範例 A：新增學生並查看排序

```text
選擇操作：
1. 添加學生資料
2. 排序成績排名選單
...
請輸入選項（1-8）：1

請輸入學生姓名（或輸入 'q' 結束）：Alice
請輸入學生的成績（用逗號分隔）：90, 85, 95

請輸入學生姓名（或輸入 'q' 結束）：q

選擇操作：
請輸入選項（1-8）：2
請選擇:
1. 依平均成績排序 (高 -> 低)
...
```

### 範例 B：錯誤輸入驗證

```text
請輸入學生的成績（用逗號分隔）：100, abc, 90
成績輸入無效，請確保成績是數字並用逗號分隔。
```

> 備註：錯誤會由 `MenuErrorHandler` 與自訂例外統一處理，避免程式中斷。

## 🚀 未來規劃（大學延伸方向）

升上大學後，我會以這個專案作為基礎，持續往以下方向深化：

* **資料結構與演算法落地**：優化搜尋、排序與統計流程，並比較時間複雜度。
* **資料庫化**：由 JSON 擴充到 SQLite / PostgreSQL，練習正規化與查詢效能。
* **Web 化與 API 化**：以 FastAPI 或 Flask 製作前後端分離版本。
* **自動化測試與 CI**：補上整合測試、GitHub Actions，自動驗證每次提交。
* **使用者體驗提升**：加入更完整的輸入提示、資料匯入與報表可視化。
