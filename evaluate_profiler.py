import ast
from typing import Dict, List, Any
import time
from utils import validate_matrix
import numpy as np

class EvaluateProfiler:
    def __init__(self, test_cases: List[Dict[str, Any]]):
        self.test_cases = test_cases

    def evaluate_code(self, code: str) -> Dict[str, Any]:
        try:
            if "def isolated_component_deletion" not in code:
                return {
                    'success': False,
                    'error': '未找到预期函数 isolated_component_deletion',
                    'score': 0
                }

            tree = ast.parse(code)
            compiled = compile(tree, '<string>', 'exec')
            namespace = {}
            exec(compiled, namespace)
            main_function = namespace.get('isolated_component_deletion')
            if not callable(main_function):
                return {
                    'success': False,
                    'error': '函数不可调用',
                    'score': 0
                }

            results = []
            total_time = 0

            for case in self.test_cases:
                if not validate_matrix(case['input']):
                    results.append({
                        'success': False,
                        'error': '输入矩阵格式无效',
                        'input': case['input']
                    })
                    continue

                start_time = time.time()
                try:
                    result = main_function(case['input'])
                    end_time = time.time()

                    if not validate_matrix(result):
                        results.append({
                            'success': False,
                            'error': '输出矩阵格式无效',
                            'input': case['input'],
                            'actual': result
                        })
                        continue

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

            success_count = sum(1 for r in results if r.get('success', False))
            score = (success_count / len(self.test_cases)) * 100 if self.test_cases else 0

            return {
                'success': score == 100,
                'score': score,
                'average_time': total_time / len(self.test_cases) if self.test_cases else 0,
                'results': results
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'score': 0
            }

