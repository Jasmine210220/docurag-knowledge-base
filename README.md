# PDF 智能知识库

一个本地知识库项目，当前阶段完成了基础工程结构、配置加载和程序入口，后续将逐步补全文档加载、文本切分、向量索引、检索和问答能力。

## 当前进度

当前已完成：

- 项目目录初始化
- Python 包结构初始化
- 环境变量配置加载
- 程序入口建立
- 数据目录自动检查和创建

当前未完成：

- PDF 和其他文档格式的加载
- 文本切分
- 向量化与索引
- 检索
- 问答生成

## 目录结构

```text
.
├── data/
│   ├── raw/
│   └── vector_store/
├── docs/
│   └── project-notes.md
├── src/
│   └── kb_rag/
│       ├── config.py
│       ├── main.py
│       └── __init__.py
├── tests/
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## 目录说明

- `data/raw/`
  - 存放原始文档，例如 PDF、TXT、Markdown、CSV、JSON
- `data/vector_store/`
  - 存放向量索引和相关中间产物
- `docs/project-notes.md`
  - 记录当前项目结构、模块职责和实现说明
- `src/kb_rag/config.py`
  - 负责环境变量加载和基础路径定义
- `src/kb_rag/main.py`
  - 负责程序入口、配置读取和目录检查
- `tests/`
  - 预留测试目录

## 配置说明

项目通过 `.env` 加载运行配置，示例模板如下：

```env
OPENAI_API_KEY=your_api_key_here
EMBEDDING_MODEL=text-embedding-3-small
CHAT_MODEL=gpt-4.1-mini
```

当前配置项作用如下：

- `OPENAI_API_KEY`
  - OpenAI 接口密钥
- `EMBEDDING_MODEL`
  - 向量化模型名称
- `CHAT_MODEL`
  - 问答模型名称

`.env.example` 用于提供模板，`.env` 不应提交到仓库。

## 安装与运行

### 1. 创建虚拟环境

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. 安装依赖

```powershell
pip install -r requirements.txt
```

### 3. 创建配置文件

根据 `.env.example` 创建 `.env` 文件，并填写实际配置。

### 4. 运行入口程序

```powershell
python -m src.kb_rag.main
```

当前入口程序会执行以下操作：

- 加载环境变量
- 检查 `data/raw` 和 `data/vector_store` 目录
- 输出当前配置和初始化状态

## 当前代码说明

### `src/kb_rag/config.py`

负责：

- 定义项目根目录
- 定义数据目录、原始文档目录、向量目录
- 加载 `.env` 配置
- 生成 `Settings` 配置对象

### `src/kb_rag/main.py`

负责：

- 调用配置加载函数
- 确保目录存在
- 输出当前初始化信息

## Git 忽略规则

当前 `.gitignore` 已排除以下内容：

- `.venv/`
- `__pycache__/`
- `.env`
- `data/raw/` 中的真实文档
- `data/vector_store/` 中的索引和缓存文件

仓库中仅保留目录占位文件 `.gitkeep`，用于保留目录结构。

## 后续计划

后续预计按以下顺序补充模块：

1. 文档加载
2. 文本切分
3. 向量化与索引
4. 检索
5. 问答生成
6. 交互接口
