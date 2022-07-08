# 模組使用說明

## 104人力銀行爬蟲
```python
from helper import Job104

MUST_INCLUDE = ['數據分析', '商業分析', 'BA', '分析', '研究', 'AI', '資料', '演算法', 'DS']

job104 = Job104(KEYWORD='金融&數據分析', MAX_PAGES=1, MUST_INCLUDE=MUST_INCLUDE)
list_JobData = []

for info in job104.Crawler():
    print(info)

```

```{card} 回傳結果

    {'Title': ['***研究部', '研究助理', '金融與總經', '***銀行'],
    'Company': ['中***股份有限公司'],
    'County': '台北市',
    'Salary': ['待遇面議', '4 萬元'],
    'Category': ['金融研究員 ', '券商後線人員 '],
    'JobDescription': '*** is looking for research associates **********',
    'Experience': ['不拘'],
    'Education': ['大學', '碩士'],
    'Major': ['商業及管理學科類'],
    'Language': ['英文', '--', '聽', '/精通', '說', '/精通'],
    'Skills': ['不拘'],
    'Others': '****************************************************',
    'Url': 'https://www.104.com.tw/job/*****?jobsource=jolist_b_relevance'}

```

## apriori&視覺化模組

```{card} 輸入格式
    [
        ['個股', '團隊', '法說會'],
        ['簡報', '模型', '行銷'],
        ['自由', '趨勢', '自動化'],
        ['專題', '認真', '應徵'],
        ['SAS', '團隊', '業務'],
        ['看法', '趨勢', '模型'],
        ['時間', '技能', '團隊'],
        ['收益', 'PowerPoint', '簡報'],
        ['行政', '整理', '資料'],
        ['探勘', '團隊', '社群'],
        ['自由', '系統', '交割'],
        ['跨業', '交流', '活潑'],
        ['業務', '控管', '實務'],
        ['自由', 'Kubernetes', 'IDE'],
        ['應用', '團隊', '協力'],
    ]
```

```python
from helper import EZApriori

ezapriori = EZApriori(TRANSACTION=list_Job104MergedData)
ezapriori.fit(SUPPORT=0.1, CONFIDENCE=0.7)
```