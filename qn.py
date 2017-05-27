# -*- coding: utf-8 -*-
# flake8: noqa

from qiniu import Auth, put_data, etag, urlsafe_base64_encode
import qiniu.config

#需要填写你的 Access Key 和 Secret Key
access_key = 'uzc59bVURbUbazey9vrexXKocNKBUN8NuLijk57N'
secret_key = '-9lenw28jU2REojvGkcsEPWk5Nm9V2HIVqb5Nkts'

#构建鉴权对象
q = Auth(access_key, secret_key)

#要上传的空间
bucket_name = 'ihome'

#上传到七牛后保存的文件名
key = 'iHome-logo2.png';

#生成上传 Token，可以指定过期时间等
token = q.upload_token(bucket_name, key, 3600)

file = open('/home/python/Documents/iHome/statics/imgs/logo.png', 'rb')
data = file.read()
#要上传文件的本地路径
# localfile = '/home/python/Documents/iHome/statics/imgs/logo.png'

ret, info = put_data(token, key, data)
print(info)
file.close()
# assert ret['key'] == key
# assert ret['hash'] == etag(localfile)




