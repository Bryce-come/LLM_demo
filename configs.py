import os
from dotenv import load_dotenv
import sys

# 加载环境变量
load_dotenv()


class Config:
    # DeepSeek配置
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    if not DEEPSEEK_API_KEY:
        print("错误: 未设置 DEEPSEEK_API_KEY 环境变量")
        print("请在 .env 文件中设置 DEEPSEEK_API_KEY=your-api-key")
        sys.exit(1)

    DEEPSEEK_API_BASE = "https://api.deepseek.com/v1"
    # 修改为正确的模型名称
    DEEPSEEK_MODEL = "deepseek-chat"  # 或者使用 "deepseek-coder"

    # 路径配置
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    CODE_PATH = os.path.join(DATA_DIR, "code")
    CASE_PATH = os.path.join(DATA_DIR, "cases")
    OUTPUT_PATH = os.path.join(DATA_DIR, "output")

    # 生成配置
    MAX_TOKENS = 2000 # 限制最大token可以帮助控制生成文本的长度
    TEMPERATURE = 0.7 # 温度越高，生成的结果越多样化，保证多样性和确定性

    # 评估配置
    MIN_SCORE_THRESHOLD = 0.7 # 最低得分阈值，低于该阈值则认为响应无效
    MAX_RETRIES = 3 # 允许响应的最大次数