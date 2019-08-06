
rfilename = '../data/getresult.csv'
wfilename = '../data/getresult.csv'
qijianshu=10
tw_num = '08'

def init_dict():
    tw_dict={}
    for i in range(0,10):
        for k in range(0,10):
            tw_dict[str(i)+str(k)]=0
    return tw_dict

def tw_count(data_list):
    tw_dict = init_dict()
    for tw in data_list:
        if tw_dict[tw] > 0:
            tw_dict[tw] += 1
        else:
            tw_dict[tw] = 1
    return tw_dict

##################
import csv
import sys
import get_data_from_net as g

#获取当前本地数据，返回data，数据结果形如：['19089', '1234567']
def read_from_csv_data_all(fileName):
    data = []
    result_data = []
    try:
        with open(fileName) as f:
            reader = csv.reader(f)
            # header = next(reader)
            data = [row for row in reader]
    except csv.Error as e:
        print('Error reading CSV file at line %s:%s',reader.line_num,e)
        sys.exit(-1)
    return data

#读取csv文件,返回数据结果如：['19089', '53']
def reader_csv_base_tw(filename,start_num=0,end_num=0):
    result_data = []
    data = read_from_csv_data_all(filename)
    # data = read_from_csv(filename)

    count = 0
    for datarow in data:
        if start_num > count:
            count += 1
            continue
        elif end_num < count and end_num != 0:
            break
        result_data_num = str.split(datarow[0],' ')
        result_data_value = str.split(datarow[1][0:4:3],' ')
        result_data.append(result_data_num+result_data_value)
        count += 1
    return result_data

#切片转字符串
def listToString(str_content):
    result_data = "".join(str_content).replace('\t','')
    return result_data

#获取当前本地数据最新期数数
def getLatest(fileName):
    result_data = []
    data = read_from_csv_data_all(fileName)
    count = 1
    for datarow in data:
        if count > 1:
            break
        result_data.append(listToString(datarow)[:-7])
        count+=1
    return round(float(result_data[0]))

#取tw数,end为距今的期数，如：10，则表示最近的10期tw
def twFromData(str_content,end):
    count = 1
    tw_result = []
    for datarow in str_content:
        if count > end and end > 0:
            break
        # result_data = datarow[5] + datarow[8]
        result_data = datarow[:]
        tw_result.append(result_data)
        count+=1
    return tw_result

#将字符串写入csv文件
def write_to_csv(filename,content):
    if len(content)==0 or contain_english(content):
        return
    try:
        with open(filename,'r+') as f:
            old = f.read()
            f.seek(0)
            f.write(content+'\n')
            f.write(old)
            # writeCSV = f.write(content+'\n')
            # writeCSV.writerow(content)
    except csv.Error as e:
        print('Error Write CSV %s',e)
        sys.exit(-1)

def write_csv_from_net(wfilename,start_num,end_num):
    #1.先判断wfilename文件是否存在，若不存在，则新建
    file_status = IsNotExistFile(wfilename)
    #file_status为true，表示文件已存在，则需获取本地文件里面的数据
    if file_status:
        latest_num = getLatest(wfilename)
        #end_num比latest_num大，表示有服务器有新的数据
        if end_num > latest_num and latest_num > 0:
            start_num = latest_num
        else:
            return
    for i in range(end_num,start_num,-1):
        print(start_num)
        url = ""
        if i<10000:
            url = '0'+ str(i)
        else:
            url = str(i)
        content = g.getUrlResponeContent("http://kaijiang.500.com/shtml/qxc/" + url + ".shtml")
        if content == "continue":
            continue
        content = url + "," + content
        print(content)
        write_to_csv(wfilename,content)
# data_analy(filename)
# twFromData(data)
##################

#########################
import os
import operator

def IsNotExistFile(fileName):
    return os.access(fileName, os.F_OK)

def tw_sort(tw_dict):
    return sorted(tw_dict.items(),key=operator.itemgetter(1),reverse=True)
