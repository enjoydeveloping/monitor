#coding:gbk

import time
from scr import *


def main():
    config = load_config()
    path = config["path"]
    num = config["refresh"]
    cycle = config["cycle"]
    QJ = Function(path)
    QJ.call_cookie()
    while 1:
        N = period(cycle)
        print time.strftime("%H:%M")
        try:
            url_data = QJ._main_page_data
            QJ.query(url_data[0],url_data[1],QJ._form,QJ._header)
            QJ.main_page_handle()
            if QJ._modules:
                url_data = QJ._sec_page_data
                for name in QJ._modules:
                    QJ.query(url_data[name][0],url_data[name][1],None,QJ._header)
                    QJ.sec_page_handle(name)
                QJ.input_warn_unit(N)
            else:
                QJ._serious_unit = {"数据库":[],"应用":[],"机房":[],"网络":[],"主机":[],"Ping":[]}
        except urllib2.URLError:
            print "网络已断开"
            print '\07' * N
        time.sleep(num * 60)

if __name__ == "__main__":
    main()
