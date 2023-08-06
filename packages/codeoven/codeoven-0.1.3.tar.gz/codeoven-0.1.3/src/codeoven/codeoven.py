import re
import subprocess
import os
import sys, json
import time
import pandas as pd
import numpy as np
from datetime import datetime
from glob import glob
import hashlib
import ast
import logging


class RE:
    @classmethod
    def parameter(cls):
        return re.compile(r"(\s*)(const)?\s*(double|int|float|char)\s*(\w+)\s*=\s*([0-9\.e\-\+\*/]+)\s*;\s*//([^@]*)@oven(.*)")

    @classmethod
    def substitution(cls):
        return re.compile(r"(\s*)([\w\.]+)\s*=\s*([0-9\.e\-\+\*/]+)\s*;\s*//([^@]*)@oven(.*)")
    
    @classmethod
    def array1d(cls):
        return re.compile(r"(\s*)(double|int|float|char)\s*(\w+)\[([0-9]+)?\]\s*=\s*(\{[0-9,\s\.]*\})\s*;\s*//([^@]*)@oven(.*)")

    @classmethod
    def printf(cls):
        return re.compile(r"(\s*)printf\(\s*\"([^\"]+)\"\s*,\s*([^;]*);\s*//([^@]*)@oven(.*)")

    @classmethod
    def printf_text(cls):
        return re.compile(r"(\w+):%(d|ld|f|lf)")

class Parameter:
    p = RE.parameter()
    def __init__(self, code):
        self.info = None
        m = re.match(self.p, code)
        if m is None:
            return
        indent, const_flag, var_type, var_name, value, comment, oven_param = m.groups()
        if oven_param is not None:
            oven_param = oven_param.strip()
        assert (oven_param is None) or (oven_param in [".compile", ""] or (oven_param.startswith(".assign:")))
        self.info = {"indent": indent, "const_flag": const_flag is not None, 
                        "var_type": var_type, "var_name": var_name, 
                        "value": value, "comment": comment.strip(), "oven_param": oven_param}
    
    def compose(self, value_dict, burn_flag):
        value = self.info["value"]
        if self.info["var_name"] in value_dict:
            value = value_dict[self.info["var_name"]]
        output_str = ""
        output_str += self.info["indent"]
        output_str += "const " if self.info["const_flag"] else ""
        output_str += self.info["var_type"] + " "
        output_str += self.info["var_name"]
        output_str += f" = {value};"
        if len(self.info["comment"]):
            output_str += f"// " + self.info["comment"]
        output_str += "\n"
        
        if self.info["oven_param"] != ".compile" and not burn_flag:
            output_str += self.info["indent"]
            output_str += f"printf(\"@oven<|{self.info['var_name']}\\n\");\n"
            output_str += self.info["indent"]
            output_str += f"fflush(stdout);\n"
            output_str += self.info["indent"]
            output_str += f"scanf(\"%d\", &{self.info['var_name']});\n"
        return output_str

    @property
    def name(self):
        if self.info is None:
            return None
        return self.info["var_name"]
    
    @property
    def is_valid(self):
        return self.info is not None

class VariableSubstitute:
    p = RE.substitution()
    def __init__(self, code):
        self.info = None
        m = re.match(self.p, code)
        if m is None:
            return
        indent, var_name, value, comment, oven_param = m.groups()
        self.info = {"indent": indent, "var_name": var_name, "value": value, "comment": comment.strip(), "oven_param": oven_param}
    
    def compose(self, value_dict, burn_flag):
        output_str = ""
        if self.info["oven_param"] != ".compile" and not burn_flag:
            output_str += self.info["indent"]
            output_str += f"printf(\"@oven<|{self.info['var_name']}\\n\");\n"
            output_str += self.info["indent"]
            output_str += f"fflush(stdout);\n"
            output_str += self.info["indent"]
            output_str += f"scanf(\"%lf\", &{self.info['var_name']});\n"
        else:
            value = self.info["value"]
            if self.info["var_name"] in value_dict:
                value = value_dict[self.info["var_name"]]
            output_str += self.info["indent"]
            output_str += self.info["var_name"]
            output_str += f" = {value};"
            if len(self.info["comment"]):
                output_str += f"// " + self.info["comment"]
            output_str += "\n"

        return output_str

    @property
    def name(self):
        if self.info is None:
            return None
        return self.info["var_name"]
    
    @property
    def is_valid(self):
        return self.info is not None

