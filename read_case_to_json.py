import json
import os
from typing import List, Dict, Any

class TestCase:
    def __init__(self, input_data, expected_output, description=""):
        self.input_data = input_data
        self.expected_output = expected_output
        self.description = description

class CaseReader:
    def __init__(self, case_dir: str):
        self._case_dir = case_dir

    def read_cases(self) -> List[Dict]:
        cases = []

        for file_name in os.listdir(self._case_dir):
            if file_name.endswith('.txt'):
                case_path = os.path.join(self._case_dir, file_name)
                case = self._parse_case_file(case_path)
                if case:
                    cases.append(case)

        return cases

    def _parse_case_file(self, file_path: str) -> Dict:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            sections = content.split('---')

            input_data = self._parse_section(sections[0])
            expected_output = self._parse_section(sections[1])
            description = sections[2].strip() if len(sections) > 2 else ""

            return {
                'input': input_data,
                'expected': expected_output,
                'description': description
            }

        except Exception as e:
            print(f"解析案例文件 {file_path} 失败: {e}")
            return None

    def _parse_section(self, section: str) -> Any:
        try:
            lines = [line.strip() for line in section.split('\n') if line.strip() and not line.strip().startswith('#')]

            data = ' '.join(lines)
            return json.loads(data)

        except json.JSONDecodeError:
            result = {}
            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    result[key.strip()] = value.strip()
            return result