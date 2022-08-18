import datetime
import os
import pathlib
import copy
from turtle import clear


lst_Ch = []
lst_txt = []
divH = 2
list_week = ['ПОНЕДЕЛЬНИК', 'ВТОРНИК', 'СРЕДА', 'ЧЕТВЕРГ', 'ПЯТНИЦА', 'СУББОТА', 'ВОСКРЕСЕНЬЕ']


def id_to_name_Ch(name_Ch_id):
    for el in lst_Ch:
        if el[0]==name_Ch_id: 
            Rezult = el[1]
            break
        else:
            Rezult = name_Ch_id
    return Rezult


def set_scr():
    #подготовка экрана
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Парсер для обработки программ телеканалов ')
    print('Макеев Петр тел. 8-912-34-161-34 ')
    print('-----------------------------------------------')
 

# поправка на часовой пояс
def timeDiv(strTime):
    if ':' in strTime:
        strHourN = int(strTime.split(':')[0]) + divH
    else:
        strHourN = int(strTime.split('.')[0]) + divH
    if strHourN>23 : strHourN = strHourN - 24
    if strHourN<0  : strHourN = 24 - strHourN 
    if strHourN<10:
        Rezult = '0' + str(strHourN) + '.' + strTime[-2:]
    else:
        Rezult = str(strHourN) + '.' + strTime[-2:]
    return Rezult


