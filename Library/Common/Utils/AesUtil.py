import base64
import json
import time
from hashlib import sha256

from Crypto.Cipher import AES
from Library.Common.Utils.YamlUtil import YamlUtil
from Crypto.Util.Padding import pad


# 加密通用工具类
class AesUtil(YamlUtil):
    def __init__(self):
        super().__init__()
        self.aes_config_data = self.load_common_config("aes")
        self.aes_key = self.aes_config_data["key"]
        self.aes_iv = self.aes_config_data["iv"]
        self.salt = self.aes_config_data["salt"]

    def encrypt_before_login_get_sign(self):
        """
        :return: 盐 + 时间戳加密 = Sign
        """
        t = time.time()
        timestamp = int(round(t * 1000))
        data_to_encrypt = (self.salt if self.salt else "") + '*' + timestamp.__str__()
        print("-----------------")
        print(data_to_encrypt)
        cipher = AES.new(self.aes_key.encode(), AES.MODE_CBC, self.aes_iv.encode())
        padded_data = pad(data_to_encrypt.encode(), AES.block_size)
        encrypted_data = cipher.encrypt(padded_data)
        return base64.b64encode(encrypted_data).decode()

    def salt_insert_tokens(self, token):
        """
        :param token: token
        :return: salt + token 拼接
        """
        # logger.debug(
        #     f"执行方法 salt_insert_tokens 入参打印：token : {token}, salt : {self.salt}")
        if len(token) < 18:
            raise ValueError("Token长度必须至少为18")
        if len(self.salt) != 8:
            raise ValueError("盐值长度必须为8")

        insert_positions = [4, 10, 18, -2]
        insert_values = [self.salt[i:i + 2] for i in range(0, len(self.salt), 2)]

        for pos, value in zip(insert_positions, insert_values):
            token = token[:pos] + value + token[pos:]
        # logger.debug(
        #     f"执行方法 salt_insert_tokens 加盐后的 token ：{token}")
        return token

    # 盐+token+时间戳 = Sign
    def encrypt_by_cbc(self, token):
        salt_token = self.salt_insert_tokens(token)
        t = time.time()
        timestamp = int(round(t * 1000))
        data_to_encrypt = salt_token + '*' + timestamp.__str__()
        cipher = AES.new(self.aes_key.encode(), AES.MODE_CBC,
                         self.aes_iv.encode())
        padded_data = pad(data_to_encrypt.encode(), AES.block_size)
        encrypted_data = cipher.encrypt(padded_data)
        return base64.b64encode(encrypted_data).decode()

    def decrypt_by_cbc(self, data):
        cipher = AES.new(self.aes_key.encode(), AES.MODE_CBC,
                         self.aes_iv.encode())
        decrypted_data = cipher.decrypt(base64.b64decode(data))
        return decrypted_data.rstrip(b'\0').decode()

    def encrypt_by_ecb(self, token, data):
        def padding(s):
            return s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
        # padding = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
        cipher_text = AES.new(self.get_key(token), AES.MODE_ECB).encrypt(padding(json.dumps(data)).encode("utf-8"))
        return base64.b64encode(cipher_text).decode("utf-8")

    def decrypt_by_ecb(self, token, data):
        try:
            meg = AES.new(self.get_key(token), AES.MODE_ECB).decrypt(base64.b64decode(data)).decode("utf-8")
            return json.loads(meg[:-ord(meg[-1])])
        except Exception as e:
            return f"解码失败: {str(e)}"

    @staticmethod
    def get_key(key) -> bytes:
        hash_obj = sha256(key.encode("utf-8"))
        hash_data = hash_obj.digest()
        return hash_data[:16]

    def encrypt_after_get_sign(self, token):
        """
        encrypt_after_get_sign
        :param token: 登陆-token
        :return: encrypt_after_get_sign
        """
        salt_token = self.salt_insert_tokens(token)
        t = time.time()
        timestamp = int(round(t * 1000))
        data_to_encrypt = salt_token + '*' + timestamp.__str__()
        cipher = AES.new(self.aes_key.encode(), AES.MODE_CBC,
                         self.aes_iv.encode())
        padded_data = pad(data_to_encrypt.encode(), AES.block_size)
        encrypted_data = cipher.encrypt(padded_data)
        return base64.b64encode(encrypted_data).decode()

    def decrypt_response_data(self, data):
        """
        decrypt_response_data
        :param data: 加密数据
        :return: 原数据
        """
        cipher = AES.new(self.aes_key.encode(), AES.MODE_CBC,
                         self.aes_iv.encode())
        decrypted_data = cipher.decrypt(base64.b64decode(data))
        return decrypted_data.rstrip(b'\0').decode()


if __name__ == '__main__':
    test = AesUtil("bw")
