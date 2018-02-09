#coding:gbk

import time,json,urllib,urllib2,cookielib,threading

class Main_Page_Data:
    _main_page_data = ("http://56.1.88.88:8088/Query/monitormain.do","http://56.1.88.88:8088/Query/","主页")

class Sec_Page_Data:
    _sec_page_data = {
        "数据库":("http://56.1.88.88:8088/Query/treeManage.do?method=getmonitorWarn&mainid=4&showindex=1&status=2","http://56.1.88.88:8088/Query/monitormain.do?method=queryTreeWarn&mainid=4&showindex=1&status=2"),
        "应用":("http://56.1.88.88:8088/Query/treeManage.do?method=getmonitorWarn&mainid=8&showindex=1&status=2","http://56.1.88.88:8088/Query/monitormain.do?method=queryTreeWarn&mainid=8&showindex=1&status=2"),
        "机房":("http://56.1.88.88:8088/Query/treeManage.do?method=getmonitorWarn&mainid=7&showindex=1&status=2","http://56.1.88.88:8088/Query/monitormain.do?method=queryTreeWarn&mainid=7&showindex=1&status=2"),
        "网络":("http://56.1.88.88:8088/Query/treeManage.do?method=getmonitorWarn&mainid=2&showindex=1&status=2","http://56.1.88.88:8088/Query/monitormain.do?method=queryTreeWarn&mainid=2&showindex=1&status=2"),
        "主机":("http://56.1.88.88:8088/Query/treeManage.do?method=getmonitorWarn&mainid=1&showindex=1&status=2","http://56.1.88.88:8088/Query/monitormain.do?method=queryTreeWarn&mainid=1&showindex=1&status=2"),
        "ping":("http://56.1.88.88:8088/Query/treeManage.do?method=getmonitorWarn&mainid=11&showindex=1&status=2","http://56.1.88.88:8088/Query/monitormain.do?method=queryTreeWarn&mainid=11&showindex=1&status=2")
}

class Request_Data:
    _header = {
    "Accept":"application/x-ms-application, image/jpeg, application/xaml+xml, image/gif, image/pjpeg, application/x-ms-xbap, */*",
    "User-Agent":"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Content-Type":"application/x-www-form-urlencoded",
    "Accept-Encoding":" gzip, deflate",
    "Host": "56.1.88.88:8088",
    "Connection": "Keep-Alive",
    }

    _form = urllib.urlencode({"method":"toAddMain","usercode":"monitor","password":"monitor"})

    def call_cookie(self):
        cookie = cookielib.MozillaCookieJar()
        cookie.load(self._path+"cookie.txt",ignore_discard=True,ignore_expires=True)
        self._opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

class Function(Main_Page_Data,Sec_Page_Data,Request_Data):
    _page_src = None
    _switch = 0
    _modules = []
    _serious_unit = {"数据库":[],"应用":[],"机房":[],"网络":[],"主机":[],"ping":[]}
    def __init__(self,path):
        self._path = path
        thread = threading.Thread(target=self.on_off)
        thread.start()

    def on_off(self):
        while 1:
            st = raw_input()
            if st == "turn off":
                self._switch = 0
                print "告警声音已经关闭"

    def query(self,url,referer,form,header):
        request = urllib2.Request(url,form,header)
        request.add_header("Referer",referer)
        response = self._opener.open(request)
        self._page_src = response.read().replace("\n","").replace("\r","").replace("\t","")
    
    def main_page_handle(self):
	self._modules = []
        const = 180
        colour = "#FF0033"
        serious = "严重"
        try:
            for name in self._sec_page_data:
                place_1 = self._page_src.index(name)
                seek = place_1 - const
                colour_str = self._page_src[seek:seek+100]
                if colour_str.find(colour) != -1:
                    seek = place_1 + 1100
                    serious_str = self._page_src[seek:seek+1500]
                    place_2 = serious_str.find(serious)
                    count = serious_str[place_2+6:place_2+7]
                    self._modules.append(name)
                    print "%-8s: %s个严重告警" %(name,count)
                else:
                    print "%-8s:   normal" %name
            print "*----------------------------*"
        except ValueError:
            print (name+"没找到关键字")

    def sec_page_handle(self,name):
        s_place = 0
        e_place = 0
        description = []
        while 1:
            try:
                s_place = self._page_src.index("d.add",s_place+1)
                e_place = self._page_src.index(';',s_place)
                text = self._page_src[s_place:e_place+1]
                description.append(text)
            except ValueError:
                break
            if description:
                for unit in description:
                    if unit not in self._serious_unit[name]:
                        self._switch = 1
                        break
        self._serious_unit[name] = description

    def input_warn_unit(n):
        for name in self._serious_unit:
            if name in self._modules:
                print "**"+name+"模块以下单元出现严重告警**"
                L = len(self._serious_unit[name])
                for i in range(1,L):
                    print '\n=>  '+self._serious_unit[name][i]
                print "* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *"
        if self._switch:
            print '\07'*n

def load_config():
    with open("config.json",'r') as fp:
        data = json.loads(fp.read())
    return data

def period(cycle):
    now_time = time.localtime(time.time())[3]
    if now_time >07 and now_time <22:
        n = cycle[0]
    else:
        n = cycle[1]
    return n

