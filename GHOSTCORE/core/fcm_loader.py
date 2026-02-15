import yaml

class FCMLoader:
    def load_case(self, case_file):
        with open(case_file, 'r') as f:
            return yaml.safe_load(f)
