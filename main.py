from operator import index
from striprtf.striprtf import rtf_to_text
import os
import pathlib


lst_rtf = []
lst_Ch = []
# lst_D1 =[]
# lst_D2 =[]
# lst_D3 =[]
# lst_D4 =[]
# lst_D5 =[]
# lst_D6 =[]
# lst_D7 =[]
divH = 2
list_week = ['ПОНЕДЕЛЬНИК', 'ВТОРНИК', 'СРЕДА', 'ЧЕТВЕРГ', 'ПЯТНИЦА', 'СУББОТА', 'ВОСКРЕСЕНЬЕ']

LProg1 = ''
LProg2 = ''
LProg3 = ''
LProg4 = ''
LProg5 = ''
LProg6 = ''
LProg7 = ''

# поправка на часовой пояс
def timeDiv(strTime):
    strHourN = int(strTime.split('.')[0]) + divH
    if strHourN>23 : strHourN = strHourN - 24
    if strHourN<0  : strHourN = 24 - strHourN 
    if strHourN<10:
        Rezult = '0' + str(strHourN) + strTime[2:]
    else:
        Rezult = str(strHourN) + strTime[2:]
    return Rezult


def rtf_to_list(path_prog):
    # перебираем файлы rtf в папке in и составляем список файлов источников
    list_in = os.listdir(path_prog + '\\in')
    for name_files_in in list_in:
        lst_rtf.append(path_prog + '\\in\\' + name_files_in)


# def scan_channel():
#     # сканируем источники и формируем список каналов
#     for name_files in lst_rtf:
#         print(name_files)


def rtf_to_Channel(path_prog):
    # считываем rtf в список
    
    # сканируем файлы rtf и формируем списки каналов и программ
    for name_files in lst_rtf:
        # открываем файлы rtf построчно сохраняем в список
        with open(name_files) as infile:
            content = infile.read()
        rtftext = rtf_to_text(content)
        str_rtf = rtftext.splitlines()
        
        # обрабатываем список с программой из файла источника 
        for str_line in str_rtf:
            # делим строку на две части по пробелу
            str_sub_line = str_line.rstrip().split(' ', 2)

            # пропускаем пустые строки
            if len(str_sub_line)>1:
                str_sub_line1 = str_sub_line[0] 
                str_sub_line2 = str_sub_line[1]
                
                # пропускаем прочерки
                if str_sub_line2.find('---')<0 :         

                    # выбираем название канала 
                    if str_sub_line[0] == '':

                        # пропускаем дни недели
                        if not str_sub_line2.upper() in list_week :
                            str_sub_lineCh = str_line.strip().split(' ')
                            name_Ch = ''
                            for str_ch in str_sub_lineCh:
                                if not str_ch[0]=='!':
                                    name_Ch = name_Ch + ' ' + str_ch
                            if name_Ch.strip() not in lst_Ch: lst_Ch.append(name_Ch.strip())

def fill_Day():        
    # готовим заготовки списков программ по дням недели
    global lst_D1
    global lst_D2
    global lst_D3
    global lst_D4
    global lst_D5
    global lst_D6
    global lst_D7

    lst_D1 = [['~']]
    for el in lst_Ch:
        lst_D1.append([el])
    lst_D1.remove(['~'])
    lst_D2 = [['~']]
    for el in lst_Ch:
        lst_D2.append([el])
    lst_D2.remove(['~'])
    lst_D3 = [['~']]
    for el in lst_Ch:
        lst_D3.append([el])
    lst_D3.remove(['~'])
    lst_D4 = [['~']]
    for el in lst_Ch:
        lst_D4.append([el])
    lst_D4.remove(['~'])
    lst_D5 = [['~']]
    for el in lst_Ch:
        lst_D5.append([el])
    lst_D5.remove(['~'])
    lst_D6 = [['~']]
    for el in lst_Ch:
        lst_D6.append([el])
    lst_D6.remove(['~'])
    lst_D7 = [['~']]
    for el in lst_Ch:
        lst_D7.append([el])
    lst_D7.remove(['~'])  



