import os


class FileSearch(object):

    BANK_LIST = ["北京银行", "渤海银行", "大连银行", "广发银行", "汉口银行", "昆仑银行",
                 "马农商&合肥科技农商行", "农商银行", "浙商银行", "邮储银行", "进出口银行", "华夏银行",]

    XLS_SUFFIX = [".xls", ".csv", ".xlsx"]
    PDF_SUFFIX = [".pdf"]
    FILE_PREFIX = "H"

    ROOT_DIR = r"C:\nas-个人文件夹\RPA用（误删）\RPA银行下载文件"
    __sub_dirs = []

    def __init__(self,
                 run_date: str,
                 root_dir=ROOT_DIR) -> None:

        self.run_date = run_date
        self.root_dir = root_dir

    def search_bankflow_files(self) -> list[str]:
        return self.search_files(file_suffix=self.XLS_SUFFIX,
                                 bank_list=self.BANK_LIST)

    def search_rct_files(self) -> list[str]:
        return self.search_files(file_suffix=self.PDF_SUFFIX)

    def search_files(self, file_suffix=None, bank_list=None) -> list[str]:
        found_files = []
        dirs = self.search_dirs(bank_list)
        for dir in dirs:
            for f in os.listdir(dir):
                f_path = os.path.join(dir, f)
                if os.path.basename(f_path).startswith(self.FILE_PREFIX):
                    if file_suffix is None:
                        found_files.append(f_path)
                    elif os.path.splitext(f)[-1] in file_suffix:
                        found_files.append(f_path)
                        print(f"match:{f_path}")
                else:
                    print(f"file_prefix not match:{f_path}")
        return found_files

    def search_dirs(self, bank_list: list[str] = None):
        self.__traversal_dirs(self.root_dir)

        match_dirs = []
        for dir in self.__sub_dirs:
            if os.path.basename(dir) == self.run_date:
                if bank_list is None:
                    match_dirs.append(dir)
                elif (dir.split("\\")[-3]) in bank_list:
                    match_dirs.append(dir)
        return match_dirs

    def __traversal_dirs(self, path):
        for item in os.scandir(path):
            if item.is_dir():
                self.__sub_dirs.append(item.path)
                self.__traversal_dirs(item)
            else:
                pass


if __name__ == "__main__":
    FileSearch("2022-11-07", r"D:\Ouye\12家银行流水回单").search_rct_files()
