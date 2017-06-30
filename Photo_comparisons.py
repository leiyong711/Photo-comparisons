# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: Photo-comparisons
# author: "Lei Yong" 
# creation time: 2017/6/30 0030 23:02
# Email: leiyong711@163.com

import time
import json
import urllib2
import cv2

data = []
img_info = []


# 调用电脑摄像头拍照
def take_pictures(filename):
    cap = cv2.VideoCapture()
    ret, frame = cap.read()
    cv2.imwrite(filename, frame)  # picture.jpg


# 对比截图与旧图
def contrast(filename1, filename2):
    # 请求地址
    url = 'https://api-cn.faceplusplus.com/facepp/v3/compare'
    # 公钥
    key = "m_JZUUs-CzSzKsaqZa_TOAD7PMl4tv6r"
    # 密钥
    secret = "SqeJQDQ_ZBpKKwxJUEgpq0fv-FY6OS6N"
    # 参数协议分割标识
    boundary = '-%s' % hex(int(time.time() * 1000))

    # 制作协议包
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_key')
    data.append(key)
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_secret')
    data.append(secret)
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"; filename="%s"' % ('image_file1', filename1))
    data.append('Content-Type: %s\r\n' % 'application/octet-stream')
    data.append(open(filename1, 'rb').read())
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"; filename="%s"' % ('image_file2', filename2))
    data.append('Content-Type: %s\r\n' % 'application/octet-stream')
    data.append(open(filename2, 'rb').read())
    data.append('--%s--\r\n' % boundary)

    # Post请求
    http_body = '\r\n'.join(data)
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
    req.add_data(http_body)
    resp = urllib2.urlopen(req, timeout=5)
    # 返回结果
    qrcont = resp.read()
    ps = json.loads(qrcont)
    # print ps
    img_info1 = u'照片1：\n   人脸标识：%s\n   左上角纵坐标：%s\n   左上角横坐标：%s\n   宽度：%s\n   高度：%s\n'\
                % (ps['faces1'][0]['face_token'], ps['faces1'][0]['face_rectangle']['top'],
                   ps['faces1'][0]['face_rectangle']['left'],
                   ps['faces1'][0]['face_rectangle']['width'], ps['faces1'][0]['face_rectangle']['height'])

    img_info2 = u'照片2：\n   人脸标识：%s\n   左上角纵坐标：%s\n   左上角横坐标：%s\n   宽度：%s\n   高度：%s\n'\
                % (ps['faces2'][0]['face_token'], ps['faces1'][0]['face_rectangle']['top'],
                   ps['faces2'][0]['face_rectangle']['left'],
                   ps['faces2'][0]['face_rectangle']['width'], ps['faces1'][0]['face_rectangle']['height'])

    result = '两图对比相似度：%s' % ps['confidence']
    img_info.append(img_info1)
    img_info.append(img_info2)
    img_info.append(result)
    return img_info

if __name__ == '__main__':
    take_pictures('picture.jpg')  # 拍摄照片
    time.sleep(2)   # 延时等待2秒存储截图
    info = contrast('picture.jpg', '2.jpg')
    for i in range(len(info)):  # 遍历对比结果数据
        print info[i]
