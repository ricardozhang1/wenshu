# coding: utf-8
import base64
import json
import time

import pyDes
import requests
import execjs
import time

d_time = time.strptime(time.ctime())
v = str(d_time.tm_year) + str(d_time.tm_mon) + str(d_time.tm_mday)

js_text = """
function cipher() {
    var info = {};
	var date = new Date();
	var timestamp = date.getTime().toString();
	var salt = rand_str(24);
	var year = date.getFullYear().toString();
	var month = (date.getMonth() + 1 < 10 ? "0" + (date.getMonth() + 1) : date.getMonth()).toString();
	var day = (date.getDate() < 10 ? "0" + date.getDate() : date.getDate()).toString();
	var iv = year + month + day;
	info["timestamp"] = timestamp
	info["salt"] = salt
	info["iv"] = iv
	info["date"] = date
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


def cipher():
    js_var = execjs.compile(js_text)
    ss = js_var.call('cipher')
    print(ss)
    enc = DES3.encryption(ss['timestamp'], ss['salt'], '20201028')
    print(enc)
    dd_str = ss['salt'] + '20201028' + enc
    ciphertext = js_var.call('strTobinary', dd_str)
    print(ciphertext)
    return ciphertext, ss


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


doc_id_dict = {"0489872404624e6b9074ac0600c4d800":[],"a31a731395604fc0b94aac1100bee448":[],"c52698c3ab67412c8764ac1100bee47c":[],"754878e4d60242f3b795abbf0115f46b":[],"6b9f617824354818b10eabea012995f8":[],
"0ee7da1c6e90465fa2a7abe800d4ecea":[],"462d79e68997400bb68fabbf0115f4af":[],"abb32689cce44c368253ac1700bed8a6":[],"23a741665deb43c4a90fabcf00d43d40":[],"bae832907a1b4683a827ac1700bed899":[],
"33ec65d4408f44cc8870abac0115c24a":[],"fb125ed65d9b41158437abbf0115f4e0":[],"236a2fffb5474fb4ad45abac0115c217":[],"6a0a5108f41c4b95afa5abac0115c25d":[],"9840d84631694c889892abac0115c232":[],
"2f71ebe3d6fb4efc9153aa9500c00a3f":[],"bcd74bf4238f4719a413ab090117753f":[],"3af51d5a502747c5b074aad600c0c9d6":[],"84794041794a43f0b6c5aacc01139663":[],"41945ee88e524b36b2d9aa9c00c07997":[],
"a1528ad6705845d9b023a9e601154302":[],"645f8bebcba349b9a533a99e01220aaf":[],"de374f1998254181b91aa9e601154069":[],"e8998cce191a4b798bf4a9e6011542e5":[],"9da1b7be8bf4416a8a2fa9fb010fa9d0":[],
"f2459267fa95401baec4abdc00fe99b0":[],"8336fe4bdbb44465b14cab3a00c209c7":[],"8a24599855f64d5bb1eeaacc01139690":[],"1c4109095b204614ba21aae300c0d188":[],"f31dbb332b3847bca27aaae300c0d14b":[],
"00c89fc6548c40309a60aa0200efdbe8":[],"318b7232dbe24c588ba4aa0200efdb99":[],"7bbfcad140d74712ac37a9b901112fa7":[],"f977920475b541b18de0a9c700c5f10a":[],"a7580f4caef043dfabc5ab0901177557":[],}

for doc_id in doc_id_dict.keys():
    print('==='*10, doc_id)
    # time.sleep(2)
    ciphertext, ss = cipher()
    print(ss)
    post_data = {
        "docId": f"{doc_id}",
        "ciphertext": ciphertext,
        "cfg": "com.lawyee.judge.dc.parse.dto.SearchDataDsoDTO@docInfoSearch",
        "__RequestVerificationToken": ss['salt'],
    }
    response = requests.post(url, headers=headers, data=post_data, cookies=cookie)
    if 'HTTP Status 503' in response.text:
        print('【服务器繁忙】 爬的人太多了， 请重试')
        exit()
    data = json.loads(response.text)
    content = data.get('result')
    key = data.get('secretKey')
    iv = v
    print(content)


    def parse_html(content, key, iv):
        _str = DES3.decrypt(content, key, iv)
        print("【解密返回结果】：", _str)

    ddd_data = parse_html(content, key, iv)