class Print:
    p = RE.printf()
    p_text = RE.printf_text()
    def __init__(self, code):
        self.info = None
        m = re.match(self.p, code)
        if m is None:
            return
        indent, text, args_str, comment, oven_param = m.groups()
        output_dict = {}
        m_text = re.match(self.p_text, text)
        if m_text is not None:
            key, fmt_type = m_text.groups()
            output_dict[key] = {"fmt_type": fmt_type}

        self.info = {"indent": indent, "output_dict": output_dict, "text": text, "args_str": args_str, "comment": comment.strip(), "oven_param": oven_param}

    def compose(self, _):
        text = "@oven|>" + self.info["text"]
        args_str = self.info["args_str"]
        output_str = ""
        output_str += self.info["indent"]
        output_str += f"printf(\"{text}\",{args_str};"
        if len(self.info["comment"]):
            output_str += f"// " + self.info["comment"]
        output_str += "\n"
        return output_str

    @property
    def name(self):
        if self.info is None:
            return None
        return ",".join(self.info["output_dict"].keys())
    
    @property
    def is_valid(self):
        return self.info is not None


class Array1D:
    p = RE.array1d()
    margin_factor = 1.5
    def __init__(self, code):
        self.info = None
        m = re.match(self.p, code)
        if m is None:
            return
        indent, var_type, var_name, size_dim0, values, comment, oven_param= m.groups()
        if size_dim0 is not None:
            size_dim0 = ast.literal_eval(size_dim0)
        self.info = {"indent": indent, "var_type": var_type, "var_name": var_name, "size_dim0": size_dim0, "values": values, "comment": comment.strip(), "oven_param": oven_param}

    def compose(self, value_dict):
        data = value_dict[self.info["var_name"]]
        if isinstance(data, list):
            data = np.array(data)
        size_dim0 = self.info["size_dim0"] if self.info["size_dim0"] is not None else int(data.size*self.margin_factor)
        output_str = ""
        output_str += self.info["indent"]
        output_str += f"{self.info['var_type']} "
        output_str += self.info["var_name"]
        output_str += f"[{size_dim0}];"
        output_str += "\n"
        output_str += self.info["indent"]
        output_str += f"oven_receive_double_array1d(\"{self.info['var_name']}\", {self.info['var_name']});\n"
        return output_str

    @property
    def name(self):
        if self.info is None:
            return None
        return self.info["var_name"]
    @property
    def is_valid(self):
        return self.info is not None

class Data2D:
    p = re.compile(r"(\s*)double\s*([a-zA-Z0-9_]+)\[([0-9]+)\]\[([0-9]+)\]\s*=\s*(\{[0-9_\{\},\s\.]*\});")
    def __init__(self, code):
        self.info = None
        m = re.match(self.p, code)
        if m is None:
            return
        indent, var_name, array_dim0, _, _ = m.groups()
        self.info = {"indent": indent, "var_name": var_name, "array_dim0": array_dim0}
    
    def compose(self, data):
        if isinstance(data, pd.core.frame.DataFrame):
            data = data.to_numpy()
        if isinstance(data, list):
            data = np.array(data)
        output_str = ""
        output_str += self.info["indent"]
        output_str += "double "
        output_str += self.info["var_name"]
        output_str += f"[{data.shape[0]}][{data.shape[1]}] = "
        output_str += "{"
        output_str += ",".join(["{" + ",".join([str(x) for x in row]) + "}" for row in data])
        output_str += "};\n"
        return output_str

    @property
    def name(self):
        if self.info is None:
            return None
        return self.info["var_name"]
    @property
    def is_valid(self):
        return self.info is not None

