import asyncio
import os
from configs import Config
from utils import ensure_directories
from profiler import Profiler
import sys


async def main():
    try:
        # 确保目录存在
        ensure_directories()

        # 测试用例
        test_cases = [
            {
                'input': [
                    [0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1],
                    [0, 0, 0, 1, 1, 1],
                    [0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 1, 0, 0]
                ],
                'expected': [
                    [0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 1, 1, 1],
                    [0, 0, 0, 1, 1, 1],
                    [0, 0, 0, 1, 1, 1],
                    [0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0]
                ],
                'description': '消除孤立的1，保持连续的1区域'  # 添加问题描述
            }
        ]

        # 初始化处理器
        profiler = Profiler()
        profiler.set_test_cases(test_cases)

        # 生成和评估代码
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