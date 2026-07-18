# 项目说明笔记

## 当前实现范围

DocuRAG 当前已经完成：

- 工程脚手架
- `src` 布局包配置
- 环境变量配置加载
- 多格式文档加载
- 文本切分
- 向量化与索引
- 检索模块
- 最小问答链组装
- CLI 交互入口
- 各阶段手工验证脚本

当前还未完成：

- 问答效果优化
- 更完整的产品交互层

## 配置层

[src/docurag/config.py](/C:/Users/12142/Documents/DocuRAG/src/docurag/config.py) 当前把运行时配置拆成三部分：

- `ChatModelSettings`
- `EmbeddingModelSettings`
- `VectorStoreSettings`

默认值：

- Chat provider：`dashscope`
- Chat model：`qwen-max`
- Embedding provider：`dashscope`
- Embedding model：`text-embedding-v1`
- Vector store provider：`chroma`

环境变量可以覆盖这些默认值。

## 检索模块

当前最小检索层位于：

- [src/docurag/retrievers/chroma_retriever.py](/C:/Users/12142/Documents/DocuRAG/src/docurag/retrievers/chroma_retriever.py)

职责：

- 重新打开持久化 Chroma store
- 执行相似度检索

## 问答模块

当前最小问答层位于：

- [src/docurag/chat_models/builder.py](/C:/Users/12142/Documents/DocuRAG/src/docurag/chat_models/builder.py)
  - 根据当前配置构建聊天模型
- [src/docurag/qa/chain.py](/C:/Users/12142/Documents/DocuRAG/src/docurag/qa/chain.py)
  - 使用 LangChain 经典 retrieval chain 组装最小问答链

当前状态说明：

- 在当前依赖声明下已具备依赖闭环
- 在当前环境中已验证可导入
- 已可通过自动化测试验证最小链路可组装
- 这仍不代表问答效果已经优化完成

## CLI 交互模块

当前最小 CLI 入口位于：

- [src/docurag/cli.py](/C:/Users/12142/Documents/DocuRAG/src/docurag/cli.py)

职责：

- 解析命令行参数
- 检查当前向量集合是否有可用文档
- 复用现有 embedding、chat model、retrieval chain 完成最小问答调用

当前能力边界：

- 支持单次提问模式：`python -m docurag.cli --question "..."`
- 支持简单交互循环：`python -m docurag.cli --interactive`
- 不负责动态构建索引，默认依赖已存在的向量库
- 单次问答调用失败时返回非 0 退出码
- 交互循环中单次问答失败时只提示错误，不直接打崩整个 CLI
- `Ctrl+C` 或 EOF 会正常结束交互循环

## 手工测试脚本

当前脚本包括：

- `tests/manual/manual_loader_test.py`
- `tests/manual/manual_splitter_test.py`
- `tests/manual/manual_vector_index_test.py`
- `tests/manual/manual_retriever_test.py`
- `tests/manual/manual_qa_test.py`

说明：

- 每个脚本都独立于主入口
- 手工向量入库脚本会在写入前重置测试向量目录中的已有测试索引内容
- 检索 / 问答脚本当前使用两层保守前置检查：
  - 测试向量目录中存在非占位内容
  - 当前测试集合通过公开接口可读取到至少一条已存文档
- 这比单纯检查目录存在更可靠，但仍不等于完整的 Chroma 健康检查

补充说明：

- `tests/manual/` 下的文件名虽然看起来像测试文件，但当前项目将它们视为手工验证脚本
- 默认 `python -m pytest -q` 只收集 `tests/test_*.py`
- 手工脚本需要单独执行，不纳入默认自动化测试入口
