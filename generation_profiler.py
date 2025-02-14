import openai
from typing import Optional, Dict
import time
from configs import Config


class GenerationProfiler:
    def __init__(self):
        self.client = openai.OpenAI(
            api_key=Config.DEEPSEEK_API_KEY,
            base_url=Config.DEEPSEEK_API_BASE
        )

    async def generate_code(self, prompt: str) -> Optional[str]:
        """生成代码"""
        try:
            response = self.client.chat.completions.create(
                model=Config.DEEPSEEK_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a Python programming expert. Please provide code solutions in Python."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=Config.TEMPERATURE,
                max_tokens=Config.MAX_TOKENS,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0
            )

            code = response.choices[0].message.content

            # 提取代码块
            if "```python" in code:
                code = code.split("```python")[1].split("```")[0]
            elif "```" in code:
                code = code.split("```")[1].split("```")[0]

            return code.strip()

        except Exception as e:
            print(f"代码生成失败: {e}")
            if hasattr(e, 'response'):
                print(f"错误详情: {e.response}")
            return None

    async def get_response(self,
                           prompt: str,
                           retry_count: int = Config.MAX_RETRIES) -> Optional[str]:
        """获取响应，包含重试机制"""
        for attempt in range(retry_count):
            try:
                code = await self.generate_code(prompt)
                if code and "def" in code:
                    return code
            except Exception as e:
                print(f"第{attempt + 1}次尝试失败: {e}")
                if attempt < retry_count - 1:
                    time.sleep(2)
                continue
        return None