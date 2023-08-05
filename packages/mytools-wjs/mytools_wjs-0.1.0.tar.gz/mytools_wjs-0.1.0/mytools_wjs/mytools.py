"""mytools.py - Tools for working with functions and callable objects
"""

################################################################################
### expansion() and expansion_up() function
################################################################################
__all__ = ["expansion", "expansion_up", "mapping_yq", "mapping_NumberToChinese", "secondsT0format", "timestampTotime"]

import time


def expansion_up(array: list or tuple) -> list:
    """
    生成器实现列表扁平化方法，提升性能，适合大并多维度的列表操作
    :param array: 多维数据
    :return: 返回多维列表展开后的一维列表
    """

    def flatten(items: list):
        """
        扁平操作， 通过生成器让递归调用编程普通调用
        :param items: ...
        """
        for item in items:
            if type(item) is list or type(item) is tuple:
                yield from flatten(item)
            else:
                yield item

    return [fla for fla in flatten(array)]


def expansion(array: list or tuple, result: list or tuple = None) -> list:
    """
    递归实现列表扁平化方法， 调用栈过多可能造成程序性能下降
    :param array:  多维列表
    :param result:  默认参数， 一般不用传
    :return: 返回多维列表展开后的一维列表， 若传入参数 result， 则返回  一维array + result
    """
    if result is None:
        result = []
    for arr in array:
        if type(arr) is list or type(arr) is tuple:
            expansion(arr, result)
        else:
            result.append(arr)
    return result


def mapping_yq(abt: int or str) -> str:
    """
    任意长度映射 例 1->① 123->①②③
    :param abt: 传入要映射的参数
    :return: 返回映射后的字符串
    """
    try:
        mapping = {
            '0': '⓪',
            '1': '①',
            '2': '②',
            '3': '③',
            '4': '④',
            '5': '⑤',
            '6': '⑥',
            '7': '⑦',
            '8': '⑧',
            '9': '⑨',
            '10': '⑩'
        }
        abt = str(abt)
        if abt == '10':
            return mapping[abt]
        result = ''
        while len(abt) > 0:
            one = abt[0]
            result += mapping[one]
            abt = abt[1:]
        return result
    except:
        return "传入字符中可能包含非数字字符！"


def mapping_NumberToChinese(number: int or float, mode: str = 'J', length: int = 3) -> str:
    """
    数字转大写
    :param length: 若选择模式为 ’M‘ 此参数有效, 控制小数点后数据精度, 默认为3, 最大为3, 代表数据精度为小数点后三位
    :param mode: 模式， J -> 简体; F -> 繁体; M -> 金额转换; 默认简体
    :param number: 传入需要转换的数字
    :return: 返回转换后的字符串
    """
    if len(str(int(number))) > 20 or length > 3:
        print('数据超出范围!')
        return 'error'

    if mode == 'F' or mode == 'M':
        mapping_J = {
            '0': '零',
            '1': '壹',
            '2': '贰',
            '3': '叁',
            '4': '肆',
            '5': '伍',
            '6': '陆',
            '7': '柒',
            '8': '捌',
            '9': '玖',
        }
        mapping_D = ['仟', '佰', '拾', '']
        mapping_DD = ['', '万', '亿', '兆', '京', '垓']
        if mode == 'F':
            if type(number) != int:
                number = int(number)
        else:
            number_M = float(number)
            number = int(number)
            mapping_M = ['角', '分', '厘']
    else:
        if type(number) != int:
            number = int(number)
        mapping_J = {
            '0': '零',
            '1': '一',
            '2': '二',
            '3': '三',
            '4': '四',
            '5': '五',
            '6': '六',
            '7': '七',
            '8': '八',
            '9': '九',
        }
        mapping_D = ['千', '百', '十', '']
        mapping_DD = ['', '万', '亿', '兆', '京', '垓']

    def yingshe(string: str):
        """
        ---
        :param string: ---
        :return:  ---
        """
        temp = ''
        if len(string) == 4:
            if string[0: 3] == '000' and string[3] != '0':
                return '零' + mapping_J[string[3]]
            elif string[0: 2] == '00' and string[2] != '' and string[3] != '0':
                return '零' + mapping_J[string[2]] + '十' + mapping_J[string[3]]
            elif (string[0] != '0' and string[1] == '0') and string[2] != '0':
                if string[3] != '0':
                    return mapping_J[string[0]] + '千' + '零' + mapping_J[string[2]] + '十' + mapping_J[string[3]]
                else:
                    return mapping_J[string[0]] + '千' + '零' + mapping_J[string[2]] + '十'
            elif string[1: 3] == '00' and string[0] != '0' and string[3] != '0':
                return mapping_J[string[0]] + '千' + '零' + mapping_J[string[3]]
            elif string[2] == '0' and string[0] != '0' and string[1] != '0' and string[3] != '0':
                return mapping_J[string[0]] + '千' + mapping_J[string[1]] + '百' + '零' + mapping_J[string[3]]
            elif string[0] == '0' and string[1] != '0' and string[2] != '0' and string[3] != 0:
                return '零' + mapping_J[string[1]] + '百' + mapping_J[string[2]] + '十' + mapping_J[string[3]]
            elif string[0] == '0' and string[2] == '0' and string[1] != '0' and string[3] != '0':
                return '零' + mapping_J[string[1]] + '百零' + mapping_J[string[3]]
            else:
                ind = 4 - len(string)
                for s in string:
                    if s != '0':
                        temp += mapping_J[s] + mapping_D[ind]
                    ind += 1
                return temp
        else:
            ind = 4 - len(string)
            for s in string:
                temp += mapping_J[s]
                if s != '0':
                    temp += mapping_D[ind]
                ind += 1
            if temp[-1] == '零':
                temp = temp.replace('零', '')
            return temp

    temp_num = ''
    i = 1
    for n in str(number)[::-1]:
        temp_num += n
        if i % 4 == 0:
            temp_num += ','
        i += 1
    first_list = [i for i in temp_num[::-1].split(',') if i != '']
    last_list = []
    for first in first_list:
        last_list.append(yingshe(first))
    last_list.reverse()
    first_list.clear()
    index = 0
    temp_list = []
    FLAG = True
    for last in last_list:
        if last == '' and FLAG:
            FLAG = False
        else:
            temp_list.append(last)
            FLAG = True
    for last in temp_list:
        if last != '':
            last += mapping_DD[index]
        else:
            last += '零'
        index += 1
        first_list.append(last)
    first_list.reverse()
    result = ""
    for res in first_list:
        result += res
    if result == '一十':
        return '十'

    if mode == 'M' and 0 <= length <= 3:
        if length == 0:
            return result + '元整'
        tail = str(str(number_M).split('.')[1])[0: length]
        for _ in range(length - len(tail)):
            tail += '0'
        if length == 1:
            if tail == '0':
                return result + "元整"
            else:
                return result + "元" + mapping_J[tail] + "角"
        elif length == 2:
            if tail[0] == '0' and tail[1] != '0':
                return result + "元" + mapping_J[tail[1]] + '分'
            elif tail[0] != '0' and tail[1] == '0':
                return result + "元" + mapping_J[tail[0]] + '角'
            elif tail == '00':
                return result + "元整"
            else:
                return result + "元" + mapping_J[tail[0]] + '角' + mapping_J[tail[1]] + '分'
        else:
            if tail == '000':
                return result + "元整"
            elif tail[0: 2] == '00' and tail[2] != '0':
                return result + '元' + mapping_J[tail[2]] + '厘'
            elif tail[0] == '0' and tail[2] == '0' and tail[1] != '0':
                return result + '元' + mapping_J[tail[1]] + '分'
            elif tail[0] != '0' and tail[1] == '0' and tail[2] == '0':
                return result + '元' + mapping_J[tail[0]] + '角'
            elif tail[0] == '0' and tail[1] != '0' and tail[2] != '0':
                return result + '元' + mapping_J[tail[1]] + '分' + mapping_J[tail[2]] + '厘'
            elif tail[0] != '0' and tail[1] != '0' and tail[2] == '0':
                return result + '元' + mapping_J[tail[0]] + '角' + mapping_J[tail[1]] + '分'
            elif tail[0] != '0' and tail[1] == '0' and tail[2] != '0':
                return result + '元' + mapping_J[tail[0]] + '角' + mapping_J[tail[2]] + '厘'
            else:
                return result + '元' + mapping_J[tail[0]] + '角' + mapping_J[tail[1]] + '分' + mapping_J[tail[2]] + '厘'

    return result


