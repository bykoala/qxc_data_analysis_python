import csv
import sys

filename = 'data/person_data.csv'
#获取当前本地数据，返回data，数据结果形如：['19089', '1234567']
def read_from_person_data(fileName,tagName):
    try:
        with open(fileName) as f:
            reader = csv.reader(f)
            for row in reader:
                row = "".join(row)
                row_list = row.split(":")
                if row_list[0] == tagName:
                    return row_list[1]

    except csv.Error as e:
        print('Error reading CSV file at line %s:%s',reader.line_num,e)
        sys.exit(-1)
    return

ts = read_from_person_data(filename,'ts').split(";")
ws = read_from_person_data(filename,'ws').split(";")
hs = read_from_person_data(filename,'hs').split(";")
gl = read_from_person_data(filename,'gl').split(";")
zs = read_from_person_data(filename,'zs').split(";")

def calc_result(gl_or_zs,hs,ts,ws):
    hs_result = []
    ts_result = []
    ws_result = []
    ts_ws_result = []
    ts_hs_result = []
    ws_hs_result = []
    all_result = []
    #如果gl_or_zs为0，则只计算gl中的数据
    if gl_or_zs == 0:
        gl_or_zs = gl
    for i in gl_or_zs:
        i = list(i)
        #只计算头数
        if ts != 0:
            for t in ts:
                if t == i[0]:
                    ts_result.append(i)

        if hs != 0:
            ts_join = int(i[0])+int(i[1])
            if ts_join >= 10:
                ts_join = ts_join % 10
            for h in hs:
                if int(h) == ts_join:
                    hs_result.append(i)
        if ws != 0:
            for w in ws:
                if w == i[0]:
                    ws_result.append(i)
#只有合数hs
    if ts == 0 and ws == 0 and hs != 0:
        print("组数:" + str(len(hs_result)))
        return hs_result
#只有头尾tw
    if ts !=0 and hs == 0 and ws == 0:
        print("组数:" + str(len(ts_result)))
        return ts_result
#只有尾数ws
    if ts == 0 and hs == 0 and ws != 0:
        print("组数:" + str(len(ws_result)))
        return ws_result
#有合数和头数，没有尾数
    if hs != 0 and ts != 0:
        for t in ts_result:
            tw_join = int(t[0])+int(t[1])
            if tw_join >= 10:
                tw_join = tw_join % 10
            for h in hs:
                if int(h) == tw_join:
                    ts_hs_result.append(t)
        if ws == 0:
            print("组数:" + str(len(ts_hs_result)))
            return ts_hs_result
#有合数和尾数，没有头数
    if hs != 0 and ws !=0:
        for w in ws_result:
            ws_join = int(w[0])+int(w[1])
            if ws_join >= 10:
                ws_join = ws_join % 10
            for h in hs:
                if int(h) == ws_join:
                    ws_hs_result.append(w)
        if ts == 0:
            print("组数："+ str(len(ws_hs_result)))
            return ws_hs_result

#有头数和尾数，没有合数
    if ts != 0 and ws !=0:
        for w in ws_result:
            for t in ts:
                if int(t) == int(w[0]):
                    ts_ws_result.append(w)
        if hs == 0:
            print("组数:" + str(len(ts_ws_result)))
            return ts_ws_result

#有合数、尾数及头数
    if hs != 0 and ts != 0 and ws !=0:
        for tw in ts_ws_result:
            tw_ws_join = int(tw[0])+int(tw[1])
            if tw_ws_join >= 10:
                tw_ws_join = tw_ws_join % 10
            for h in hs:
                if int(h) == tw_ws_join:
                    all_result.append(tw)
        print("组数:" + str(len(all_result)))
        return all_result

#结果以友好的方式展示
def showResultToString(list):
    str_result = ""
    count = 0
    for i in list:
        if len(list)-1 != count:
            str_result += str(i[0])+ str(i[1]) + ","
        else:
            str_result += str(i[0])+ str(i[1])
        count += 1
    print(str_result)

#calc_result函数调用说明:第一个参数0表示gl，否则传zs。第二个为合数hs，第三个为头尾tw，第四个为尾数ws,某个数若无值，则传0
# print(calc_result(gl,hs,tw,ws))
showResultToString(calc_result(gl,hs,ts,ws))
