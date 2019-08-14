import requests

def getUrlResponeContent(url):
    data = requests.get(url)
    if data.status_code == 200:
        # response_data = data.text.encode("iso-8859-1").decode('gbk')
        # tmp_data = response_data[response_data.index('开奖号码：'):]
        # tmp_data_num_start = tmp_data.index('<ul')
        # tmp_data_num_end = tmp_data.index('</ul>')
        # tmp_data = tmp_data[tmp_data_num_start+4:tmp_data_num_end]
        # tmp_data = tmp_data.replace("<li class=\"ball_orange\">","").replace("</li>","").replace("\t","").replace("\n","").replace("\r","")
        response_data = data.text
        tmp_data = response_data[response_data.index('"ball-list red">')+16:]
        tmp_data = tmp_data[:tmp_data.index('</div>')]
        tmp_data = tmp_data.replace("<span class=\"ball-list red\"","").replace("</span>","").replace("\n","").replace("\r","").replace(">","").replace(" ","")
        return tmp_data
    elif data.status_code == 404:
        return "continue"
    else:
        print(url)
        return "continue"

# print(getUrlResponeContent('https://kjh.55128.cn/qxc-kjjg-2019090.htm'))