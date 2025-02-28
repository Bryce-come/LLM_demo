import os
from dotenv import load_dotenv
import sys

# 加载环境变量
load_dotenv()

class Config:
    # OpenAI配置
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        print("错误: 未设置 OPENAI_API_KEY 环境变量")
        print("请在 .env 文件中设置 OPENAI_API_KEY=your-api-key")
        sys.exit(1)

    OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    OPENAI_MODEL = "gpt-3.5-turbo"

    # 路径配置
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    CODE_PATH = os.path.join(DATA_DIR, "code")
    CASE_PATH = os.path.join(DATA_DIR, "cases")
    OUTPUT_PATH = os.path.join(DATA_DIR, "output")

    # 生成配置
    MAX_TOKENS = 2000
    TEMPERATURE = 0.7

    # 评估配置
    MIN_SCORE_THRESHOLD = 0.7
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # 增加重试间隔配置