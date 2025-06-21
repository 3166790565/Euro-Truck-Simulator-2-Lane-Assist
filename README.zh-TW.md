> [!WARNING]  
> **ETS2LA V2 仍在開發中！** 請預期會遇到錯誤、功能不完善和崩潰的情況。
> 查看[此視頻](https://www.youtube.com/watch?v=EgZp05tA5ks)預覽當前功能。

![](ETS2LA/Assets/markdown_logo.png)


# ETS2LA V2.0
ETS2LA 是一個旨在為 SCS Software 的卡車模擬遊戲帶來自動駕駛技術的項目。本頁面包含一些信息，但如果您想閱讀所有文檔，請前往[我們的網站](https://ets2la.com)！

<img alt="GitHub commits" src="https://img.shields.io/github/commit-activity/m/ETS2LA/Euro-Truck-Simulator-2-Lane-Assist/main?style=for-the-badge&logo=Github">
<img alt="Discord" src="https://img.shields.io/discord/1120719484982939790?style=for-the-badge&logo=discord">


### 重要鏈接
- [下載](https://ets2la.com/guides/installation/installer/) - 關於如何下載和安裝當前版本的說明。
- [網站](https://ets2la.com) - 閱讀文檔並訪問您的賬戶。
- [Discord](https://ets2la.com/discord) - 加入我們的社區，與開發者交流並獲取支持。
- [Ko-Fi](https://ko-fi.com/tumppi066) - **在 Ko-Fi 上支持我們，幫助我們維持項目的發展。**

### 我遇到了程序問題
請查看[常見問題解答](https://ets2la.com/faq)獲取答案。如果您的問題未在其中列出，請加入 [Discord](https://ets2la.com/discord) 並在支持頻道中提問。如果某個問題變得常見，我們會將答案添加到常見問題解答中！

### 如何提供幫助
我們特別尋找有 **Python** 和/或 **Unity** 經驗的人。該項目完全開源，因此您可以創建自己的分支，然後在完成後將您的更改合併到主應用程序中。下面有我們的倉庫列表，方便訪問。

如果您沒有開發背景，您仍然可以提供幫助！我們所有的翻譯都由社區完成，為此我們在[網站上提供了說明](https://ets2la.com/guides/translation/manual/)，介紹如何進行翻譯。這相當簡單，任何具有基本文本編輯理解的人都應該能夠完成。

### 我們的倉庫
> [!NOTE]
> 大多數開發團隊成員更喜歡使用 **GitHub** 而非 **GitLab**。然而，由於世界各地的網絡情況不同，我們必須在 **GitLab** 上託管一些數據，以使其對全球各地的每個人都可訪問。

**主要倉庫**
- [ETS2LA](https://github.com/ETS2LA/Euro-Truck-Simulator-2-Lane-Assist) - 主倉庫，您當前所在的位置。包含運行一切的後端。
- [Visualization](https://github.com/ETS2LA/visualization) - 包含周圍環境 3D 可視化的 Unity 項目。
- [Frontend](https://github.com/ETS2LA/frontend) - 主應用程序 UI。包含用戶交互的所有內容。
- [Cloud](https://github.com/ETS2LA/cloud) - 此倉庫包含 ETS2LA 服務的後端。

**額外的 ETS2LA 相關倉庫**
- [Documentation](https://github.com/ETS2LA/documentation) - 這是存儲和渲染主要文檔的地方。
- [Translations](https://github.com/ETS2LA/translations) - 主要翻譯倉庫。這是存儲和獲取所有翻譯的地方。
- [Installer](https://github.com/ETS2LA/installer) - 這是 ETS2LA 安裝程序的主要倉庫。
- [CDN](https://github.com/ETS2LA/cdn) - 用於向網絡受限環境中的用戶提供一些文件。
- [Bot](https://github.com/ETS2LA/bot) - ETS2LA discord 服務器機器人。處理一些 ETS2LA 相關命令和管理。

**GitLab 託管的倉庫**
- [ETS2LA](https://gitlab.com/ETS2LA/ets2la) - 主倉庫，GitHub 上倉庫的鏡像。
- [Data](https://gitlab.com/ETS2LA/data) - 包含從遊戲中提取的 ETS2LA 地圖數據。這些數據包含所有道路和預製定義以及我們的自定義偏移。
- [ETS2LA Plugin](https://gitlab.com/ETS2LA/ets2la_plugin) - ETS2 和 ATS 的 ETS2LA 插件。包含從遊戲中提取各種重要信息並將其發送到後端的代碼。

### 為什麼要開發 ETS2LA？
> 好吧，我不是想用我對這個程序的絕對興奮來刷屏，因為我已經告訴過你們我有多喜歡它，但我認為有必要再重複一次，我坐輪椅，沒有手動靈活性來獨自玩這個遊戲，而且正是因為這個程序，我才能夠玩這個遊戲！我非常喜歡它，我真的希望開發者知道我感謝他們為製作這個程序所做的所有辛勤工作。當我因為殘疾而無法在現實世界中駕駛時，能夠在模擬器中駕駛帶來了一種滿足感。🙂
> - **匿名用戶** - ETS2LA Discord