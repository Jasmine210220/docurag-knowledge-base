# DocuRAG：多格式文档知识库问答系统

这是一个本地 RAG 项目。当前已经完成：

- 工程化项目结构
- `src` 布局包配置
- 环境变量配置加载
- 多格式文档加载
- 文本切分
- 向量化与索引
- 检索模块
- 最小问答链组装
- 最小 CLI 交互入口
- 手工验证脚本
- 最小自动化测试

当前还未完成：

- 问答效果优化
- 更完整的交互产品形态（如 Web / GUI）

## 当前技术路线

- 文档加载：LangChain 常见 loader 生态
- 文本切分：`RecursiveCharacterTextSplitter`
- Embedding：`DashScopeEmbeddings`
- 向量库：`Chroma`
- 检索：基于 Chroma 的相似度检索
- 问答链：LangChain 经典 retrieval chain
- 配置加载：`python-dotenv`
- JSON 依赖：`jq`

## 当前目录结构

```text
.
|-- data/
|   |-- raw/
|   |-- test_samples/
|   |-- test_vector_store/
|   `-- vector_store/
|-- docs/
|   `-- project-notes.md
|-- src/
|   `-- docurag/
|       |-- chat_models/
|       |-- loaders/
|       |-- processors/
|       |-- qa/
|       |-- retrievers/
|       |-- vectorstores/
|       |-- __init__.py
|       |-- cli.py
|       |-- config.py
|       `-- main.py
|-- tests/
|   |-- manual/
|   |-- __init__.py
|   |-- test_builders.py
|   |-- test_cli.py
|   |-- test_config.py
|   |-- test_loaders.py
|   |-- test_qa.py
|   |-- test_retriever.py
|   `-- test_splitter.py
|-- .env.example
|-- .gitignore
|-- pyproject.toml
|-- requirements.txt
`-- README.md
```

## 配置说明

项目当前将聊天模型配置和向量模型配置拆开管理，位于 [src/docurag/config.py](/C:/Users/12142/Documents/DocuRAG/src/docurag/config.py)。

`.env.example` 当前结构如下：

```env
DASHSCOPE_API_KEY=your_dashscope_api_key_here

CHAT_MODEL_PROVIDER=dashscope
CHAT_MODEL=qwen-max
CHAT_API_KEY=

EMBEDDING_PROVIDER=dashscope
EMBEDDING_MODEL=text-embedding-v1
EMBEDDING_API_KEY=

VECTOR_STORE_PROVIDER=chroma
VECTOR_COLLECTION_NAME=docurag_documents
VECTOR_STORE_DIR=
```

默认行为：

- 聊天模型默认是 `qwen-max`
- embedding 模型默认是 `text-embedding-v1`
- 向量库存储目录默认是 `data/vector_store/`

你可以直接使用默认配置，也可以通过环境变量覆盖。

## 安装方式

当前仓库中：

- `requirements.txt` 负责运行依赖和当前测试依赖
- `pyproject.toml` 负责把 `src/` 布局安装成可导入包

因此当前最一致的安装顺序是：

### 1. 创建并激活虚拟环境

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. 安装依赖

```powershell
python -m pip install -r requirements.txt
```

### 3. 安装本地包

```powershell
python -m pip install -e .
```

说明：

- 第 2 步负责安装 LangChain、Chroma、DashScope、`jq`、`pytest` 等依赖
- 第 3 步负责让 `docurag` 包在当前环境中可直接导入

## 运行方式

### 工程初始化 / 加载预览入口

```powershell
python -m docurag.main
```

`docurag.main` 当前定位为：

- 工程初始化入口
- 文档加载预览入口

它当前会：

- 读取环境变量配置
- 检查 `data/raw/` 和向量目录
- 扫描 `data/raw/` 中受支持文件
- 调用文档加载模块
- 打印当前加载结果和失败文件信息

说明：

- 它当前不会自动执行切分、向量入库、检索或问答演示
- 这条入口保持轻量，不承担交互问答职责

### CLI 最小交互入口

单次提问模式：

```powershell
python -m docurag.cli --question "What is DocuRAG?"
```

交互循环模式：

```powershell
python -m docurag.cli --interactive
```

可选参数：

```powershell
python -m docurag.cli --question "What is DocuRAG?" --top-k 2
```

说明：

- CLI 会复用现有的 embedding、Chroma、retriever、chat model 和 QA chain
- CLI 默认直接使用当前正式向量目录和集合配置
- CLI 不会自动重建索引，它假设你已经先完成向量入库
- 如果当前集合里没有文档，CLI 会直接给出明确提示
- 单次提问模式下如果真实问答调用失败，CLI 会打印错误并返回非 0 退出码
- 交互循环模式下如果某次问答失败，CLI 会提示错误并继续等待下一次输入
- `Ctrl+C` 或 EOF 会让交互循环正常结束，不抛出堆栈

## 问答模块当前状态

当前问答模块已经具备：

- 可导入
- 可组装真实 `build_qa_chain()`
- 可通过不依赖外部 API 的自动化测试完成最小链路验证

当前这不表示：

- 问答效果已经优化完成
- 已经具备完整产品级问答体验

## 手工验证脚本

文档加载验证：

```powershell
python tests/manual/manual_loader_test.py
```

文本切分验证：

```powershell
python tests/manual/manual_splitter_test.py
```

向量入库最小验证：

```powershell
python tests/manual/manual_vector_index_test.py
```

检索最小验证：

```powershell
python tests/manual/manual_retriever_test.py
```

问答最小验证：

```powershell
python tests/manual/manual_qa_test.py
```

说明：

- 手工脚本不污染主入口
- 手工向量入库脚本每次运行前会重置测试向量目录中的已有测试索引内容，但保留 `.gitkeep`
- 检索和问答脚本当前使用保守前置检查：
  - 测试向量目录中存在非占位内容
  - 当前测试集合通过公开接口可读取到至少一条已存文档
- 这比只检查目录存在更可靠，但仍不等于完整的底层 Chroma 健康检查
- 正式向量目录仍然是 `data/vector_store/`

## 最小自动化测试

当前自动化测试包括：

- `tests/test_builders.py`
  - 验证聊天模型构造器和 embedding 构造器的基础异常行为
- `tests/test_cli.py`
  - 验证 CLI 单次提问模式的最小链路装配和前置检查
- `tests/test_config.py`
  - 验证 `load_settings()` 默认值和环境变量覆盖行为
- `tests/test_loaders.py`
  - 验证 `get_loader()` 的后缀分发
- `tests/test_splitter.py`
  - 验证 `split_documents()` 是否保留 metadata 并补充 `chunk_index`
- `tests/test_retriever.py`
  - 验证检索模块是否返回与 query 更相关的文档
- `tests/test_qa.py`
  - 直接覆盖真实 `build_qa_chain()` 的最小可组装链路

默认自动化测试入口：

```powershell
python -m pytest -q
```

说明：

- 默认 `pytest` 收集当前只面向 `tests/test_*.py`
- `tests/manual/` 下的脚本定位仍然是手工验证脚本，不参与默认自动化收集
- 手工脚本需要按文件单独执行

运行方式：

```powershell
python -m pytest tests/test_builders.py tests/test_cli.py tests/test_config.py tests/test_loaders.py tests/test_splitter.py tests/test_retriever.py tests/test_qa.py
```
