
import os
import re
from dateutil.parser import parser
import xlwt
import xlrd
from pypdf import PdfWriter, PdfReader

# 根据key返回Value，如找不到返回空字符


def dict_get(kv: dict, k):
    v = kv.get(k)
    if v is not None:
        return v
    else:
        return ""


def fmt_amt(amt_str="人民币（大写）： 肆仟万元整 ￥ 40,000,000.00元"):
    regex = r"([\d|,|.])+"
    matches = re.finditer(regex, str(amt_str))
    match_text = ""
    for matchNum, match in enumerate(matches, start=1):
        match_text = match.group()
    return match_text.replace(",", "")


def fmt_trans_date(trans_date="2022-09-23 11:41:30"):
    try:
        if (isinstance(trans_date, float)):
            return xlrd.xldate_as_datetime(
                trans_date, 0).strftime("%Y-%m-%d")
        else:
            new_date = trans_date.replace(
                "年", "-").replace("月", "-").replace("日", " ").replace("时", ":").replace("分", ":").replace("秒", "")
        return parser().parse(new_date).strftime("%Y-%m-%d")
    except:
        return trans_date


def get_curno(file_name):
    regex = r"(?<=H_)\d*"
    finds = re.findall(regex, file_name)
    if len(finds) > 0:
        return finds[0]
    else:
        return ""


def read_xl(xl_path, sheet_idx=0):
    xls = xlrd.open_workbook(xl_path, formatting_info=True)
    sheet = xls.sheet_by_index(sheet_idx)
    return sheet


def wt_rct_excel(xl_path, rct_list) -> str:

    excel_header = ["回单流水号", "我方公司名称", "银行名称", "本方银行账号", "日期",
                    "收入金额", "支出金额", "余额", "对方户名", "对方账号", "用途", "摘要", "回单路径"]

    xl = xlwt.Workbook(encoding="uft-8")
    sheet = xl.add_sheet("sheet1", cell_overwrite_ok=False)

    col_idx = 0
    for col_name in excel_header:
        sheet.write(0, col_idx, col_name)
        col_idx = col_idx+1

    row_idx = 1
    for rct in rct_list:
        sheet.write(row_idx, 0, rct.flow_no)  # 流水号
        sheet.write(row_idx, 1, rct.company_name)
        sheet.write(row_idx, 2, rct.bank_name)
        sheet.write(row_idx, 3, rct.cur_no)
        sheet.write(row_idx, 4, rct.trans_date)
        sheet.write(row_idx, 5, rct.rec_amt)
        sheet.write(row_idx, 6, rct.pay_amt)
        sheet.write(row_idx, 8, rct.ant_name)
        sheet.write(row_idx, 9, rct.ant_no)
        sheet.write(row_idx, 12, rct.file_path)

        row_idx = row_idx+1

    xl.save(xl_path)
    return xl_path


def wt_bankflow_excel(xl_path, bankflow_list) -> str:

    excel_header = ["公司名称", "银行名称", "本方银行账号", "日期", "流水号",
                    "收入金额", "支出金额", "余额", "对方户名", "对方账号", "用途",
                    "摘要", "电子回单", "服务器回单路径", "SrvUUID"]

    xl = xlwt.Workbook(encoding="uft-8")
    sheet = xl.add_sheet("sheet1", cell_overwrite_ok=False)

    col_idx = 0
    for col_name in excel_header:
        sheet.write(0, col_idx, col_name)
        col_idx = col_idx+1

    row_idx = 1
    for bf in bankflow_list:
        sheet.write(row_idx, 0, bf.company_name)
        sheet.write(row_idx, 1, bf.bank_name)
        sheet.write(row_idx, 2, bf.bank_no)
        sheet.write(row_idx, 3, bf.trans_date)
        sheet.write(row_idx, 4, bf.flow_no)
        sheet.write(row_idx, 5, bf.rec_amt)
        sheet.write(row_idx, 6, bf.pay_amt)
        sheet.write(row_idx, 7, bf.balance)
        sheet.write(row_idx, 8, bf.ant_name)
        sheet.write(row_idx, 9, bf.ant_no)
        sheet.write(row_idx, 10, bf.purpose)
        sheet.write(row_idx, 11, bf.summary)

        row_idx = row_idx+1

    xl.save(xl_path)
    return xl_path


def split_pdf(pdf_file, output_dir=None):
    f_name = os.path.basename(pdf_file)
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(pdf_file), "subpdf")

    pdfs = []
    try:
        if os.path.exists(output_dir) == False:
            os.mkdir(output_dir)
        reader = PdfReader(pdf_file)
        for index in range(len(reader.pages)):
            writer = PdfWriter()
            pageObj = reader.pages[index]
            writer.add_page(pageObj)
            newpath = os.path.join(output_dir, f"{index}_{f_name}")
            with open(newpath, 'wb') as fw:
                writer.write(fw)

            pdfs.append(newpath)
    except Exception as e:
        print(e)

    return pdfs

if __name__=="__main__":
    fs=split_pdf(r"D:\Ouye\12家银行流水回单\浙商银行\欧冶商业保理有限责任公司\20221107\H 2900000000121800049625 20221101~20221107.pdf")
    for f in fs:
        print(f)
