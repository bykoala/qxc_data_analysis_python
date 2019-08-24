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
                if row.__contains__(tagName):
                    return row

    except csv.Error as e:
        print('Error reading CSV file at line %s:%s',reader.line_num,e)
        sys.exit(-1)
    return

tw = read_from_person_data(filename,'tw').split(":")[1].split(";")
ws = read_from_person_data(filename,'ws').split(":")[1].split(";")
hs = read_from_person_data(filename,'hs').split(":")[1].split(";")
gl = read_from_person_data(filename,'gl').split(":")[1].split(";")
zs = read_from_person_data(filename,'zs').split(":")[1].split(";")

def calc_result(gl_or_zs,hs,tw,ws):
    hs_result = []
    tw_result = []
    ws_result = []
    tw_ws_result = []
    tw_hs_result = []
    ws_hs_result = []
    all_result = []
    #如果gl_or_zs为0，则只计算gl中的数据
    if gl_or_zs == 0:
        gl_or_zs = gl
    for i in gl_or_zs:
        i = list(i)
        #如果hs合数为0，表示只计算头尾数
        if tw != 0:
            for t in tw:
                if t == i[0]:
                    tw_result.append(i)

        if hs != 0:
            tw_join = int(i[0])+int(i[1])
            for h in hs:
                if int(h) == tw_join:
                    hs_result.append(i)
        if ws != 0:
            for w in ws:
                if w == i[0]:
                    ws_result.append(i)
#只有合数hs
    if tw == 0 and ws == 0 and hs != 0:
        print("组数:" + str(len(hs_result)))
        return hs_result
#只有头尾tw
    if tw !=0 and hs == 0 and ws == 0:
        print("组数:" + str(len(tw_result)))
        return tw_result
#只有尾数ws
    if tw == 0 and hs == 0 and ws != 0:
        print("组数:" + str(len(ws_result)))
        return ws_result
#有合数和头尾，没有尾数
    if hs != 0 and tw != 0:
        for t in tw_result:
            tw_join = int(t[0])+int(t[1])
            for h in hs:
                if int(h) == tw_join:
                    tw_hs_result.append(t)
        print("组数:" + str(len(tw_hs_result)))
        return tw_hs_result
#有合数和尾数，没有头数
    if hs != 0 and tw == 0 and ws !=0:
        for w in ws_result:
            ws_join = int(w[0])+int(w[1])
            for h in hs:
                if int(h) == ws_join:
                    ws_hs_result.append(w)
        print("组数："+ str(len(ws_hs_result)))
        return ws_hs_result

#有头数和尾数，没有合数
    if hs == 0 and tw != 0 and ws !=0:
        for w in ws_result:
            for t in tw:
                if int(t) == int(w[0]):
                    tw_ws_result.append(w)
        print("组数:" + str(len(tw_ws_result)))
        return tw_ws_result

#有合数、尾数及头数
    if hs != 0 and tw != 0 and ws !=0:
        for tw in tw_ws_result:
            tw_ws_join = int(tw[0])+int(tw[1])
            for h in hs:
                if int(h) == tw_ws_join:
                    all_result.append(tw)
        print("组数:" + str(len(all_result)))
        return all_result
#calc_result函数调用说明:第一个参数0表示gl，否则传zs。第二个为合数hs，第三个为头尾tw，第四个为尾数ws,某个数若无值，则传0
print(calc_result(gl,0,tw,ws))
'''
def init_list():
    count = 0
    tw = ""
    for i in range(0,10):
        for k in range(0,10):
            tw += str(i)+str(k) + ";"
    return tw

print(init_list())
'''