import base64
import json
import urllib

import requests
from encoo.logger import Logger


class BaiduOCR:

    __logger = Logger("BaiduOCR")

    def __init__(self) -> None:
        pass

    def ocr_table(self, file_path):

        url = "https://aip.baidubce.com/rest/2.0/ocr/v1/table?access_token=" + \
            self.get_access_token()

        payload = f"pdf_file={BaiduOCR.get_file_content_as_base64(file_path, True)}"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        ocr_tables = []

        try:
            response = requests.request(
                "POST", url, headers=headers, data=payload)

            self.__logger.debug(f"BaiduOCR response {response.content}")
            ocr_tables = self.convert_resp(response.content)
        except Exception as ex:
            self.__logger.error(f"BaiduOCR {ex}")

        return ocr_tables

    def convert_resp(self, response) -> list[dict]:
        resp_json = json.loads(response)
        ocr_tables = []
        for t in resp_json["tables_result"]:
            ocr_t = {}
            for body in t["body"]:
                k = f"{body['col_start']}-{body['row_start']}-{body['col_end']}-{body['row_end']}"
                v = body['words']
                ocr_t[k] = v
            # end for
            ocr_tables.append(ocr_t)
        self.__logger.debug(f"BaiduOCR ocr_tables {ocr_tables}")

        return ocr_tables

    @staticmethod
    def get_file_content_as_base64(path, urlencoded=False):
        with open(path, "rb") as f:
            content = base64.b64encode(f.read()).decode("utf8")
            if urlencoded:
                content = urllib.parse.quote_plus(content)
        return content

    def get_access_token(self):
        API_KEY = "WYz5wiwt1PoWQkBqlG2EIGIG-"
        SECRET_KEY = "chYQKg2vkn9eTdB5h80GgKSzjwCnmxat"

        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {"grant_type": "client_credentials",
                  "client_id": API_KEY, "client_secret": SECRET_KEY}
        return str(requests.post(url, params=params).json().get("access_token"))


if (__name__ == "__main__"):
    BaiduOCR().ocr_table(
        r"D:\Ouye\12家银行流水回单\浙商银行\欧冶商业保理有限责任公司\20221107\H 2900000000121800049625 20221101~20221107.pdf")