#########################

###############################
import re

def contain_english(content):
    return bool(re.search('[a-zA-Z]', content))

#当期期数开tw，则为0;skip参数为匹配次数,加入传1，则表示匹配一次后，继续往后匹配
def getNumFromTw(tw="00",skip=0):
    count = 0
    tw_result = []
    str_content = read_from_csv_data_all(rfilename)
    if len(str_content) <= 0:
        return
    for datarow in str_content:
        # result_data = list(set(datarow[0]).intersection(set(datarow[1])))
        # result_data_num = str.split(datarow[0],' ')
        result_data_num = datarow[0]
        result_data = datarow[1][0:4:3]
        if tw == result_data and skip == 0:
            return result_data_num,count
        elif skip > 0:
            count+=1
            skip -= 1
            continue
    #     result = result_data_num + result_data
    #     tw_result.append(result)
        count+=1
    # return tw_result

###############################
###############################
#最大漏开
def max_omission(tw,str_content=[]):
    count = 0
    tw_result = []
    # str_content = reader_csv_base_tw(rfilename)
    if len(str_content) <= 0:
        return
    tmp_num = ''
    tmp_count = 0
    for datarow in str_content:
        result_data_num = datarow[0]
        result_data = datarow[1]

        #匹配
        if tw == result_data:
            if count > tmp_count:
                tmp_count = count
                count = 0
            tmp_num = result_data_num
            # tmp_count = count
        else:
            count+=1
    if len(tmp_num) == 0:
        return  '该tw在指定期间内，尚未开出'
    return tmp_num,tmp_count
        #     result = result_data_num + result_data
        #     tw_result.append(result)
###############################
###############################

#############################
#############################
#最大连开
def max_output(tw,str_content=[]):
    count = 0
    tw_result = []
    # str_content = reader_csv_base_tw(rfilename)
    if len(str_content) <= 0:
        return
    result_num = ''
    out_count_previous = 0
    out_count_previous_num = 0
    count_num_flag = 0
    for datarow in str_content:
        result_data_num = datarow[0]
        result_data = datarow[1]
        #匹配
        if tw == result_data:
            count += 1
            if count == 1:
                out_count_ttmp = result_data_num
            if count > out_count_previous:
               count_num_flag += 1
               out_count_previous = count
            #最大连开第一次开奖的期数
            if count_num_flag == 1:
               result_num = out_count_ttmp
        else:
            #不匹配，则把刚刚匹配的最大次数保存下来
            if(count >= out_count_previous):
                out_count_previous = count
            count = 0
            count_num_flag = 0
    if len(result_num) == 0:
        return  '该tw在指定期间内，尚未开出'
    return result_num,out_count_previous
    #     result = result_data_num + result_data
    #     tw_result.append(result)
###############################
###############################

#1.先获取本地最新期数，然后判断是否继续向服务器请求新的数据
#2.如果有新的数据，则在第一行插入新数据
# mycsv.write_csv_from_net(wfilename,4100,19090)

#获取本地现有的第一行数据
# result = mycsv.getLatest(rfilename)

#最近N期的tw数
bt_result = twFromData(reader_csv_base_tw(rfilename), qijianshu)
print(bt_result)

#对最近N期tw数进行统计次数，并排序
# print(tw_sort(tw_count(bt_result)))

#通过tw，查询最近开的期数
# for tw_num in  bt_result:
#     print(getNumFromTw(tw_num))

#
# print(getNumFromTw("53",1))

#最大漏开
str_content = reader_csv_base_tw(rfilename)
# print(max_omission('69',str_content))

#最大连开
# print(max_output('11',str_content))
#从本地文件中读取期数及其对应tw数
# print(len(reader_csv_base(rfilename,0,20)))

# mycsv.write_to_csv(wfilename,"123")
# print(content)

# read_from_csv_data_all(rfilename)
# reader_csv_base_tw(rfilename)