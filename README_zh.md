# LifeTree (人生树) — 个人决策智能操作系统 (Life OS)

<p align="center">
  <img src="lifetree-brand/assets/brand-hero.jpg" alt="LifeTree Brand Cover" width="100%" style="border-radius: 12px;" />
</p>

<p align="center">
  <strong>底层硬核决策科学数学引擎 + 表层极简人类语言 UI 翻译</strong>
</p>

<p align="center">
  <a href="README.md"><strong>English</strong></a> | 
  <a href="README_zh.md"><strong>简体中文</strong></a> | 
  <a href="README_de.md"><strong>Deutsch</strong></a>
</p>

<p align="center">
  <a href="#-anthropic-skill-标准兼容"><img src="https://img.shields.io/badge/Anthropic--Skill-Standard--Compliant-brightgreen.svg?style=for-the-badge&logo=anthropic" alt="Anthropic Skill Standard" /></a>
  <a href="#-架构与技术栈"><img src="https://img.shields.io/badge/Database-SQLite%20FTS5-green.svg?style=for-the-badge&logo=sqlite" alt="SQLite FTS5" /></a>
  <a href="#-核心创新点"><img src="https://img.shields.io/badge/GraphRAG-Temporal%20Ontology-purple.svg?style=for-the-badge" alt="Temporal GraphRAG" /></a>
  <a href="#-开源协议"><img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge" alt="License MIT" /></a>
</p>

---

> [!CAUTION]
> **重要风险提示与免责声明**：
> 所有仿真结论、事件概率、VaR/CVaR 风险指标与效用得分高度依赖于人为输入的权重、主观效用参数与法定/市场历史概率；模型仅作为**定量决策辅助与情景推演工具**，**不构成任何金融、法律、税务、医疗或移民正式建议，亦无法替代最终的人为判断**。

---

## 🌟 设计哲学：底层硬核数学引擎 + 表层极简人类语言

LifeTree 的核心设计原则为：**“算法与数学模型可以尽可能抽象复杂，但展示给用户的 UI 和文档绝不堆砌学术名词，始终使用最直观、最易懂的人类语言呈现。”**

| 内部底层数学模型 (Code Engine) | 转换后的表层人类 UI 语言 (Plain Human Language) |
| :--- | :--- |
| **CVaR 95% Expected Shortfall** | **🛡️ 最坏情况资金保障线 (极端黑天鹅安全兜底)** |
| **Kahneman-Tversky CPT Score** | **🧠 心理真实满意度 (考虑防避亏损偏好)** |
| **AHP Principal Eigenvector (CR<0.10)**| **⚖️ 决策偏好一致性 (完美匹配个人优先级)** |
| **Bayesian Posterior $P(H \mid E)$** | **🔮 最新证据胜算/信心度 (结合最新情报更新)** |
| **2x2 Nash Equilibrium** | **🤝 多方博弈双赢平衡方案 (协调各方诉求)** |
| **Influence Diagram Semantics** | **📊 决策要素拆解 (厘清“我能掌控的”与“外部环境”)** |

---

## 🧠 决策科学模型库 (`./scripts/decision_models/`)

LifeTree 为高风险个人决策场景（职业转型、资产配置、身份规划、跨国避税）集成了专门解耦的决策科学模型库：

| 模块 | 脚本路径 | 核心算法与数学原理 |
| :--- | :--- | :--- |
| **MAUT 多属性效用** | `maut_utility_engine.py` | 6 维标准化效用标定与 AHP 层次分析法特征向量权重抽取 ($\mathbf{A}w = \lambda_{\max} w$) |
| **CVaR 尾部风险** | `cvar_risk_engine.py` | 95% 在险价值 (VaR) 与 95% 条件风险价值 ($\text{CVaR}_{0.95}$ / 期望短缺 $ES_{0.95}$) 极端破产警示 |
| **影响图 Semantic 建模** | `influence_diagram_layer.py` | 决策节点 ($\square$)、机会节点 ($\bigcirc$)、价值节点 ($\diamondsuit$) 拓扑标注与因果干预链路区分 |
| **贝叶斯信念更新** | `bayesian_belief_updater.py` | 动态后验概率更新 $P(H \mid E) = \frac{P(E \mid H)P(H)}{P(E)}$ 与 Dempster-Shafer 区间概率 bounds |
| **跨期效用贴现** | `intertemporal_discounting_engine.py` | 指数贴现 $V e^{-rt}$ 与行为双曲线贴现 $U(t) = \frac{V}{1 + kt}$ 修正远期回报偏差 |
| **最优停止求解器** | `optimal_stopping_solver.py` | 37% 法则 / Snell Envelope 最佳出手时机阈值计算 $k^* = \lfloor n / e \rfloor$ |
| **Copula 风险联动** | `copula_correlation_engine.py` | 二元高斯 Copula 系统性联动矩阵（宏观下行 $\rightarrow$ 薪资下跌 + 资产缩水） |
| **前景理论 (Prospect Theory)**| `prospect_theory_engine.py` | Kahneman-Tversky 损失厌恶价值函数 $v(x)$ ($\lambda = 2.25$) 与概率权重 $w(p)$ |

---

## 💻 快速开始与引擎运行

### 1. 运行端到端 MVP 决策流程闭环（自动生成 HTML 产物）
```bash
python3 .agent/skills/lifetree/scripts/run_mvp_workflow.py
```

### 2. 运行全量自动化单元测试集与性能基准
```bash
python3 .agent/skills/lifetree/tests/run_all_tests.py
python3 .agent/skills/lifetree/tests/benchmark_performance.py --quick
```

---

## 📄 开源协议

本项目采用 **MIT 开源协议** - 详见 [LICENSE](LICENSE) 文件。
