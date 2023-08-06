import sys, os, getopt
from code_util.log import log_error, log, log_level_enum


class JConfig:
    def __init__(self):
        self.config_map = {}

        def remove_strip_yinhao(str):
            if str[0] == '"' or str[0] == "'":
                str = str[1:]
            if str[-1] == '"' or str[-1] == "'":
                str = str[0:-1]
            return str

        config_file_path = os.path.join(os.getcwd(), 'config.jconfig')
        self.config_file_path = config_file_path
        if os.path.exists(config_file_path):
            with open(config_file_path, 'r') as f:
                all_lines = f.readlines()
                for item in all_lines:
                    equ_index = item.index('=')
                    if equ_index < 0:
                        continue
                    key = item[0:equ_index].strip()

                    key = remove_strip_yinhao(key)

                    value = item[equ_index + 1:].strip()

                    value = remove_strip_yinhao(value)
                    self.config_map[key] = value
        else:
            with open(config_file_path, 'w') as f:
                f.writelines("")

    def get_config(self, key):
        if key in self.config_map:
            return self.config_map[key]
        log(f"no config key : {key}", log_level_enum.Warning)
        with open(self.config_file_path, 'a') as f:
            f.writelines(f'{key}=""\n')
        return None


j_config = JConfig()
__isDebug = True  # True if sys.gettrace() else False

buffer_folder = j_config.get_config("buffer_folder")  # "bufferfoder"
model_folder = j_config.get_config("model_folder")  # "/Users/jiangke/Downloads/models/"
train_model_folder = j_config.get_config("train_model_folder")  # "/Users/jiangke/Downloads/models/train_models/"
data_sample_path = j_config.get_config('data_sample_path')
