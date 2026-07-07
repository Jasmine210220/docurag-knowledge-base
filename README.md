# DocuRAG：多格式文档知识库问答系统

一个面向多格式文档导入、文本切片、知识库构建与问答流程的本地 RAG 项目。

## 当前进度

当前已完成：

- 项目目录初始化
- Python 包结构初始化
- 环境变量配置加载
- 程序入口建立
- 数据目录自动检查和创建
- 文档导入模块
- 多种文件类型的统一加载入口
- 手动测试脚本和最小测试样本

当前未完成：

- 文本切分
- 向量化与索引
- 检索
- 问答生成
- 交互接口

## 当前支持的文件类型

当前文档导入模块已支持以下格式：

- `.txt`
- `.md`
- `.json`
- `.csv`
- `.pdf`

## 目录结构

```text
.
├── data/
│   ├── raw/
│   ├── test_samples/
│   └── vector_store/
├── docs/
│   └── project-notes.md
├── src/
│   └── docurag/
│       ├── loaders/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── factory.py
│       │   └── file_loaders.py
│       ├── config.py
│       ├── main.py
│       └── __init__.py
├── tests/
│   └── manual/
│       ├── __init__.py
│       └── manual_loader_test.py
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## 目录说明

- `data/raw/`
  - 存放原始输入文档，作为主程序当前默认扫描目录
- `data/test_samples/`
  - 存放最小测试样本，用于手动验证不同文件类型的加载结果
- `data/vector_store/`
  - 存放后续向量索引和相关中间产物
- `docs/project-notes.md`
  - 记录当前项目结构、模块职责和实现说明
- `src/docurag/loaders/`
  - 存放文档导入模块，包括基类、工厂和各文件类型加载器
- `src/docurag/config.py`
  - 负责环境变量加载和基础路径定义
- `src/docurag/main.py`
  - 负责程序入口、配置读取、目录检查和文档加载演示
- `tests/manual/`
  - 存放手动验证脚本

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
python -m src.docurag.main
```

当前入口程序会执行以下操作：

- 加载环境变量
- 检查 `data/raw` 和 `data/vector_store` 目录
- 扫描 `data/raw` 中受支持的文件类型
- 调用对应加载器读取文档
- 输出当前加载结果和首条文档预览

## 手动测试

当前提供了一个手动测试脚本，用于逐个验证不同文件类型的加载结果：

```powershell
python tests/manual/manual_loader_test.py
```

该脚本会：

- 扫描 `data/test_samples/`
- 根据文件后缀选择对应加载器
- 输出每个样本文件返回的 `Document` 数量
- 打印基础元数据和内容预览

当前仓库已包含最小测试样本：

- `sample.txt`
- `sample.md`
- `sample.json`
- `sample.csv`

## 当前代码说明

### `src/docurag/config.py`

负责：

- 定义项目根目录
- 定义数据目录、原始文档目录、测试样本目录、向量目录
- 加载 `.env` 配置
- 生成 `Settings` 配置对象

### `src/docurag/loaders/base.py`

负责：

- 定义文档加载器抽象基类
- 统一加载器输入输出接口
- 统一补充公共元数据

### `src/docurag/loaders/factory.py`

负责：

- 维护文件后缀到加载器的映射关系
- 根据文件类型返回对应加载器
- 提供目录级批量加载入口

### `src/docurag/loaders/file_loaders.py`

负责：

- 实现 TXT / MD 文本加载
- 实现 JSON 加载
- 实现 CSV 加载
- 实现 PDF 加载

### `src/docurag/main.py`

负责：

- 调用配置加载函数
- 确保目录存在
- 扫描原始文档目录
- 调用导入模块并输出当前加载结果

## 依赖说明

当前核心依赖包括：

- `python-dotenv`
  - 加载环境变量
- `langchain-core`
  - 提供 `Document` 数据结构
- `langchain-community`
  - 提供文档加载器实现
- `pypdf`
  - 提供 PDF 读取能力

## Git 忽略规则

当前 `.gitignore` 已排除以下内容：

- `.venv/`
- `.idea/`
- `__pycache__/`
- `.env`
- `data/raw/` 中的真实文档
- `data/vector_store/` 中的索引和缓存文件

`data/test_samples/` 默认忽略，仅保留少量明确列出的最小测试样本。

## 后续计划

后续预计按以下顺序补充模块：

1. 文本切分
2. 向量化与索引
3. 检索
4. 问答生成
5. 交互接口