# готовим список каналов
def txt_to_list(path_prog):
    # создаем список файлов источников
    global lst_txt
    global divH

    list_in = os.listdir(path_prog + '\\in')
    for name_files_in in list_in:
        if name_files_in[-3:]=='txt':
            lst_txt.append(path_prog + '\\in\\' + name_files_in)
    
    # составляем словарь каналов
    for name_files in lst_txt:
        name_ch_files = os.path.basename(name_files)
        name_ch = name_ch_files[:name_ch_files.index('.')]
        lst_Ch.append([name_ch,name_ch])

    # открываем сохраненный словарь каналов
    fl_ch = True
    try:
        # считываем справочник каналов Chanenl.txt
        with open('Channel.txt', 'r') as file_r:
            str_txt_ch = file_r.readlines()
        for i, el in enumerate(str_txt_ch):
            str_txt_ch[i]=el[:-1]
    except:
        # cправочник каналов Channel.txt недоступен
        fl_ch =False
    if not fl_ch:
        # сливаем список каналов в справочник каналов в Channel.txt
        str_ch=''
        for el in lst_Ch:
            str_ch += ( el[0]+ '|' + el[1] + '\n')
        try:
            with open('Channel.txt', 'w') as file_w:
                file_w.writelines(str_ch)
        except:
            print('Файл Channel.txt заблокирован для вывода списка каналов!')            
    else:
        # формируем список справочника каналов 
        for str_line_ch in str_txt_ch:
            str_sub_line = str_line_ch.rstrip().split('|')
            # сверяем названия каналов из импортируемых файлов со справочником в Channel.txt
            for i, el in enumerate(lst_Ch):
                if el[0] == str_sub_line[0]:
                    lst_Ch[i][1] = str_sub_line[1]

    # выводим телеканаля и запрашиваем действия
    Loop_list_Ch = True
    while Loop_list_Ch:
        set_scr()
        # выводим список на экран для проверки названий и порядка 
        #print('----------------------------')
        print('  №  |  Название телеканала ' +  ' |  Время: Мск + ' + str(divH) +' ч ')
        print('-----------------------------------------------')
        for i, el in enumerate(lst_Ch,1):
            print(str(i).center(5) + '|  ' + el[1])
        print('-----------------------------------------------')
        print('Работа со списком телеканалов:')
        print('<0> - продолжить обработку')
        print('<1> - переименовать телеканал')
        print('<2> - поменять место телеканала в списке')
        print('<3> - изменить часовой пояс')

        # выбираем действие
        Loop_action_Ch = True
        while Loop_action_Ch:
            try:
                mode_lst1 = (input('Выберите действие <0>'))
                if len(mode_lst1) == 0:
                    mode_lst = 0
                else:
                    mode_lst = int(mode_lst1)

            # Если полученный ввод не число, будет вызвано исключение
            except ValueError:
                # Цикл будет повторяться до правильного ввода
                print("Это не число, попробуйте снова.")
            else:
                if mode_lst>-1 and mode_lst<4:
                    # выход из цикла выбора действия
                    Loop_action_Ch = False
        
        # продолжаем обработку телеканалов
        if mode_lst == 0:  
            Loop_list_Ch = False

        # переименовка телеканала
        if mode_lst == 1:
            loop_sel_channel = True
            while loop_sel_channel:
                try:
                    id_channel = int(input('Укажите номер телеканала, для переименования <1 - '+str(len(lst_Ch)) + '>: '))
                # Если полученный ввод не число, будет вызвано исключение
                except ValueError:
                    # Цикл будет повторяться до правильного ввода
                    print("Это не число, попробуйте снова.")
                if id_channel>0 and id_channel<len(lst_Ch)+1: 
                     loop_sel_channel = False
                else:
                    print('Вы указали неверный номер телеканала')
            # указываем новое имя телеканала
            loop_rename_chanel = True
            while loop_rename_chanel:
                rename_channel = (input('Укажите новое название телеканала <' + lst_Ch[id_channel-1][1] + '>: '))
                if len(rename_channel) == 0:
                    rename_channel = lst_Ch[id_channel-1][1]
                    loop_rename_chanel = False
            # print('Переименовываем телеканал')
            lst_Ch[id_channel-1][1] = rename_channel

        # изменение порядка телеканалов
        if mode_lst == 2:
            loop_sel_id = True
            while loop_sel_id:
                try:
                    id1_channel = int(input('Укажите номер телеканала, для перемещения в списке <1 - '+str(len(lst_Ch)) + ': '))
                # Если полученный ввод не число, будет вызвано исключение
                except ValueError:
                    # Цикл будет повторяться до правильного ввода
                    print("Это не число, попробуйте снова.")
                if id1_channel>0 and id1_channel<len(lst_Ch)+1:
                    loop_sel_id = False
            loop_sel_pos = True
            while loop_sel_pos:
                try:
                    id2_channel = int(input('Укажите на какое место переместить телеканал <' + lst_Ch[id1_channel-1][1] + '> в списке <1 - '+str(len(lst_Ch)) + ': '))
                # Если полученный ввод не число, будет вызвано исключение
                except ValueError:
                    # Цикл будет повторяться до правильного ввода
                    print("Это не число, попробуйте снова.")
                if id2_channel>0 and id2_channel<len(lst_Ch)+1:
                    loop_sel_pos = False
            # если номера разные меняем места                    
            if id1_channel!=id2_channel:
                # print('Меняем место')
                lst_Ch.insert(id2_channel-1, lst_Ch.pop(id1_channel-1))

        # меняем часовой пояс
        if mode_lst == 3:
            loop_sel_H = True
            while loop_sel_H:
                try:
                    divH_tmp = input('Укажите укажите сдвиг программ в часах (от -1 до 9) <2>:')
                    if len(divH_tmp) == 0:
                        divH = 2
                    else:
                        divH = int(divH_tmp)

                # Если полученный ввод не число, будет вызвано исключение
                except ValueError:
                    # Цикл будет повторяться до правильного ввода
                    print("Это не число, попробуйте снова.")
                if divH>-2 and divH<10:
                    loop_sel_H = False     
            

    # редактирование закончено сливаем откорректированный список телеканалов в Channel.txt
    # сливаем  справочник каналов в Channel.txt
    str_ch=''
    for el in lst_Ch:
        str_ch = str_ch + ( el[0]+ '|' + el[1] + '\n')
    try:
        with open('Channel.txt', 'w') as file_w:
            file_w.writelines(str_ch)
    except:
        print('Файл Channel.txt заблокирован для вывода списка каналов!')            
            


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
        lst_D1.append([el[1]])
    lst_D1.remove(['~'])
    lst_D2 = [['~']]
    for el in lst_Ch:
        lst_D2.append([el[1]])
    lst_D2.remove(['~'])
    lst_D3 = [['~']]
    for el in lst_Ch:
        lst_D3.append([el[1]])
    lst_D3.remove(['~'])
    lst_D4 = [['~']]
    for el in lst_Ch:
        lst_D4.append([el[1]])
    lst_D4.remove(['~'])
    lst_D5 = [['~']]
    for el in lst_Ch:
        lst_D5.append([el[1]])
    lst_D5.remove(['~'])
    lst_D6 = [['~']]
    for el in lst_Ch:
        lst_D6.append([el[1]])
    lst_D6.remove(['~'])
    lst_D7 = [['~']]
    for el in lst_Ch:
        lst_D7.append([el[1]])
    lst_D7.remove(['~'])  