class Result:
    def __init__(self, oven):
        self._oven = oven
        self.header_names = {}

    def set_header(self, header_names):
        assert isinstance(header_names, (dict, list)), "header_names should be list or dict of list"
        self.header_names = header_names.copy()
    @property
    def keys(self):
        return list(self._oven.file_dict.keys())
    
    @property
    def df(self):
        assert len(self.keys) == 1
        return self[self.keys[0]]

    def __getitem__(self, key):
        if key not in self._oven.file_dict:
            return None
        if self._oven.file_dict[key].name.endswith(".csv"):
            header_names = None
            if isinstance(self.header_names, dict) and key in self.header_names:
                header_names = self.header_names[key]
            elif isinstance(self.header_names, list):
                header_names = self.header_names
            df = pd.read_csv(self._oven.file_dict[key].path(self._oven.work_dir), names=header_names)
            return df
        
class Dough:
    def __init__(self, file_name:str, logger=None):
        self.file_name = file_name
        self.codes = []
        self.parameter_dict = {}
        self.file_dict = {}
        self.output_dict = {}
        self.flag_dict = {}
        # self.logger = logger if logger is not None else logzero.logger
        self.hash = None
        self.parse()

    def parse(self):
        # Extract [oven:~] blocks
        p = re.compile(r"//\s*\[oven:([a-z]+):?([a-z]*)\]")
        with open(self.file_name, "r") as f:
            codes = f.readlines()
        self.hash = hashlib.md5("\n".join(codes).encode()).hexdigest()
        context = None
        
        for code in codes:
            if len(code.strip()) == 0:
                continue
            m = re.match(p, code.strip().lower())
            if m is not None:
                command = m.groups()
                if context is not None:
                    assert command[0] == "endof"+context or command[0] == "end"
                    context = None
                else:
                    context = command[0].lower()
                continue
            
            if context == "parameters" or context == "parameter":
                if self.parse_context_parameters(code):
                    continue
                self.logger.warning(f"Invalid parameter: {code}")

            if context == "file" or context == "files":
                if self.parse_context_files(code):
                    continue
                self.logger.warning(f"Invalid file: {code}")

            if context == "data":
                if self.parse_context_data(code):
                    continue
                self.logger.warning(f"Invalid data: {code}")
            
            if context == None:
                if self.investigate(code):
                    continue

            self.codes.append(code)
            self.flag_finder(code)

    def investigate(self, code):
        c = Parameter(code)
        if c.is_valid:
            self.parameter_dict[c.name] = c
            self.codes.append(c)
            return True

        c = VariableSubstitute(code)
        if c.is_valid:
            self.parameter_dict[c.name] = c
            self.codes.append(c)
            return True

        c = Print(code)
        if c.is_valid:
            self.output_dict[c.name] = c
            self.codes.append(c)
            return True

        c = Array1D(code)
        if c.is_valid:
            self.parameter_dict[c.name] = c
            self.codes.append(c)
            return True

            
    
    def parse_context_parameters(self, code:str):
        parameter = Parameter(code)
        if parameter.is_valid:
            self.parameter_dict[parameter.name] = parameter
            self.codes.append(parameter)
            return True
        parameter = VariableSubstitute(code)
        if parameter.is_valid:
            self.parameter_dict[parameter.name] = parameter
            self.codes.append(parameter)
            return True

        return False

    def parse_context_data(self, code:str):
        d = Data2D(code)
        if d.is_valid:
            self.data_dict[d.name] = d
            self.codes.append(d)
            return True
        self.logger.warning(f"Invalid data: {code}")
        self.codes.append(code)
        return False

    def compose(self, parameters:dict=None, burn_flag=False):
        if parameters is None:
            parameters = {}

        output_codes = []
        output_codes.append('#include "oven_utils.h"\n')
        for code in self.codes:
            if isinstance(code, str):
                output_codes.append(code)
            if isinstance(code, (Parameter, VariableSubstitute)):
                output_codes.append(code.compose(parameters, burn_flag))
            if isinstance(code, Print):
                output_codes.append(code.compose(parameters))
            if isinstance(code, (Array1D)):
                output_codes.append(code.compose(parameters))
        return output_codes

    def flag_finder(self, code:str):
        if "<gsl" in code:
                self.flag_dict["gsl"] = "-lgsl"

