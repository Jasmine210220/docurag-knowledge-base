from pathlib import Path
import sys


# 这个脚本需要单独执行，所以这里手动把项目根目录加入 Python 搜索路径。
# 这样做只影响当前测试脚本，不会污染主业务代码的导入方式。
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.docurag.loaders import get_loader


# 这个脚本是手动测试脚本，不是主业务代码。
# 它的作用是：在不影响真实用户数据目录的前提下，单独验证文档加载模块是否正常工作。
TEST_SAMPLES_DIR = PROJECT_ROOT / "data" / "test_samples"


def main() -> None:
    # 手动测试样本目录和 data/raw 分开，是为了避免测试文件和真实业务文件混在一起。
    # 这样后续你在做功能验证时，不会误伤真实用户数据，也不会让测试过程污染正式数据流。
    if not TEST_SAMPLES_DIR.exists():
        print("测试样本目录不存在，请先检查项目结构。")
        return

    # 当前阶段先只搭测试骨架。
    # 如果测试目录里还没有样本文件，就明确提示，而不是报错退出。
    sample_files = [
        file_path
        for file_path in sorted(TEST_SAMPLES_DIR.iterdir())
        if file_path.is_file() and not file_path.name.startswith(".")
    ]

    if not sample_files:
        print("当前没有测试样本，请后续在 data/test_samples/ 中添加测试文件。")
        return

    # 手动测试脚本和主业务代码的目标不同：
    # 主业务代码更关注“正常处理数据”，手动测试脚本更关注“把每个文件的结果都展示出来”。
    # 所以这里按文件逐个测试，这样即使某一种类型失败，也不会影响你观察其他类型的结果。
    total_documents = 0
    success_count = 0
    failure_count = 0

    print(f"扫描到的测试样本数量: {len(sample_files)}")

    for file_path in sample_files:
        print(f"\n=== 测试文件: {file_path.name} ===")

        try:
            loader = get_loader(file_path)
            print(f"使用的 loader: {loader.__class__.__name__}")

            documents = loader.load()
            print(f"返回的 Document 数量: {len(documents)}")

            total_documents += len(documents)
            success_count += 1

            # 为了便于人工检查，这里逐条打印基础信息。
            # 手动测试脚本的价值就在于：结果要让人一眼看懂，而不是只返回一个成功/失败。
            for index, document in enumerate(documents, start=1):
                print(f"\n--- Document {index} ---")
                print(f"来源: {document.metadata.get('source', 'unknown')}")
                print(f"类型: {document.metadata.get('file_type', 'unknown')}")
                print(f"预览: {document.page_content[:100]}")
        except Exception as error:
            # 手动测试脚本要尽量把失败原因明确打印出来，方便判断是代码问题还是环境依赖问题。
            failure_count += 1
            print(f"加载失败: {error}")

    print("\n=== 测试总结 ===")
    print(f"成功文件数: {success_count}")
    print(f"失败文件数: {failure_count}")
    print(f"总 Document 数量: {total_documents}")


if __name__ == "__main__":
    # 不把这段测试逻辑放进主程序，是为了保证主业务入口保持干净。
    # 主程序负责真实功能流转，手动测试脚本只负责开发阶段的单独验证。
    main()
