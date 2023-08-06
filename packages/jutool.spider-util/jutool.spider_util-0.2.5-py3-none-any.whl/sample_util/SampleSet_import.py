from sample_util.NLSampleSource import NLSampleSourceBase
from code_util.log import log


def import_str_base_csv_file(path: str, source: NLSampleSourceBase, set_name: str, has_header=False, split_char='\t'):
    with open(path, 'r') as f:
        lines = f.readlines()
        lines = [[c.strip() for c in line.split(split_char)] for line in lines]

        col_num = len(lines[0])
        col_name = []
        if has_header:
            col_name = lines[0]
            lines = lines[1:]
        else:
            col_name = [f'col{_i}' for _i in range(col_num)]

    if not source.has_set(set_name):
        source.create_new_set(set_name, f"import data from file{path}", ["import"], col_name)

    for line in lines:
        if len(line) != col_num:
            log(f"行数据异常，跳过{line}")
            continue
        source.add_row(set_name, line)

    source.flush()
