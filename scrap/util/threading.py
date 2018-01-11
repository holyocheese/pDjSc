#-*- coding:utf-8 -*-
from contextlib import closing
from time import sleep
import requests
import sys
sys.path.append("..")
import scrap.src.ProcessBar as ProcessBar


# 下载文件（线程）显示进度条

@staticmethod
def downloadImg(object, src, filename, nsec, *session):
    """
        :param object: 对象
        :param src:
        :param filename:
        :param nsec: 睡眠秒数
        :param session :
        :return:"""
    print filename + "is downloading"
    filetype = src.split('.')[-1]
    # 进度条
    while 1:
        try:
            if not session:
                session = requests.session()
            with closing(session.get(src, headers=object.headers, stream=True)) as response:
                chunk_size = 128  # 单次请求最大值
                content_size = int(response.headers['content-length'])  # 内容体总大小
                progress = ProcessBar.ProgressBar(filename, total=content_size,
                                                  unit="KB", chunk_size=chunk_size, run_status="正在下载",
                                                  fin_status="下载完成")
                with open(filename + '.' + filetype, 'ab') as f:
                    for data in response.iter_content(chunk_size=chunk_size):
                        f.write(data)
                        progress.refresh(count=len(data))
            break
        except IOError as e:
            print "文件名错误："+e
            break
        except requests.ConnectionError as e:
            print e
            # 请求被拒绝 60秒后重试
            sleep(60)
            continue
    sleep(nsec)