def txt_to_prog(path_prog):
    # сканируем файлы txt и формируем  программы
    for name_files in lst_txt:
        # открываем файлы txt построчно сохраняем в список
        with open(name_files, 'r') as file_r:
            str_txt = file_r.readlines()
            
        # устанавливаем первый день недели, канал, программу
        name_Day = 'None'
        name_Ch_id = os.path.basename(name_files).split('.')[0]
        name_Ch = id_to_name_Ch(name_Ch_id)


        name_Pr = ''
    
        # обрабатываем список с программой из файла источника 
        for str_line in str_txt:
            # проверяем первый знак 
            str_tmp = str_line[:-1].strip()
            # и пустые строки
            if len(str_tmp)<3: continue
 
            str_sub_lineD = str_tmp.split(',',2)
            if str_sub_lineD[0].upper() in list_week:
                # в строке день недели
                name_Day = str_sub_lineD[0].upper()
            else:
                # в строке программа
                # отделяем время программы от названия программы
                if len(str_sub_lineD)>0:
                    str_sub_lineD = str_tmp.split(' ',1)

                    if str_sub_lineD[0][0].isalpha() or name_Pr=='None':
                        fl_merge = True
                    else:
                        fl_merge = False
                        
                    if fl_merge:
                        name_Pr = name_Pr + ' ' + str_tmp
                    else:
                        name_Pr = timeDiv(str_sub_lineD[0]) + '|' + str_sub_lineD[1] 
    
                    # собираем список [канал, [программа]] 
                    if name_Day == 'ПОНЕДЕЛЬНИК':
                        for i, el in enumerate(lst_Ch):
                            if el[1]==name_Ch:
                                if fl_merge:
                                    lst_D1[i][-1] = lst_D1[i][-1] + ' ' + str_tmp
                                else:
                                    lst_D1[i].append(name_Pr.strip())                            

                    elif name_Day == 'ВТОРНИК':
                        for i, el in enumerate(lst_Ch):
                            if el[1]==name_Ch:
                                if fl_merge:
                                    lst_D2[i][-1] = lst_D2[i][-1] + ' ' + str_tmp
                                else:
                                    lst_D2[i].append(name_Pr.strip())                            

                    elif name_Day == 'СРЕДА':
                        for i, el in enumerate(lst_Ch):
                            if el[1]==name_Ch:
                                if fl_merge:
                                    lst_D3[i][-1] = lst_D3[i][-1] + ' ' + str_tmp
                                else:
                                    lst_D3[i].append(name_Pr.strip())                            

                    elif name_Day == 'ЧЕТВЕРГ':
                        for i, el in enumerate(lst_Ch):
                            if el[1]==name_Ch:
                                if fl_merge:
                                    lst_D4[i][-1] = lst_D4[i][-1] + ' ' + str_tmp
                                else:
                                    lst_D4[i].append(name_Pr.strip())                            

                    elif name_Day == 'ПЯТНИЦА':
                         for i, el in enumerate(lst_Ch):
                            if el[1]==name_Ch:
                                if fl_merge:
                                    lst_D5[i][-1] = lst_D5[i][-1] + ' ' + str_tmp
                                else:
                                    lst_D5[i].append(name_Pr.strip())                            

                    elif name_Day == 'СУББОТА':
                        for i, el in enumerate(lst_Ch):
                            if el[1]==name_Ch:
                                if fl_merge:
                                    lst_D6[i][-1] = lst_D6[i][-1] + ' ' + str_tmp
                                else:
                                    lst_D6[i].append(name_Pr.strip())                            

                    elif name_Day == 'ВОСКРЕСЕНЬЕ':
                        for i, el in enumerate(lst_Ch):
                            if el[1]==name_Ch:
                                if fl_merge:
                                    lst_D7[i][-1] = lst_D7[i][-1] + ' ' + str_tmp
                                else:
                                    lst_D7[i].append(name_Pr.strip())                            

                

 
