# 介紹及參考資料

## 專案介紹
```{card}
使用爬蟲至104人力銀行爬取相關職缺的學歷、工作描述、相關技能等資料。並且將把取下來的文字利用中研院的斷詞套件進行斷詞及詞性標註。並且使用停斷詞將不必要的詞刪除。最後使用 `apyori`、`pyvis` 兩個套件進行關聯性分析以及視覺化。
```
## 使用套件


1. [ckiplab/ckip-transformers](https://github.com/ckiplab/ckip-transformers)
1. [apyori](https://github.com/ymoch/apyori)
1. [pyvis](https://pyvis.readthedocs.io/en/latest/tutorial.html)

## 參考資料
1. [Getting Started with Apriori Algorithm in Python](https://www.section.io/engineering-education/apriori-algorithm-in-python/)
1. [Tutorial - pyvis 0.1.3.1 documentation](https://pyvis.readthedocs.io/en/latest/tutorial.html)



## 輸出結果
````{card} <i class="fas fa-play-circle icon"></i>&nbsp; Output

<iframe width='100%' height='750px '
    style="border:none"
    src='../Plot_Apriori__S_0.100_C_0.700.html'></iframe>

````