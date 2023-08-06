import json

from XsCore import XsFso


class XsJson:
    def __init__(self, path):
        """
        :param path: json文件的路径，可以是相对路径 'data/action.json'
        """
        self.save_path = path

    def save(self, jsonobj):
        """
        将对象序列化到json文件
        :param jsonobj: 可以是列表，也可以是字典
        :return:
        """
        with open(self.save_path, 'w', encoding="utf-8") as fp:
            json.dump(jsonobj, fp, indent=4, ensure_ascii=False)

    def load(self):
        str_json = XsFso.readFile(self.save_path)
        if len(str_json) > 1:
            return json.loads(str_json)
        return None
