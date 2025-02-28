from typing import Dict, Any, Optional, List
import logging
from generation_profiler import GenerationProfiler
from evaluate_profiler import EvaluateProfiler
from prompt import PromptGenerator
from utils import save_to_json
import os
from configs import Config

class Profiler:
    def __init__(self):
        self.generation_profiler = GenerationProfiler()
        self.evaluate_profiler = None
        self.test_cases = None
        self.logger = self._setup_logger()

    def _setup_logger(self):
        logger = logging.getLogger('Profiler')
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler('profiler.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def set_test_cases(self, test_cases: List[Dict]):
        self.test_cases = test_cases
        self.evaluate_profiler = EvaluateProfiler(test_cases)
        self.logger.info(f"已设置 {len(test_cases)} 个测试用例")

    async def generate_and_evaluate(self) -> Optional[Dict[str, Any]]:
        try:
            if not self.test_cases:
                self.logger.error("未设置测试用例")
                return None

            prompt = PromptGenerator.get_matrix_transform_prompt()
            self.logger.info("开始生成代码")
            generated_code = await self.generation_profiler.get_response(prompt)

            if not generated_code:
                self.logger.error("代码生成失败")
                return None

            self.logger.info("代码生成成功，开始评估")
            if self.evaluate_profiler:
                evaluation_result = self.evaluate_profiler.evaluate_code(generated_code)

                result = {
                    'code': generated_code,
                    'evaluation': evaluation_result
                }

                output_file = os.path.join(Config.OUTPUT_PATH, 'result.json')
                save_to_json(result, output_file)
                self.logger.info(f"结果已保存到: {output_file}")
                self.logger.info(f"评估完成，得分: {evaluation_result['score']}")
                return result
            else:
                self.logger.error("评估器未初始化")
                return None

        except Exception as e:
            self.logger.error(f"处理失败: {e}")
            return None

    def get_best_result(self, results: List[Dict]) -> Optional[Dict]:
        if not results:
            return None
        sorted_results = sorted(
            results,
            key=lambda x: x['evaluation']['score'],
            reverse=True
        )
        return sorted_results[0]