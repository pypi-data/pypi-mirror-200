import base64


class XsBase64:

    @staticmethod
    def encodeStr(content: str) -> str:
        return base64.b64encode(content.encode()).decode()

    @staticmethod
    def decodeStr(content: str) -> str:
        return base64.b64decode(content.encode()).decode()

    @staticmethod
    def encodeImage(filepath: str) -> str:
        with open(filepath, "rb") as f:  # 转为二进制格式
            base64_data = base64.b64encode(f.read())  # 使用base64进行加密
        return base64_data.decode()

    @staticmethod
    def decodeImage(save_path: str, content: str) -> str:
        image = base64.b64decode(content.encode())
        with open(save_path, "wb") as f:
            f.write(image)


