from configparser import ConfigParser

import xlrd
from logger import Logger


def get_config(cfg_path, section, key=None):

    config = ConfigParser()
    config.read(cfg_path, encoding='utf-8')

    if key != None:
        return config.get(section, key)
    else:
        return config.items(section)


def get_excel_cfg(cfg_path, sheet_name=None, inc_header=True):
    data_list = []
    try:
        xls = xlrd.open_workbook(cfg_path, formatting_info=True)

        if sheet_name:
            sheet = xls.sheet_by_name(sheet_name)
        else:
            sheet = xls.sheet_by_index(0)
        row_start_idx = 0
        if inc_header:
            row_start_idx = 1

        for row in range(row_start_idx, sheet.nrows):
            data_list.append(sheet.row_values(row))
    except Exception as e:
        Logger("encoo\config.py").error(f"get_excel_cfg {e}")

    return data_list


if __name__ == "__main__":
    cfg = get_excel_cfg(
        r"C:\Users\renjunfeng\Desktop\流水汇总文件2023-03-28.xls", inc_header=True)
    print(len(cfg))