def rtf_to_prog(path_prog):
    # считываем rtf в список
    
    # сканируем файлы rtf и формируем списки каналов и программ
    for name_files in lst_rtf:
        # открываем файлы rtf построчно сохраняем в список
        with open(name_files) as infile:
            content = infile.read()
        rtftext = rtf_to_text(content)
        str_rtf = rtftext.splitlines()
        
        # устанавливаем первый день недели, канал, программу
        name_Day = 'ПОНЕДЕЛЬНИК'
        name_Ch = ''
        name_Pr = ''
     
        # обрабатываем список с программой из файла источника 
        for str_line in str_rtf:
            # делим строку на две части по пробелу
            str_sub_line = str_line.rstrip().split(' ', 2)

            # пропускаем пустые строки
            if len(str_sub_line)>1:
                str_sub_line1 = str_sub_line[0] 
                str_sub_line2 = str_sub_line[1]
                
                # пропускаем прочерки
                if str_sub_line2.find('---')<0 :         

                    # выбираем название канала и дни недели
                    if str_sub_line[0] == '':

                        if str_sub_line2.upper() in list_week :
                            name_Day = str_sub_line2.upper()
                        else:
                            str_sub_lineCh = str_line.strip().split(' ')
                            name_Ch = ''
                            for str_ch in str_sub_lineCh:
                                if not str_ch[0]=='!':
                                    name_Ch = name_Ch + ' ' + str_ch

                            
                    else:
                        # отделяем время программы от названия программы
                        str_sub_lineD = str_line.split(' ')
                        name_Pr = ''
                        # перебираем список времени начала программы, меняем согласно часовому поясу и склеиваем в строку обратно
                        for str_time in str_sub_lineD:
                            if not str_time[:2].isdigit():
                                name_Pr = name_Pr + ' ' + str_time
                            elif len(str_time)<5:
                                name_Pr = name_Pr + ' ' + str_time
                            elif not str_time[2]=='.':
                                name_Pr = name_Pr + ' ' + str_time
                            else:
                                name_Pr = name_Pr + ' ' + timeDiv(str_time) 
                                                          
                        
                        # собираем список [канал, [программа]] переработать!!!
                        if str_sub_line1[0][:2].isdigit():

                            if name_Day == 'ПОНЕДЕЛЬНИК':
                                lst_D1[lst_Ch.index(name_Ch.strip())].append(name_Pr.strip())                            

                            elif name_Day == 'ВТОРНИК':
                                lst_D2[lst_Ch.index(name_Ch.strip())].append(name_Pr.strip())

                            elif name_Day == 'СРЕДА':
                                lst_D3[lst_Ch.index(name_Ch.strip())].append(name_Pr.strip())

                            elif name_Day == 'ЧЕТВЕРГ':
                                lst_D4[lst_Ch.index(name_Ch.strip())].append(name_Pr.strip())

                            elif name_Day == 'ПЯТНИЦА':
                                lst_D5[lst_Ch.index(name_Ch.strip())].append(name_Pr.strip())

                            elif name_Day == 'СУБЮОТА':
                                lst_D6[lst_Ch.index(name_Ch.strip())].append(name_Pr.strip())

                            if name_Day == 'ВОСКРЕСЕНЬЕ':
                                lst_D7[lst_Ch.index(name_Ch.strip())].append(name_Pr.strip())
    

def main():

    # определяем окружение
    path_prog = os.getcwd()
    
    # заполняем список сканируемых файлов каналов
    rtf_to_list(path_prog)

    # считываем каналы 
    rtf_to_Channel(path_prog)

    # !!!!! запрос сортировки каналов

    # создаем заготовки списков программ по дням
    fill_Day()

    # считываем программы 
    rtf_to_prog(path_prog)

    # сделать запрос поправки на часовой пояс, по умолчанию поставить 2 часа
    #read_divH()
    
    # print(lst_rtf)

    # считываем файл с программой ТВ

        # # считываем названия и порядок каналов
        # try:
        #     with open("Channel.txt", "r", encoding='utf-8') as file:  # file = open("myfile.txt")
        #         Channel_Name = file.readlines()
        # except FileNotFoundError:
        #     print("Невозможно открыть файл Canal.txt")


# точка входа.
if __name__ == '__main__':
    main()


