import json
import os
from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class TestCase:
    input_data: Dict[str, Any]
    expected_output: Dict[str, Any]
    description: str = ""


class CaseReader:
    def __init__(self, case_dir: str):
        self.case_dir = case_dir

    def read_cases(self) -> List[Dict]:
        """读取所有测试案例并转换为JSON格式"""
        cases = []

        for file_name in os.listdir(self.case_dir):
            if file_name.endswith('.txt'):  # 假设案例文件是txt格式
                case_path = os.path.join(self.case_dir, file_name)
                case = self._parse_case_file(case_path)
                if case:
                    cases.append(case)

        return cases

    def _parse_case_file(self, file_path: str) -> Dict:
        """解析单个案例文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 解析案例内容
            sections = content.split('---')  # 假设使用---分隔不同部分

            case = {
                'id': os.path.basename(file_path).split('.')[0],
                'input_data': self._parse_section(sections[0]),
                'expected_output': self._parse_section(sections[1]),
                'description': sections[2].strip() if len(sections) > 2 else ""
            }

            return case

        except Exception as e:
            print(f"解析案例文件 {file_path} 失败: {e}")
            return None

    def _parse_section(self, section: str) -> Dict:
        """解析案例中的输入或输出部分"""
        try:
            # 移除注释和空行
            lines = [line.strip() for line in section.split('\n')
                     if line.strip() and not line.strip().startswith('#')]

            # 尝试解析为JSON
            data = ' '.join(lines)
            return json.loads(data)

        except json.JSONDecodeError:
            # 如果不是JSON格式，尝试解析键值对格式
            result = {}
            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    result[key.strip()] = value.strip()
            return result

    def save_to_json(self, cases: List[Dict], output_path: str):
        """将案例保存为JSON文件"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(cases, f, indent=2, ensure_ascii=False)
            print(f"案例已保存到: {output_path}")
        except Exception as e:
            print(f"保存案例失败: {e}")