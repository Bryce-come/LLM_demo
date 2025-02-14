import os
import json
from typing import List, Dict, Any
from configs import Config

def ensure_directories():
    """确保所有必要的目录存在"""
    directories = [Config.CODE_PATH, Config.CASE_PATH, Config.OUTPUT_PATH]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def save_to_json(data: Any, filepath: str) -> bool:
    """保存数据到JSON文件"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"保存JSON失败: {e}")
        return False

def load_from_json(filepath: str) -> Any:
    """从JSON文件加载数据"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载JSON失败: {e}")
        return None

def validate_matrix(matrix: List[List[int]]) -> bool:
    """验证矩阵格式"""
    if not matrix or not isinstance(matrix, list):
        return False
    if not all(isinstance(row, list) for row in matrix):
        return False
    if not all(all(isinstance(x, int) and x in [0, 1] for x in row) for row in matrix):
        return False
    return True