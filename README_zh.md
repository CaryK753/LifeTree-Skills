# LifeTree (人生树) — 个人决策智能操作系统 (Life OS)

<p align="center">
  <img src="lifetree-brand/assets/brand-hero.jpg" alt="LifeTree Brand Cover" width="100%" style="border-radius: 12px;" />
</p>

<p align="center">
  <strong>基于以对象为中心的时序 GraphRAG 与代码驱动蒙特卡洛模拟的个人决策操作系统</strong>
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

## 📖 目录

- [🤖 AI Agent 使用此 Skill 指导说明](#-ai-agent-使用此-skill-指导说明)
- [🎨 交互式 HTML 决策仪表盘与动态图谱查看器](#-交互式-html-决策仪表盘与动态图谱查看器)
- [📦 Anthropic Skill 标准兼容](#-anthropic-skill-标准兼容)
- [🌟 系统哲学与隐喻](#-系统哲学与隐喻)
- [🏗️ 架构与技术栈](#️-架构与技术栈)
- [🚀 核心创新点](#-核心创新点)
- [📁 项目与 Skill 目录结构](#-项目与-skill-目录结构)
- [💻 快速开始与引擎运行](#-快速开始与引擎运行)
- [📈 Star History 趋势图](#-star-history-趋势图)
- [📄 开源协议](#-开源协议)

---

## 🤖 AI Agent 使用此 Skill 指导说明

当 AI Agent 被分配用于解决复杂的个人高风险决策（如全球身份规划、资产配置、职业转型、跨国避税）时，**必须严格遵循以下 5 步操作规程**：

### 第 1 步：读取 Skill 指令
首先阅读 `SKILL.md`，理解领域规则、本地 SQLite 数据库 Schema 以及 Python 计算引擎位置。

### 第 2 步：检索嵌入式本地 SQLite 数据库
在向用户重复询问之前，先通过 FTS5 全文检索本地已有的知识图谱节点：
```bash
python3 scripts/graph_engines/sqlite_graph_store.py "blocked account"
```

### 第 3 步：运行 Agent 联网检索与即时 GraphRAG 合成
使用 Tavily / 博查 搜索工具获取最新的法定政策法规，并将事实合成入本体图谱：
```bash
python3 scripts/data_connectors/search_connector_tavily.py "Germany chanceskarte statutory deposit 2026"
python3 scripts/data_connectors/jit_connector_synthesizer.py
```

### 第 4 步：执行代码驱动数学计算引擎（强制规程）
> [!IMPORTANT]
> **严禁大模型通过文本生成盲估数学指标**：
> 必须显式运行 `scripts/` 中的 Python 脚本来计算最短路径、蒙特卡洛模拟、龙卷风敏感度图与 VaR 资金限额：
```bash
python3 scripts/graph_engines/temporal_graph_engine.py
python3 scripts/simulation_engines/monte_carlo_decision_engine.py
python3 scripts/decision_analysis/graph_sensitivity_engine.py
python3 scripts/decision_analysis/tornado_diagram_engine.py
python3 scripts/decision_analysis/game_theory_stakeholder_solver.py
```

### 第 5 步：生成交互式 HTML 决策仪表盘与动态图谱查看器
自动生成单文件自包含的高保真 HTML 可视化决策产物：
```bash
# 1. 生成交互式 HTML 决策仪表盘
python3 scripts/ui_translators/html_report_generator.py

# 2. 生成动态 Vis.js 知识图谱查看器
python3 scripts/graph_engines/graph_visualizer_html.py
```

---

## 🎨 交互式 HTML 决策仪表盘与动态图谱查看器

LifeTree 自动导出单文件自包含的可视化 HTML 产物：

1. **交互式 HTML 决策仪表盘 (`lifetree_decision_report.html`)**：
   - 核心决策指标卡片（P50 目标时缓、95% VaR 资金限额、后悔最小化得分）。
   - 带 Checkbox 复选框的周度待办 Task 清单。
   - Chart.js 动态蒙特卡洛置信度分布图表。
2. **动态 Vis.js 知识图谱查看器 (`lifetree_graph_viewer.html`)**：
   - 力导向物理拓扑网络，支持节点拖拽、平移与缩放。
   - 区分实体颜色的 Badge（`PERSON`、`REGULATION_LAW`、`PATHWAY_ROUTE`、`CAPITAL_ASSET` 等）。
   - 侧滑式 **节点 Inspector 检查器**，点击任意节点展示详细属性、置信度与数据源 provenance。
   - 支持实时模糊搜索与按实体类型筛选。

---

## 💻 快速开始与引擎运行

### 运行端到端 MVP 决策流程闭环（自动生成 HTML 产物）
```bash
python3 .agent/skills/lifetree/scripts/run_mvp_workflow.py
```

---

## 📈 Star History 趋势图

[![Star History Chart](https://api.star-history.com/svg?repos=CaryK753/LifeTree-Skills&type=Date)](https://star-history.com/#CaryK753/LifeTree-Skills&Date)

---

## 📄 开源协议

本项目采用 **MIT 开源协议** - 详见 [LICENSE](LICENSE) 文件。
