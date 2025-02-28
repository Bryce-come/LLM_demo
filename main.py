import asyncio
import os
from configs import Config
from utils import ensure_directories
from profiler import Profiler
from read_case_to_json import CaseReader
import sys

async def main():
    try:
        ensure_directories()

        # 从目录读取测试用例
        case_reader = CaseReader(Config.CASE_PATH)
        test_cases = case_reader.read_cases()

        if not test_cases:
            print("在 cases 目录中未找到测试用例。")
            sys.exit(1)

        # 初始化分析器
        profiler = Profiler()
        profiler.set_test_cases(test_cases)

        # 生成并评估代码
        result = await profiler.generate_and_evaluate()

        if result:
            print("\n=== 生成的代码 ===")
            print(result['code'])
            print("\n=== 评估结果 ===")
            print(f"得分: {result['evaluation']['score']}")
            if result['evaluation']['success']:
                print("所有测试用例通过！")
            else:
                print("部分测试用例失败。")
        else:
            print("代码生成失败")

    except Exception as e:
        print(f"执行失败: {e}")
        sys.exit(1)

def run_main():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n程序被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"程序异常: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_main()