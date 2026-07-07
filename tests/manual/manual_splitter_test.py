from pathlib import Path
import sys


# 这是手动测试脚本，不是主业务代码。
# 它专门用于验证“文档加载 -> 文本切分”这条开发阶段链路是否正常。
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.docurag.loaders import get_loader
from src.docurag.processors import split_documents


# 测试样本仍然只读 data/test_samples，避免影响真实用户未来的数据目录。
TEST_SAMPLES_DIR = PROJECT_ROOT / "data" / "test_samples"


def main() -> None:
    if not TEST_SAMPLES_DIR.exists():
        print("测试样本目录不存在，请先检查项目结构。")
        return

    sample_files = [
        file_path
        for file_path in sorted(TEST_SAMPLES_DIR.iterdir())
        if file_path.is_file() and not file_path.name.startswith(".")
    ]

    if not sample_files:
        print("当前没有测试样本，请先准备测试文件。")
        return

    loaded_documents = []
    skipped_files = 0

    # 这里先复用现有加载模块，把能成功加载的文档收集起来。
    # 如果某一种文件受环境依赖影响加载失败，先跳过并打印原因，不阻塞切分模块的验证。
    for file_path in sample_files:
        try:
            loader = get_loader(file_path)
            loaded_documents.extend(loader.load())
        except Exception as error:
            skipped_files += 1
            print(f"跳过文件 {file_path.name}: {error}")

    if not loaded_documents:
        print("当前没有可用于切分的文档，请先解决加载问题。")
        return

    # 这里故意把 chunk_size 设小一点，方便在测试样本上更容易观察到切分效果。
    chunks = split_documents(
        loaded_documents,
        chunk_size=80,
        chunk_overlap=20,
    )

    print(f"成功加载的原始 Document 数量: {len(loaded_documents)}")
    print(f"跳过的文件数量: {skipped_files}")
    print(f"切分后得到的 chunk 数量: {len(chunks)}")

    # 手动测试脚本的输出重点是“人能看懂”。
    # 所以这里打印前几个 chunk 的来源、序号和文本预览，帮助你直观看到切分结果。
    for chunk in chunks[:5]:
        print("\n--- Chunk ---")
        print(f"来源: {chunk.metadata.get('source', 'unknown')}")
        print(f"类型: {chunk.metadata.get('file_type', 'unknown')}")
        print(f"chunk_index: {chunk.metadata.get('chunk_index', 'unknown')}")
        print(f"预览: {chunk.page_content[:120]}")


if __name__ == "__main__":
    # 不把切分测试逻辑塞进主程序，是为了保持主业务入口干净。
    # 手动测试脚本只服务于开发阶段验证，不参与真实用户流程。
    main()
