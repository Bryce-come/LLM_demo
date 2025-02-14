import ast
from typing import Dict, List, Any
import time


class EvaluateProfiler:
    def __init__(self, test_cases: List[Dict[str, Any]]):
        self.test_cases = test_cases

    def evaluate_code(self, code: str) -> Dict[str, Any]:
        """评估代码"""
        try:
            # 编译代码
            tree = ast.parse(code)
            compiled = compile(tree, '<string>', 'exec')

            # 创建命名空间并执行代码
            namespace = {}
            exec(compiled, namespace)

            # 获取主函数
            main_function = None
            for name, obj in namespace.items():
                if callable(obj) and not name.startswith('_'):
                    main_function = obj
                    break

            if not main_function:
                return {
                    'success': False,
                    'error': '未找到可执行函数',
                    'score': 0
                }

            # 评估结果
            results = []
            total_time = 0

            # 运行测试用例
            for case in self.test_cases:
                start_time = time.time()
                try:
                    result = main_function(case['input'])
                    end_time = time.time()

                    # 检查结果
                    is_correct = result == case['expected']
                    execution_time = end_time - start_time

                    results.append({
                        'success': is_correct,
                        'time': execution_time,
                        'input': case['input'],
                        'expected': case['expected'],
                        'actual': result
                    })

                    total_time += execution_time

                except Exception as e:
                    results.append({
                        'success': False,
                        'error': str(e),
                        'input': case['input']
                    })

            # 计算得分
            success_count = sum(1 for r in results if r.get('success', False))
            score = (success_count / len(self.test_cases)) * 100

            return {
                'success': score == 100,
                'score': score,
                'average_time': total_time / len(self.test_cases),
                'results': results
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'score': 0
            }