def secondsT0format(seconds: int, mode: str = 'H', beautify: bool = True) -> str:
    """
    秒转时间
    @param beautify: 是否美化， 默认True, demo: 3600秒 -> 1小时
    @param mode: H -> 中文格式输出 S -> 英文格式输出
    @param seconds: 传入需要格式化的时间（单位：秒） int 型
    """

    def function1(num: int, dividend: int = 60):
        """
        ---
        @param dividend: ---
        @param num: ---
        """
        return int(num / dividend), num % dividend

    if mode == 'S':
        mapping = ['d', 'h:', 'm:', 's', '', '']
        beautify = False
    else:
        mapping = ['天', '时', '分', '秒', '小时', '分钟']

    if seconds > 60:
        minutes, sec = function1(seconds)
        if minutes >= 60:
            if minutes == 60 and sec == 0 and beautify:
                return f'1{mapping[4]}'
            else:
                hour, minutes = function1(minutes)
                if hour > 24:
                    day, hour = function1(hour, 24)
                    return f'{day}{mapping[0]}/{hour}{mapping[1]}{minutes}{mapping[2]}{sec}{mapping[3]}'
                else:
                    if hour == 24 and minutes == 0 and sec == 0 and beautify:
                        return f'24{mapping[4]}'
                    else:
                        return f'{hour}{mapping[1]}{minutes}{mapping[2]}{sec}{mapping[3]}'
        else:
            return f'{minutes}{mapping[2]}{sec}{mapping[3]}'
    else:
        if seconds == 60 and beautify:
            return f'1{mapping[5]}'
        else:
            return f'{seconds}{mapping[3]}'


def timestampTotime(stamp: int, mode: str = '%Y-%m-%d %H:%M:%S', strict: bool = True) -> str:
    """
    时间戳转时间
    :param strict: 严格模式： True严格, False 通配, 主要控制 stamp 传入的格式和位数, 如果为通配模式，当传入的参数格式和位数不为10位int型时会自动处理
    :param stamp: 传入需要转换的时间戳
    :param mode: 输出的时间格式
    :return: 成功返回格式化后的时间，出现错误返回error
    """
    if strict:
        if len(str(stamp)) != 10:
            print('stamp 必须为10位int型！')
            return 'error'
    else:
        if len(str(stamp)) > 10:
            stamp = int(str(stamp)[0: 10])
        elif len(str(stamp)) < 10:
            stamp = str(stamp)
            for _ in range(10-len(stamp)):
                stamp += '0'
            stamp = int(stamp)
    try:
        otherStyleTime = time.strftime(mode, time.localtime(stamp))
    except Exception as e:
        print("可能mode 参数格式错误！" + str(e.args))
        return "error"
    return otherStyleTime

