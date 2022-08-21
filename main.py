import datetime
import os
import pathlib
import copy
#from turtle import clear



lst_Ch = []
lst_Repl = []
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


# готовим список каналов и список замен
def txt_to_list_Ch(path_prog):

    global lst_txt
    global divH

    # создаем список файлов источников
    list_in = os.listdir(path_prog + '\\in')
    for name_files_in in list_in:
        if name_files_in[-3:]=='txt':
            lst_txt.append(path_prog + '\\in\\' + name_files_in)

    try:
        # считываем файл с телеканалами Chanenl.txt
        with open('Channel.txt', 'r') as file_r:
            str_txt_ch = file_r.readlines()
    except:
        # cправочник каналов Channel.txt недоступен
        print('Не найден файл со списком каналов!')
        exit()
    # заполняем справочник каналов 
    for el in str_txt_ch:
        if not (el[0] == '#' or el=='\n'):
            lst_Ch.append(el[:-1].split('|'))

    try:
        # считываем файл с заменами Replace.txt
        with open('Replace.txt', 'r') as file_r:
            str_txt_rpl = file_r.readlines()
    except:
        # cправочник каналов Replace.txt недоступен
        print('Не найден файл со списком каналов!')
        exit()

    # заполняем справочник замен 
    for el in str_txt_rpl:
        if not (el[0] == '#' or el=='\n'):
            lst_Repl.append(el[:-1].split('|'))



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

                
def replace_in_prog(str_prog):
    # меняем двойной апостроф на кавычки елочкой
    for i, str_sub in enumerate(str_prog):
        if str_sub == '"' :
            if i==0:
                # кавычка в начале строки
                str_prog = '«' + str_prog[1:]
            try:
                if str_prog[i-1] == ' ':
                    # кавычка перед словом
                    str_prog = str_prog[:i] + '«' + str_prog[i+1:]
            except:
                str_prog = str_prog[:i] + '«' + str_prog[i+1:]

            try:
                if str_prog[i+1] == ' ' or str_prog[i+1] == '.' :
                    # кавычка после слова
                    str_prog = str_prog[:i] + '»' + str_prog[i+1:]
            except:
                str_prog = str_prog[:i] + '»' + str_prog[i+1:]


            
        
    # делаем замены с перемещением согласно lst_Repl взятого из Replace.txt
    for el in lst_Repl:
        str_in = el[0]
        str_out = el[1]
        pos_repl = str_prog.upper().find(str_in.upper())
        if str_prog.upper().find(str_in.upper()) > -1 :
            str_prog = str_out + ' ' + str_prog.upper()[:pos_repl].strip() + ' ' + str_prog[pos_repl + len(str_in) :].strip()

        Rezult = str_prog
    return Rezult
 

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
                if len(el_D) > 1:
                    str_prog1 = str_prog1 + 'STYLE K ' + el_Pr.upper() + '\n'
                    str_progN =  str_progN + ' ' + el_Pr.upper() + '\n'
                else:
                    str_prog1 = str_prog1 + 'STYLE K ' + el_Pr.upper() + ' !!!! ПРОПУЩЕН !!!!' +  '\n'
                    str_progN =  str_progN + ' ' + el_Pr.upper() + ' !!!! ПРОПУЩЕН !!!!' +  '\n'
                   
            else:
                repl_str_prog = el_Pr.split('|',1)[0] + ', ' + replace_in_prog(el_Pr.split('|',1)[1]) 
                str_prog1 = str_prog1 +  repl_str_prog + '\n'
                str_progN = str_progN +  repl_str_prog + '\n'

    str_progN =  str_progN + '-------------------------------\n' + ' ВТОРНИК\n'
    str_prog2 = 'STYLE D \n'
    for el_D in lst_D2:
        # перебираем программы
        for i, el_Pr in enumerate(el_D):
            if i<1:
                if len(el_D) > 1:
                    str_prog2 = str_prog2 + 'STYLE K ' + el_Pr.upper() + '\n'
                    str_progN =  str_progN + ' ' + el_Pr.upper() + '\n'
                else:
                    str_prog2 = str_prog2 + 'STYLE K ' + el_Pr.upper() + ' !!!! ПРОПУЩЕН !!!!' +  '\n'
                    str_progN =  str_progN + ' ' + el_Pr.upper() + ' !!!! ПРОПУЩЕН !!!!' +  '\n'
                   
            else:
                repl_str_prog = el_Pr.split('|',1)[0] + ', ' + replace_in_prog(el_Pr.split('|',1)[1]) 
                str_prog2 = str_prog2 +  repl_str_prog + '\n'
                str_progN = str_progN +  repl_str_prog + '\n'

    str_progN = str_progN + '-------------------------------\n' + ' СРЕДА\n'
    str_prog3 = 'STYLE D \n'
    for el_D in lst_D3:
        # перебираем программы
        for i, el_Pr in enumerate(el_D):
            if i<1:
                if len(el_D) > 1:
                    str_prog3 = str_prog3 + 'STYLE K ' + el_Pr.upper() + '\n'
                    str_progN =  str_progN + ' ' + el_Pr.upper() + '\n'
                else:
                    str_prog3 = str_prog3 + 'STYLE K ' + el_Pr.upper() + ' !!!! ПРОПУЩЕН !!!!' +  '\n'
                    str_progN =  str_progN + ' ' + el_Pr.upper() + ' !!!! ПРОПУЩЕН !!!!' +  '\n'
                   
            else:
                repl_str_prog = el_Pr.split('|',1)[0] + ', ' + replace_in_prog(el_Pr.split('|',1)[1]) 
                str_prog3 = str_prog3 +  repl_str_prog + '\n'
                str_progN = str_progN +  repl_str_prog + '\n'

    str_progN = str_progN + '-------------------------------\n' + ' ЧЕТВЕРГ\n'
    str_prog4 = 'STYLE D \n'
    for el_D in lst_D4:
        # перебираем программы
        for i, el_Pr in enumerate(el_D):
            if i<1:
                if len(el_D) > 1:
                    str_prog4 = str_prog4 + 'STYLE K ' + el_Pr.upper() + '\n'
                    str_progN =  str_progN + ' ' + el_Pr.upper() + '\n'
                else:
                    str_prog4 = str_prog4 + 'STYLE K ' + el_Pr.upper() + ' !!!! ПРОПУЩЕН !!!!' +  '\n'
                    str_progN =  str_progN + ' ' + el_Pr.upper() + ' !!!! ПРОПУЩЕН !!!!' +  '\n'
                   
            else:
                repl_str_prog = el_Pr.split('|',1)[0] + ', ' + replace_in_prog(el_Pr.split('|',1)[1]) 
                str_prog4 = str_prog4 +  repl_str_prog + '\n'
                str_progN = str_progN +  repl_str_prog + '\n'

    str_progN = str_progN + '-------------------------------\n' + ' ПЯТНИЦА\n'
    str_prog5 = 'STYLE D \n'
    for el_D in lst_D5:
        # перебираем программы
        for i, el_Pr in enumerate(el_D):
            if i<1:
                if len(el_D) > 1:
                    str_prog5 = str_prog5 + 'STYLE K ' + el_Pr.upper() + '\n'
                    str_progN =  str_progN + ' ' + el_Pr.upper() + '\n'
                else:
                    str_prog5 = str_prog5 + 'STYLE K ' + el_Pr.upper() + ' !!!! ПРОПУЩЕН !!!!' +  '\n'
                    str_progN =  str_progN + ' ' + el_Pr.upper() + ' !!!! ПРОПУЩЕН !!!!' +  '\n'
                   
            else:
                repl_str_prog = el_Pr.split('|',1)[0] + ', ' + replace_in_prog(el_Pr.split('|',1)[1]) 
                str_prog5 = str_prog5 +  repl_str_prog + '\n'
                str_progN = str_progN +  repl_str_prog + '\n'

    str_progN = str_progN + '-------------------------------\n' + ' СУББОТА\n'
    str_prog6 = 'STYLE D \n'
    for el_D in lst_D6:
        # перебираем программы
        for i, el_Pr in enumerate(el_D):
            if i<1:
                if len(el_D) > 1:
                    str_prog6 = str_prog6 + 'STYLE K ' + el_Pr.upper() + '\n'
                    str_progN =  str_progN + ' ' + el_Pr.upper() + '\n'
                else:
                    str_prog6 = str_prog6 + 'STYLE K ' + el_Pr.upper() + ' !!!! ПРОПУЩЕН !!!!' +  '\n'
                    str_progN =  str_progN + ' ' + el_Pr.upper() + ' !!!! ПРОПУЩЕН !!!!' +  '\n'
                   
            else:
                repl_str_prog = el_Pr.split('|',1)[0] + ', ' + replace_in_prog(el_Pr.split('|',1)[1]) 
                str_prog6 = str_prog6 +  repl_str_prog + '\n'
                str_progN = str_progN +  repl_str_prog + '\n'

    str_progN = str_progN + '-------------------------------\n' + ' ВОСКРЕСЕНЬЕ\n'
    str_prog7 = 'STYLE D \n'
    for el_D in lst_D7:
        # перебираем программы
        for i, el_Pr in enumerate(el_D):
            if i<1:
                if len(el_D) > 1:
                    str_prog7 = str_prog7 + 'STYLE K ' + el_Pr.upper() + '\n'
                    str_progN =  str_progN + ' ' + el_Pr.upper() + '\n'
                else:
                    str_prog7 = str_prog7 + 'STYLE K ' + el_Pr.upper() + ' !!!! ПРОПУЩЕН !!!!' +  '\n'
                    str_progN =  str_progN + ' ' + el_Pr.upper() + ' !!!! ПРОПУЩЕН !!!!' +  '\n'
                   
            else:
                repl_str_prog = el_Pr.split('|',1)[0] + ', ' + replace_in_prog(el_Pr.split('|',1)[1]) 
                str_prog7 = str_prog7 +  repl_str_prog + '\n'
                str_progN = str_progN +  repl_str_prog + '\n'

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
    if datetime.date.today().month>8 and datetime.date.today().day>1: exit()

    # определяем окружение
    path_prog = os.getcwd()
    
    # сделать запрос поправки на часовой пояс, по умолчанию поставить 2 часа
    #read_divH()

   # заполняем список сканируемых файлов каналов
    txt_to_list_Ch(path_prog)

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