def exp_prog(path_prog): 
    # формируем данные для записи в файл
    str_prog1=''
    str_prog2=''
    str_prog3=''
    str_prog4=''
    str_prog5=''
    str_prog6=''
    str_prog7=''
    str_progN=''
    
    # понедельник
    # перебираем каналы
    str_progN = '-------------------------------\n' + ' ПОНЕДЕЛЬНИК\n'
    str_prog1 = 'STYLE D \n'
    for el_D in lst_D1:
        # перебираем программы
        for i, el_Pr in enumerate(el_D):
            if i<1:
                str_prog1 = str_prog1 + 'STYLE K ' + el_Pr.upper() + '\n'
                str_progN =  str_progN + ' ' + el_Pr.upper() + '\n'
            else:
                str_prog1 = str_prog1 +  el_Pr.replace('|',' ', 1) + '\n'
                str_progN = str_progN +  el_Pr.replace('|',' ', 1) + '\n'

    str_progN = '-------------------------------\n' + ' ВТОРНИК\n'
    str_prog2 = 'STYLE D \n'
    for el_D in lst_D2:
        # перебираем программы
        for i, el_Pr in enumerate(el_D):
            if i<1:
                str_prog2 = str_prog2 + 'STYLE K ' + el_Pr.upper() + '\n'
                str_progN =  str_progN + ' ' + el_Pr.upper() + '\n'
            else:
                str_prog2 = str_prog2 +  el_Pr.replace('|',' ', 1) + '\n'
                str_progN = str_progN +  el_Pr.replace('|',' ', 1) + '\n'

    str_progN = '-------------------------------\n' + ' СРЕДА\n'
    str_prog3 = 'STYLE D \n'
    for el_D in lst_D3:
        # перебираем программы
        for i, el_Pr in enumerate(el_D):
            if i<1:
                str_prog3 = str_prog3 + 'STYLE K ' + el_Pr.upper() + '\n'
                str_progN =  str_progN + ' ' + el_Pr.upper() + '\n'
            else:
                str_prog3 = str_prog3 +  el_Pr.replace('|',' ', 1) + '\n'
                str_progN = str_progN +  el_Pr.replace('|',' ', 1) + '\n'

    str_progN = '-------------------------------\n' + ' ЧЕТВЕРГ\n'
    str_prog4 = 'STYLE D \n'
    for el_D in lst_D4:
        # перебираем программы
        for i, el_Pr in enumerate(el_D):
            if i<1:
                str_prog4 = str_prog4 + 'STYLE K ' + el_Pr.upper() + '\n'
                str_progN =  str_progN + ' ' + el_Pr.upper() + '\n'
            else:
                str_prog4 = str_prog4 +  el_Pr.replace('|',' ', 1) + '\n'
                str_progN = str_progN +  el_Pr.replace('|',' ', 1) + '\n'

    str_progN = '-------------------------------\n' + ' ПЯТНИЦА\n'
    str_prog5 = 'STYLE D \n'
    for el_D in lst_D5:
        # перебираем программы
        for i, el_Pr in enumerate(el_D):
            if i<1:
                str_prog5 = str_prog5 + 'STYLE K ' + el_Pr.upper() + '\n'
                str_progN =  str_progN + ' ' + el_Pr.upper() + '\n'
            else:
                str_prog5 = str_prog5 +  el_Pr.replace('|',' ', 1) + '\n'
                str_progN = str_progN +  el_Pr.replace('|',' ', 1) + '\n'

    str_progN = '-------------------------------\n' + ' СУББОТА\n'
    str_prog6 = 'STYLE D \n'
    for el_D in lst_D6:
        # перебираем программы
        for i, el_Pr in enumerate(el_D):
            if i<1:
                str_prog6 = str_prog6 + 'STYLE K ' + el_Pr.upper() + '\n'
                str_progN =  str_progN + ' ' + el_Pr.upper() + '\n'
            else:
                str_prog6 = str_prog6 +  el_Pr.replace('|',' ', 1) + '\n'
                str_progN = str_progN +  el_Pr.replace('|',' ', 1) + '\n'

    str_progN = '-------------------------------\n' + ' ВТОРНИК\n'
    str_prog7 = 'STYLE D \n'
    for el_D in lst_D7:
        # перебираем программы
        for i, el_Pr in enumerate(el_D):
            if i<1:
                str_prog7 = str_prog7 + 'STYLE K ' + el_Pr.upper() + '\n'
                str_progN =  str_progN + ' ' + el_Pr.upper() + '\n'
            else:
                str_prog7 = str_prog7 +  el_Pr.replace('|',' ', 1) + '\n'
                str_progN = str_progN +  el_Pr.replace('|',' ', 1) + '\n'

    # сохраняем данные 
    try:
        with open(path_prog +'\\OUT\\REZULT.REZ', 'w') as file_w:
            file_w.writelines(str_progN)
    except:
        print('Файл REZULT.REZ заблокирован для вывода списка каналов!')            

    try:
        with open(path_prog +'\\OUT\\1.REZ', 'w') as file_w:
            file_w.writelines(str_prog1)
    except:
        print('Файл 1.REZ заблокирован для вывода списка каналов!')            

    try:
        with open(path_prog +'\\OUT\\2.REZ', 'w') as file_w:
            file_w.writelines(str_prog2)
    except:
        print('Файл 2.REZ заблокирован для вывода списка каналов!')   

    try:
        with open(path_prog +'\\OUT\\3.REZ', 'w') as file_w:
            file_w.writelines(str_prog3)
    except:
        print('Файл 3.REZ заблокирован для вывода списка каналов!')    
               
    try:
        with open(path_prog +'\\OUT\\4.REZ', 'w') as file_w:
            file_w.writelines(str_prog4)
    except:
        print('Файл 4.REZ заблокирован для вывода списка каналов!')    

    try:
        with open(path_prog +'\\OUT\\5.REZ', 'w') as file_w:
            file_w.writelines(str_prog5)
    except:
        print('Файл 5.REZ заблокирован для вывода списка каналов!')  

    try:
        with open(path_prog +'\\OUT\\6.REZ', 'w') as file_w:
            file_w.writelines(str_prog6)
    except:
        print('Файл 6.REZ заблокирован для вывода списка каналов!')   

    try:
        with open(path_prog +'\\OUT\\7.REZ', 'w') as file_w:
            file_w.writelines(str_prog7)
    except:
        print('Файл 7.REZ заблокирован для вывода списка каналов!')            
 
       
