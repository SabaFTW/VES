import yaml
from core.fcm_loader import FCMLoader
from core.compiler import Compiler
from core.logger import Logger

class Runtime:
    def __init__(self):
        self.logger = Logger("Ghostcore")
        self.compiler = Compiler()
        self.fcm = FCMLoader()

    def build_case(self, case_file):
        self.logger.info(f"Loading case: {case_file}")
        case_data = self.fcm.load_case(case_file)
        
        self.logger.info("Compiling case…")
        output = self.compiler.compile(case_data)
        
        self.logger.success(f"Build complete: {output}")
        return output
