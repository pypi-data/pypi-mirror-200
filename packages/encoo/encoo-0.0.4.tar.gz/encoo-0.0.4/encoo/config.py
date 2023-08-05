import os
import os.path
import configparser
import xlrd


class Config:

    def __init__(self, cfg_path):
        self.__config_path = cfg_path

    def get_config(self, section, key=None):
        config = configparser.ConfigParser()
        config.read(self.__config_path, encoding='utf-8')

        if key != None:
            return config.get(section, key)
        else:
            return config.items(section)

    def read_excel(self, excel_path, sheet_name):
        xls = xlrd.open_workbook(excel_path, formatting_info=True)
        sheet = xls.sheet_by_name(sheet_name)

        data_list = []
        for row in range(1, sheet.nrows):
            data_list.append(sheet.row_values(row))
        return data_list


if __name__ == "__main__":
    print(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))    