def del_dubl_prog():
    
    # перебираем программы понедельника
    for k, el_prog in enumerate(lst_D1):
        for i, el in enumerate(el_prog):
            if i>0:
                lst_el = el.split('|',1)[1]
                for j, el_seek in enumerate(el_prog):
                    if j>i:
                        lst_el_seek = el_seek.split('|',1)[1]
                        if lst_el==lst_el_seek:
                            # найден дубль в j для i
                            lst_D1[k][i] = lst_D1[k][i].split("|")[0] + ' ' + lst_D1[k][j].split('|')[0] + '|' + lst_D1[k][i].split("|")[1]
                            del lst_D1[k][j]

            
    

# основное тело программы
def main():

    # проверяем дату
    if datetime.date.today().month>7 and datetime.date.today().day>26: exit()

    # определяем окружение
    path_prog = os.getcwd()
    
    # сделать запрос поправки на часовой пояс, по умолчанию поставить 2 часа
    #read_divH()

   # заполняем список сканируемых файлов каналов
    txt_to_list(path_prog)

    # создаем заготовки списков программ по дням
    fill_Day()

    # считываем каналы 
    txt_to_prog(path_prog)

    # сводим дубликаты программ в одну строку
    del_dubl_prog()

     # сохраняем программы в файлы
    exp_prog(path_prog)


    # print('w')   


# точка входа.
if __name__ == '__main__':
    main()


