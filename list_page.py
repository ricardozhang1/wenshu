# coding: utf-8
import base64
import json

import pyDes
import requests
import execjs
import time


js_text = """
function cipher() {
    var info = {};
	var date = new Date();
	var timestamp = date.getTime().toString();
	var salt = rand_str(24);
	var year = date.getFullYear().toString();
	var month = (date.getMonth() + 1 < 10 ? "0" + (date.getMonth() + 1) : date.getMonth()).toString();
	var day = (date.getDate() < 10 ? "0" + date.getDate() : date.getDate())
			.toString();
	var iv = year + month + day;
	info["timestamp"] = timestamp
	info["salt"] = salt
	info["iv"] = iv
	return info
	
function rand_str(size){
        var str = "",
        arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];
        for(var i=0; i<size; i++){
            str += arr[Math.round(Math.random() * (arr.length-1))];
        }
        return str;
    }
};

function strTobinary(str) {
	var result = [];
	var list = str.split("");
	for (var i = 0; i < list.length; i++) {
		if (i != 0) {
			result.push(" ");
		}
		var item = list[i];
		var binaryStr = item.charCodeAt().toString(2);
		result.push(binaryStr);
	};
	return result.join("");
}
"""


d_time = time.strptime(time.ctime())
v = str(d_time.tm_year) + str(d_time.tm_mon) + str(d_time.tm_mday)

class TripleDesUtils:
    def encryption(self, data: str, key, iv) -> str:
        """3des 加密
        """
        _encryption_result = pyDes.triple_des(key, pyDes.CBC, iv, None, pyDes.PAD_PKCS5).encrypt(data)
        _encryption_result = self._base64encode(_encryption_result).decode()
        return _encryption_result

    def decrypt(self, data: str, key, iv) -> str:
        """3des 解密
        """
        data = self._base64decode(data)
        _decrypt_result = pyDes.triple_des(key, pyDes.CBC, iv, None, pyDes.PAD_PKCS5).decrypt(data).decode('utf-8')
        return _decrypt_result

    @staticmethod
    def _base64encode(data):
        try:
            _b64encode_result = base64.b64encode(data)
        except Exception as e:
            raise Exception(f"base64 encode error:{e}")
        return _b64encode_result

    @staticmethod
    def _base64decode(data):
        try:
            _b64decode_result = base64.b64decode(data)
        except Exception as e:
            raise Exception(f"base64 decode error:{e}")
        return _b64decode_result

DES3 = TripleDesUtils()
js_var = execjs.compile(js_text)
ss = js_var.call('cipher')
print(ss)
enc = DES3.encryption(ss['timestamp'], ss['salt'], v)
print(enc)
dd_str = ss['salt'] + v + enc
ciphertext = js_var.call('strTobinary', dd_str)
print(ciphertext)

post_data = {
    'pageId': '6a2f9ecddbcd10c3b8b6ee759f9f1349',
    's8': '02',
    'sortFields': 's50:desc',
    'ciphertext': ciphertext,
    'pageNum': '66',
    'pageSize': '15',  # 首页不需要这个参数，之后的页面需要翻页
    'queryCondition': '[{"key":"s8","value":"02"},{"key":"s45","value":"非法占有"}]',
    'cfg': 'com.lawyee.judge.dc.parse.dto.SearchDataDsoDTO@queryDoc',
    '__RequestVerificationToken': ss['salt']
}

txt = str(post_data)

request = base64.b64encode(txt.encode('utf-8')).decode('utf-8')
data = {
    'request': request
}

url = "https://wenshu.court.gov.cn/website/parse/rest.q4w"

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://wenshu.court.gov.cn',
    'Host': 'wenshu.court.gov.cn',
}

cookie = {'SESSION': '46373b9b-2be8-4855-b9a5-c044142b0bfd'}

response = requests.post(url, headers=headers, data=post_data, cookies=cookie)
if 'HTTP Status 503' in response.text:
    print('请重试')
    exit()
data = json.loads(response.text)
content = data.get('result')
key = data.get('secretKey')
iv = v
print(key)
print(content)


def parse_html(content, key, iv):
    _str = DES3.decrypt(content, key, iv)
    print("解密返回结果：", _str)


ddd_data = parse_html(content, key, iv)











