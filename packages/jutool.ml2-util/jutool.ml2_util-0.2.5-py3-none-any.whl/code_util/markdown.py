import time, abc
from enum import Enum


class draw_markdownobj(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def str_out(self) -> [str]:
        pass


class flowchart_color_enum(str, Enum):
    Red = "#FF0000",
    Yellow = "#FFFF00",
    Blue = "#00BFFF",
    Orange = "#FFA500",
    LightGreen = "#90EE90",
    MediumPurple = "#9370DB",
    Auqamarin = "#7FFFAA",
    DeepSkyBlue = "#00BFFF",
    NavajoWhite = "#FFDEAD",


class flowchart_shape_enum(str, Enum):
    Roundedges = "(%%)",
    Stadium = "([%%])",
    Circle = "((%%))",
    Rhombus = "{%%}",
    Parallelogram = "[/%%/]",
    Asymmetric = ">%%]",
    Hexagon = "{{%%}}",


class draw_markdownobj_flowchart(draw_markdownobj):
    def str_out(self) -> [str]:
        lines = ['```mermaid\n', f'graph {self.oriented}\n']
        for node in self.nodes:
            if node[0] in self.node_shape:
                splite = self.node_shape[node[0]].split("%%")
                left_c = splite[0]
                right_c = splite[1]
            else:
                left_c = '['
                right_c = ']'

            if node[0] in self.node_icon:
                node_str = f"fa:{self.node_icon[node[0]]} {node[1]}"
            else:
                node_str = node[1]

            lines.append(f"{node[0]}{left_c}{node_str}{right_c} \n")

        for line in self.lines:
            if line[2] is None:
                if line[3]:
                    lines.append(f"{line[0]} -.-> {line[1]} \n")
                else:
                    lines.append(f"{line[0]} --> {line[1]} \n")
            else:
                if line[3]:
                    lines.append(f"{line[0]} -.->|{line[2]}| {line[1]} \n")
                else:
                    lines.append(f"{line[0]} -->|{line[2]}| {line[1]} \n")

        for k in self.node_navigate.keys():
            v = self.node_navigate[k]  # self.node_navigate[k].lower().replace(' ', '-')
            lines.append(f'click {k} href "#{v}"\n')

        for node_color_key in self.node_color:
            lines.append(f"style {node_color_key} fill:{self.node_color[node_color_key]}\n")

        lines.append("```\n")
        return lines

    def __init__(self, oriented_left2right=True):
        self.nodes = []
        self.node_color = {}
        self.node_shape = {}
        self.lines = []
        self.oriented = "LR" if oriented_left2right else "TD"
        self.node_navigate = {}
        self.node_icon = {}

    def add_node(self, name, id, anchor_title=None, icon=None):
        self.nodes.append((id, name, None))
        if anchor_title is not None:
            self.node_navigate[id] = anchor_title
        if icon is not None:
            self.node_icon[id] = icon

    def set_node_color(self, id, color: flowchart_color_enum):
        self.node_color[id] = color

    def set_node_shape(self, id, shape: flowchart_shape_enum):
        self.node_shape[id] = shape

    def add_line(self, id1, id2, message=None, dot_line=False):
        self.lines.append((id1, id2, message, dot_line))


class draw_markdownobj_gantt(draw_markdownobj):
    def __init__(self, gantt_title, date_format='YYYY-MM-DD'):
        self.Items = {}
        self.Title = gantt_title
        self.date_format = date_format

    def str_out(self) -> [str]:
        out_str = ['```mermaid\n', 'gantt\n', f'\tdateFormat {self.date_format}\n', f'\ttitle {self.Title}\n']

        for item_key, times in self.Items.items():
            out_str.append(f"\tsection {item_key}\n")
            for t_key, t_time_tulp in times['dates'].items():
                out_str.append(f"\t{t_key}\t:{t_time_tulp[0]}, {t_time_tulp[1]}\n")

        out_str.append('```\n')
        return out_str

    def add_item(self, name):
        self.Items[name] = {
            'dates': {}
        }

    def add_item_data(self, key, date_name, date):
        self.Items[key]['dates'][date_name] = date


class markdowndoc():
    """
    生成Markdown文本的辅助类
    """

    def __init__(self, path, need_toc=True, title_with_index=False):
        """
        初始化函数
        :param path: 生成的目标目录
        :param need_toc: 是否建立目录
        """
        self.file_lines = []
        self.path = path
        self.title_with_index = title_with_index
        self.title_index_stack = []
        self._title_index_level = 0

        self.title_index = {}

        if need_toc:
            self.file_lines.append('[toc] \n')

    def _convert_char(self, ss: str):
        ss = str(ss)
        ss = ss.replace('\\', "\\\\")
        ss = ss.replace("__", "\_\_")
        ss = ss.replace("#", "\#")
        return ss

    def _generate_count_char(self, char, count):
        s = ""
        for _ in range(count):
            s += char

        return s

    def write_title(self, stra, level):
        """
        打印标题, @可替换标题序号， @@可替换序号+标题
        :param stra: 标题内容
        :param level: 标题级别
        :return: 无返回
        """
        if not self.title_with_index:
            self.file_lines.append(f"{self._generate_count_char('#', level)} {self._convert_char(stra)} \n")
        else:
            if level > self._title_index_level:
                if level != self._title_index_level + 1:
                    raise Exception("title level error")
                self.title_index_stack.append(1)
                self._title_index_level = level
            elif level == self._title_index_level:
                self.title_index_stack[-1] += 1
            elif level < self._title_index_level:
                while True:
                    if len(self.title_index_stack) > level:
                        self.title_index_stack.pop(-1)
                        continue
                    break
                self.title_index_stack[-1] += 1
                self._title_index_level = level
            index_str = ".".join([str(xx_) for xx_ in self.title_index_stack])
            self.title_index[stra] = index_str
            self.file_lines.append(f"{self._generate_count_char('#', level)} {index_str} {self._convert_char(stra)} \n")

    def write_line(self, str, is_block=None, ishtml=False):
        """
        打印文字
        :param str: 文字内容
        :param is_block: 是否粗体打印
        :return: 无返回
        """
        if ishtml:
            self.file_lines.append(f"{str} \n")
        elif is_block:
            self.file_lines.append(f"**{self._convert_char(str)}** \n")
        else:
            self.file_lines.append(f"{self._convert_char(str)} \n")

    def write_split_line(self):
        self.file_lines.append("*** \n")

    def write_footer(self):
        self.write_split_line()
        self.write_line(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

    def write_markdown_code(self, str):
        self.file_lines.append(str)

    def write_table(self, title: [], data: [[]]):
        """
        打印表格
        :param title: 标题，list【str】
        :param data: 表格内容， list【list【列内容】】
        :return: 无返回
        """
        title = [self._convert_char(x) for x in title]
        self.file_lines.append(f"| {'|'.join(title)} | \n")
        self.file_lines.append(f"| {'|'.join(['----' for _ in title])} | \n")
        for row in data:
            row = [str(_x).strip() for _x in row]
            row_new = [str(x).replace('\n', '<br>') for x in row]
            # row_new = [self._convert_char(x).replace('\n', '<br>') for x in row]
            self.file_lines.append(f"| {'|'.join(row_new)} | \n")

    def write_img(self, path):
        self.file_lines.append(f"![a{str(time.time())}]({path})\n")

    def write_markdownobj(self, obj: draw_markdownobj):
        for line in obj.str_out():
            self.file_lines.append(line)

    def flush(self):
        """
        输出文件的实际命令
        :return: 无返回
        """

        ordered_key = sorted(self.title_index.keys(), key=lambda x: len(x), reverse=True)

        with open(self.path, 'w', encoding='utf-8') as f:
            lines_new = []
            for ll in self.file_lines:
                for t_key in ordered_key:
                    t_val = self.title_index[t_key]
                    v1 = t_val
                    v2 = f"{t_val} {self._convert_char(t_key)}".lower().replace(' ', '-')
                    ll = ll.replace("@@" + t_key, v2)
                    ll = ll.replace("@" + t_key, v1)
                lines_new.append(ll)
            f.writelines(lines_new)

    def write_code(self, code):
        self.file_lines.append("\n")
        self.file_lines.append("```python \n")
        self.file_lines.append(code)
        self.file_lines.append("\n")
        self.file_lines.append("```\n")

    # def __del__(self):
    #     self.flush()
