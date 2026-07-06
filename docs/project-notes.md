# 项目说明笔记

## 当前实现范围

当前仓库实现的内容主要是基础工程结构：

- 建立源码目录 `src/kb_rag/`
- 建立数据目录 `data/raw/` 和 `data/vector_store/`
- 建立配置模板 `.env.example`
- 实现环境变量加载
- 实现程序入口
- 实现目录自动检查和创建

当前尚未实现文档解析、切分、向量化、检索和问答逻辑。

## 目录拆分

### `src/`

存放项目源码。

当前代码位于 `src/kb_rag/`，后续各功能模块也会继续放在该目录下拆分。

### `data/raw/`

存放原始输入文档。

这里预留给后续接入的文件类型，例如：

- PDF
- TXT
- Markdown
- CSV
- JSON

### `data/vector_store/`

存放向量索引和相关中间结果。

这个目录和 `data/raw/` 分开，用于区分输入数据与处理后的索引数据。

### `tests/`

预留测试目录。

当前只有基础包文件，后续测试代码会逐步补充到这里。

## 配置文件

### `.env.example`

提供运行配置模板，当前包含以下字段：

- `OPENAI_API_KEY`
- `EMBEDDING_MODEL`
- `CHAT_MODEL`

实际运行时由 `.env` 提供对应值。

### `src/kb_rag/config.py`

当前负责以下内容：

- 计算项目根目录
- 定义 `data/`、`data/raw/`、`data/vector_store/` 路径
- 调用 `load_dotenv()` 加载环境变量
- 使用 `Settings` 数据类统一返回配置

当前 `Settings` 包含三项配置：

- `openai_api_key`
- `embedding_model`
- `chat_model`

## 程序入口

### `src/kb_rag/main.py`

当前入口程序包含三个步骤：

1. 调用 `load_settings()` 读取配置
2. 调用 `ensure_directories()` 创建必要目录
3. 输出当前目录和模型配置

如果没有设置 `OPENAI_API_KEY`，程序会输出提醒信息，但不会中断执行。

## 当前运行结果

运行以下命令：

```powershell
python -m src.kb_rag.main
```

当前预期结果是：

- 能正常读取 `.env`
- 能创建缺失的数据目录
- 能输出当前使用的 embedding 模型和 chat 模型
- 未配置 API Key 时输出警告

## Git 忽略内容

当前 `.gitignore` 排除了以下内容：

- `.venv/`
- `__pycache__/`
- `.env`
- `data/raw/*`
- `data/vector_store/*`

同时通过 `.gitkeep` 保留空目录结构：

- `data/raw/.gitkeep`
- `data/vector_store/.gitkeep`

## 后续实现顺序

当前计划中的后续模块顺序如下：

1. 文档加载
2. 文本切分
3. 向量化与索引
4. 检索
5. 问答生成
6. 交互接口
