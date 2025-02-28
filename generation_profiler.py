import openai
from typing import Optional
import time
from configs import Config
import logging

class GenerationProfiler:
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY
        openai.api_base = Config.OPENAI_API_BASE
        self.logger = logging.getLogger('GenerationProfiler')

    async def generate_code(self, prompt: str) -> Optional[str]:
        try:
            response = openai.ChatCompletion.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a Python programming expert. Please provide code solutions in Python."},
                    {"role": "user", "content": prompt}
                ],
                temperature=Config.TEMPERATURE,
                max_tokens=Config.MAX_TOKENS,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0
            )

            code = response.choices[0].message.content
            if "```python" in code:
                code = code.split("```python")[1].split("```")[0]
            elif "```" in code:
                code = code.split("```")[1].split("```")[0]
            return code.strip() if code.strip() else None

        except Exception as e:
            self.logger.error(f"代码生成失败: {str(e)}")
            if hasattr(e, 'response'):
                self.logger.error(f"错误详情: {e.response}")
            return None

    async def get_response(self, prompt: str, retry_count: int = Config.MAX_RETRIES) -> Optional[str]:
        for attempt in range(retry_count):
            try:
                code = await self.generate_code(prompt)
                if code and "def isolated_component_deletion" in code and "return" in code:
                    return code
            except Exception as e:
                self.logger.warning(f"第{attempt + 1}次尝试失败: {str(e)}")
                if attempt < retry_count - 1:
                    time.sleep(2)
                continue
        self.logger.error("达到最大重试次数，代码生成失败")
        return None

    ###