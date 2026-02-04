from qiniu import Auth, put_data, put_file
import os
import uuid

from qiniu import Auth, put_file, etag,Auth, put_data, put_file
import qiniu.config
import os
import uuid

# 配置信息
access_key = 'tmoRxAnYOPtcI5k2_5qceLe4nX6-ABYW-PT1PaRj'
secret_key = 'k9-pw8JUBNCWQASOnG28trE7DdLhzlGM7DAmQRtT'
bucket_name = 'epilepsy-detect'
domain = 'http:st2f6c92m.hb-bkt.clouddn.com'

def upload_file(local_file):
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    
    # 生成随机文件名
    file_ext = os.path.splitext(local_file)[1]
    key = f"{str(uuid.uuid4())}{file_ext}"
    
    # 生成上传凭证
    token = q.upload_token(bucket_name, key, 3600)
    
    try:
        # 上传文件
        ret, info = put_file(token, key, local_file, version='v2')
        
        if info.status_code == 200:
            # 生成访问链接
            file_url = f"{domain}/{key}"
            print(file_url)
            return file_url
        else:
            print(f"上传失败: {info}")
    except Exception as e:
        print(f"上传出错: {str(e)}")

if __name__ == '__main__':
    local_file = 'E:/Code/medicine-care/EegFunc/miResult/mi_distribution.png'
    upload_file(local_file)