class ProcessRunner:
    def __init__(self):
        self.result_dict = {}

    def run(self, exec_name):
        result = subprocess.run([exec_name], encoding="UTF-8", stdout=subprocess.PIPE)
        for output in result.stdout.splitlines():
            self.extract_result(output)

        return self.organize(self.result_dict)

    def communicate(self, exec_name, parameters):
        st = time.time()
        with subprocess.Popen([exec_name], encoding="UTF-8", stdin=subprocess.PIPE, stdout=subprocess.PIPE) as proc:
            while True:
                output = proc.stdout.readline().strip()
                if len(output) == 0:
                    break
                if self.extract_result(output):
                    continue
                if output.startswith("@oven<|"):
                    key = output[7:]
                    if key in parameters:
                        self.send(proc, f"{parameters[key]}")
                    else:
                        print(f"Parameter not found: {key}")
                        proc.kill()
                        
                elif output.startswith("@oven.array<|"):
                    key = output[13:]
                    if key in parameters:
                        self.send(proc, f"{len(parameters[key])}")
                        self.send(proc, ",".join([f"{x}" for x in parameters[key]]))
                    else:
                        print(f"Parameter not found: {key}")
                        proc.kill()
                else:
                    if len(output) < 80:
                        print(output)
                    else:
                        print(f"-- Long output with a length of {len(output)} starting from '{output[:5]}' --")
        return self.organize(self.result_dict)
    
    def extract_result(self, output:str) -> bool:
        if not output.startswith("@oven|>"):
            return False
        output = output[7:]
        output_items = output.split(":")
        key = output_items[0]
        value = ast.literal_eval(":".join(output_items[1:]))

        if key in self.result_dict:
            self.result_dict[key].append(value)
        else:
            self.result_dict[key] = [value]
        return True
    
    def organize(self, result_dict):
        new_dict = {}
        for key, value in result_dict.items():
            if len(value) == 1:
                new_dict[key] = value[0]
            else:
                new_dict[key] = value
        return new_dict

    def send(self, proc, body):
        proc.stdin.write(body + "\n")
        proc.stdin.flush()


class Oven:
    def __init__(self, file_name, logger=None):
        self.dough = Dough(file_name)
        self.callback_func = None
        self.baked = False
        # self.logger = logger if logger is not None else logzero.logger

    def bake(self, parameters:dict=None, burn_flag:bool=False) -> None:
        if parameters is None:
            parameters = {}   

        output_codes = self.dough.compose(parameters, burn_flag=burn_flag)
        with open(f"oven_{self.dough.file_name}", "w") as f:
            f.writelines(output_codes)
        flags = ["-O2"] + list(self.dough.flag_dict.values())
        flag_str = " ".join([f"{x}" for x in flags])
        module_dir = os.path.dirname(__file__)
        subprocess.run(f"export C_INCLUDE_PATH='{module_dir}';cd '{os.getcwd()}';clang {flag_str} oven_{self.dough.file_name} '{module_dir}/oven_utils.c';", shell=True)
        self.baked = True

    
    def run(self, parameters:dict=None):
        if parameters is None:
            parameters = {}
        if not self.baked:
            self.bake(parameters)
            
        log_dict = {}
        st = time.time()
        runner = ProcessRunner()
        result = runner.communicate("./a.out", parameters)
        
        return result
    
    def burn(self, parameters:dict=None):
        self.bake(parameters, burn_flag=True)
        runner = ProcessRunner()
        result = runner.run("./a.out")
        return result


if __name__ == "__main__":
    oven = Oven("test.c")
    for i in range(100):
        st = time.time()
        oven.run({"a": [2, 3, 4]*500})
        print(f"{i}:{time.time()-st:.5f} s")

    if len(sys.argv) == 2:
        src_filename = sys.argv[1]
        oven = Oven(src_filename)
        output_str = """from codeoven import Oven
import sys\n\n"""
        for key, value in oven.parameters.items():
            output_str += f"# {key} {value['unit'] if value['unit'] is not None else ''}: {value['value']}\n"

        output_str += f"""
if __name__ == "__main__":
    oven = Oven("{src_filename}")
    parameters = {{}}
    oven.bake(parameters)
        """
        with open("oven.py", "w") as f:
            f.write(output_str)