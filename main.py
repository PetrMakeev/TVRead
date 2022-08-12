from operator import index
from striprtf.striprtf import rtf_to_text
import os
import pathlib


lst_rtf = []
lst_Ch = []
lst_Pr =[]
divH = 2

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

        # обрабатываем список 
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

                        if str_sub_line2.upper() in ['ПОНЕДЕЛЬНИК', 'ВТОРНИК', 'СРЕДА', 'ЧЕТВЕРГ', 'ПЯТНИЦА', 'СУББОТА', 'ВОСКРЕСЕНЬЕ'] :
                            name_Day = str_sub_line2.upper()
                        else:
                            name_Ch = str_sub_line2.split(' ', 1)[0]
                            if name_Ch not in lst_Ch: lst_Ch.append(name_Ch)
                            
                    else:
                        # отделяем время программы от названия программы
                        str_sub_lineD = str_line.split(' ')
                        str_sub_time = ''
                        # перебираем список время меняем и склеиваем в строку обратно
                        for str_time in str_sub_lineD:
                            if str_time[:2].isdigit():
                                str_sub_time = str_sub_time + ' ' + timeDiv(str_time) 
                            else:
                                str_sub_time = str_sub_time + ' ' + str_time
                        
                        # собираем список [канал, [программа]] переработать!!!
                        if str_sub_line1[0][:2].isdigit():
                            if name_Day == 'ПОНЕДЕЛЬНИК':
                                LProg1 = LProg1 + name_Day +'~' + name_Ch +'~' + str_sub_time + '\n'
                            elif name_Day == 'ВТОРНИК':
                                LProg2 = LProg2 + name_Day +'~' + name_Ch +'~' + str_sub_time + '\n'
                            elif name_Day == 'СРЕДА':
                                LProg3 = LProg3 + name_Day +'~' + name_Ch +'~' + str_sub_time + '\n'
                            elif name_Day == 'ЧЕТВЕРГ':
                                LProg4 = LProg4 + name_Day +'~' + name_Ch +'~' + str_sub_time + '\n'
                            elif name_Day == 'ПЯТНИЦА':
                                LProg5 = LProg5 + name_Day +'~' + name_Ch +'~' + str_sub_time + '\n'
                            elif name_Day == 'СУБЮОТА':
                                LProg6 = LProg6 + name_Day +'~' + name_Ch +'~' + str_sub_time + '\n'
                            if name_Day == 'ВОСКРЕСЕНЬЕ':
                                LProg7 = LProg7 + name_Day +'~' + name_Ch +'~' + str_sub_time + '\n'

    print(LProg1)
    print(LProg2)

def main():

    # определяем окружение
    path_prog = os.getcwd()

    # сделать запрос поправки на часовой пояс, по умолчанию поставить 2 часа
    #read_divH()
    

    # заполняем список сканируемых файлов каналов
    rtf_to_list(path_prog)

    # составляем список файлов каналов
    #scan_channel()

    # считываем программы по каналам
    rtf_to_prog(path_prog)

    
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


