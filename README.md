# People Stats Kit · 人力量化工具箱

**把统计学方法直接接到招聘漏斗、人才触达 AB、Offer 周期和评分校准上——开实验前算样本量，跑完后看 p 值与置信区间，分数能不能信看校准图。**


> **Copyright © 2026 张文婧 (Anna Zhang)** · [MIT License](./LICENSE) · [github.com/annawzhang](https://github.com/annawzhang)  
> 欢迎学习与面试查阅；保留版权与许可声明。**禁止删除作者信息后冒充本人作品二次发表。** 公开内容为虚构/脱敏演示数据。


[在线报告](https://annawzhang.github.io/people-stats-kit/) · 纯 Python 标准库，无第三方依赖

> 全部为虚构场景数据；口径对齐已公开的 [explainable-talent-scoring](https://github.com/annawzhang/explainable-talent-scoring) 与 [hiring-copilot](https://github.com/annawzhang/hiring-copilot)。

## 解决什么问题

| 人力场景 | 方法 | 本仓库模块 |
|---|---|---|
| 分层跟进 vs 标准跟进，回复率有没有真差异 | 双比例 z 检验 | `proportion.two_proportion_z` |
| 开跑前要多少线索才够功效 | 样本量估算 | `proportion.sample_size_two_prop` |
| 漏斗某一步掉得「看起来很多」 | Wilson 置信区间 | `funnel.funnel_rates` |
| Offer 拖多久、一半人何时入职 | Kaplan–Meier | `survival.kaplan_meier` |
| 初筛高分是否真更容易过现场面 | 分箱校准 + Brier | `calibration.calibration_bins` |

## 报告里能看到什么（seed=42）

- 触达 AB：44.4% → 52.9%，相对提升约 19%，p &lt; 0.01  
- 若要把回复率从 44% 做到 52%，每组约需 **612** 人  
- 招聘漏斗各步带 95% Wilson CI  
- 投递→入职中位周期约 **34 天**（含删失）  
- 初筛 ≥60 分档现场面通过率高于 0–39 分档  

## 本地运行

```bash
python3 -m unittest discover -s tests -v   # 9 tests
python3 run.py                             # → docs/index.html
```

| 路径 | 作用 |
|---|---|
| `peoplestats/` | 比例检验、漏斗 CI、生存分析、校准、场景合成 |
| `tests/` | 单元测试 |
| `docs/index.html` | Pages 报告 |

## 背景

作者本硕为统计学 / 金融数学，实习中做过人才评分 AB 与招聘漏斗分析。本仓库是将这些方法抽成可运行工具箱的公开版，**不包含任何公司真实数据**。
