from django.shortcuts import render,HttpResponse
import json,base64
from fontTools.ttLib import TTFont
from io import BytesIO
def jiema(request):
    re_date = json.loads(request.body.decode())
    secretKey = re_date["secretKey"]
    # ByteIO把一个二进制内存块当成文件来操作
    code_base = base64.decodebytes(secretKey.encode())
    font = TTFont(BytesIO(code_base))
    # 找出基础字形名称的列表，例如：uniE648，uniE183......
    c = font['cmap'].tables[0].ttFont.tables['cmap'].tables[1].cmap
    res_date ={}
    for k,v in re_date.items():
        result = []
        if v == "":
            res_date[k] = " "
        elif k != "secretKey":
            for i in range(len(v)):
                # 找出每一个字对应的16进制编码
                try:
                    code = int(v[i].encode("unicode-escape").decode()[-4:], 16)
                    x = int(c[code][-2:]) - 1
                    result.append(str(x))
                except:
                    result.append(v[i])
            result = [x for x in result if x!=" "]
            res_date[k] = ''.join(result)
    return HttpResponse(json.dumps(res_date))

def jiematest(request):
    return  render(request,'jiematest.html')
