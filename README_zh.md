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
# 1. 计算 Dijkstra 最优路径与风险级联传导
python3 scripts/graph_engines/temporal_graph_engine.py

# 2. 运行 10,000 次蒙特卡洛随机模拟与 95% 在险价值 (VaR)
python3 scripts/simulation_engines/monte_carlo_decision_engine.py

# 3. 计算偏导敏感度弹性与龙卷风波动图 (Tornado Diagram)
python3 scripts/decision_analysis/graph_sensitivity_engine.py
python3 scripts/decision_analysis/tornado_diagram_engine.py

# 4. 求解博弈论多利益相关者冲突死锁
python3 scripts/decision_analysis/game_theory_stakeholder_solver.py
```

### 第 5 步：翻译为人类直观摘要与周度行动清单
将复杂的运筹学指标自动翻译为直观的执行摘要，并生成带截止日期的周度 To-Do 清单：
```bash
python3 scripts/ui_translators/human_translator.py
python3 scripts/ui_translators/action_checklist_generator.py
```

---

## 📦 Anthropic Skill 标准兼容

本仓库 100% 符合 Anthropic 官方 **Agent Skill 规范与 Anthropic Skill 标准**：

- **`SKILL.md` 清单文件**：根目录与 Skill 子目录均包含带有规范 YAML Frontmatter (`name`, `description`) 的主指令文件。
- **标准模块化目录结构**：分门别类地组织 `scripts/`、`resources/`、`references/` 与 `examples/`。
- **零额外运行开销**：基于 Python 标准库实现，支持无缝导入。

---

## 🌟 系统哲学与隐喻

LifeTree (人生树) 是新一代 **个人决策智能 (PDI) 操作系统 (Life OS)**。它将公共政策网络、宏观经济趋势、法定法规与个人人生选择融入动态树状决策架构中，具备实时风险对冲、代码驱动随机预测与博弈论冲突求解能力。

---

## 💻 快速开始与引擎运行

### 运行端到端 MVP 决策流程闭环
```bash
python3 scripts/run_mvp_workflow.py
```

---

## 📈 Star History 趋势图

[![Star History Chart](https://api.star-history.com/svg?repos=CaryK753/LifeTree-Skills&type=Date)](https://star-history.com/#CaryK753/LifeTree-Skills&Date)

---

## 📄 开源协议

本项目采用 **MIT 开源协议** - 详见 [LICENSE](LICENSE) 文件。
