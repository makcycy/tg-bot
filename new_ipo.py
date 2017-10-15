import telegram
from time import sleep
from urllib.request import urlopen, Request
import re
import datetime as dt

URL = "https://www.etnet.com.hk/www/tc/stocks/ci_ipo.php"
req = Request(URL,headers={'User-Agent': 'Mozilla/5.0'})
web = urlopen(req).read().decode('utf-8')
def get_code_name():
    stock = re.findall(r'<td><a(.*?)</a></td>', web)
    code = []
    name = []
    for ind in range(len(stock)):
        if ind%2== 0:
            try:
                code.append(stock[ind].split('&type=listeing">')[1])
            except IndexError:
                pass
        else:
            try:
                name.append(stock[ind].split('"font-family:Arial">')[1])
            except IndexError:
                pass
    name = name[:len(code)]
    dictionary = dict(zip(code,name))
    for key in dictionary.keys():
        dictionary[key] = [dictionary[key]]
    return dictionary
def get_rest_info():
    date = re.findall(r'<td align="right">(.*?)</td>', web)
    return date

def combined_all(code_name, rest_info):
    key_ind = 1
    for ind in range(3, len(rest_info)):
        try:
            if ind == (6 * key_ind - 3):
                key = list(code_name.keys())[key_ind - 1]
                code_name[key].append(rest_info[ind])
                key_ind += 1
            else:
                code_name[key].append(rest_info[ind])
        except IndexError:
            break
    useful_info = {}
    for name in code_name.keys():
        deadline = dt.datetime.strptime(code_name[name][1], '%Y/%m/%d').date()
        if deadline >= dt.date.today():
            useful_info[name] = code_name[name]
    return useful_info

def getmessage():
    code_name = get_code_name()
    rest_info = get_rest_info()
    useful_info = combined_all(code_name=code_name, rest_info=rest_info)
    msg = ''
    for name_no in useful_info.keys():
        msg += '代號: ' + name_no+ '\n''\
''名稱: ' +  str(useful_info[name_no][0]) +'\n''\
''截止認購日: ' + str(useful_info[name_no][1]) + '\n''\
''上市日期: ' + str(useful_info[name_no][2]) +'\n''\
''發售價: ' + str(useful_info[name_no][3]) + '\n''\
''上市價: ' + str(useful_info[name_no][4]) + '\n''\
''每手股數: ' + str(useful_info[name_no][5]) + '\n''\
''入場費: ' + str(useful_info[name_no][6]) +'\n''\
'
    return msg



if __name__ == '__main__':
    getmessage()
