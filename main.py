import os
import pathlib
import copy
from turtle import clear


lst_Ch = []
lst_txt = []
divH = 2
list_week = ['ПОНЕДЕЛЬНИК', 'ВТОРНИК', 'СРЕДА', 'ЧЕТВЕРГ', 'ПЯТНИЦА', 'СУББОТА', 'ВОСКРЕСЕНЬЕ']



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


def txt_to_list(path_prog):
    # создаем список файлов источников
    global lst_txt
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
        # выводим список на экран для проверки названий и порядка 
        print('----------------------------')
        print('  №  |  Название телеканала ')
        print('----------------------------')
        for i, el in enumerate(lst_Ch,1):
            print(str(i).center(5) + '|  ' + el[1])
        print('----------------------------')
        print('Работа со списком телеканалов:')
        print('<0> - продолжить обработку')
        print('<1> - переименовать телеканал')
        print('<2> - поменять место телеканала в списке')

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
                print("Error! Это не число, попробуйте снова.")
            else:
                if mode_lst>-1 and mode_lst<3:
                    Loop_action_Ch = False
        
        # продолжаем обработку телеканалов
        if mode_lst == 0:  
            Loop_list_Ch = False
        
        

    

    

    




def txt_to_Channel(path_prog):
    # считываем txt в список
    
    # сканируем файлы txt и формируем списки каналов и программ
    for name_files in lst_txt:
        # открываем файлы txt построчно сохраняем в список
        with open(name_files, 'r') as file_r:
            str_txt = file_r.readlines()
        
        # обрабатываем список с программой из файла источника 
        #for str_line in str_txt:
            # если строка начинается с цифры то это программа, если с буквы то день недели
        
        
        
        
        # for str_line in str_txt:
        #     # делим строку на две части по пробелу
        #     str_sub_line = str_line.rstrip().split(' ', 2)



        #     # пропускаем пустые строки
        #     if len(str_sub_line)>1:
        #         str_sub_line1 = str_sub_line[0] 
        #         str_sub_line2 = str_sub_line[1]
                
        #         # пропускаем прочерки
        #         if str_sub_line2.find('---')<0 :         

        #             # выбираем название канала 
        #             if str_sub_line[0] == '':

        #                 # пропускаем дни недели
        #                 if not str_sub_line2.upper() in list_week :
        #                     str_sub_lineCh = str_line.strip().split(' ')
        #                     name_Ch = ''
        #                     for str_ch in str_sub_lineCh:
        #                         if not str_ch[0]=='!':
        #                             name_Ch = name_Ch + ' ' + str_ch
        #                     if name_Ch.strip() not in lst_Ch: lst_Ch.append(name_Ch.strip())
        
    # запрашиваем сортировку каналов
    # print('Обработаны следующие телеканалы:\n')
    # npp = 1
    # for el in lst_Ch:
    #     if npp>9:
    #         print('< '+ str(npp) +' > - ' + el)
    #     else:
    #         print('<  '+ str(npp) +' > - ' + el)
    #     npp += 1

    # # сливаем перечень каналов в Channel.txt
    # try:
    #     with open('Channel.txt', 'w', encoding='utf-8') as file_w:
    #         file_w.writelines(name_Ch)
    # except:
    #     print('Файл Channel.txt заблокирован для вывода списка каналов!')
    
    
        



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



def txt_to_prog(path_prog):
    # считываем txt в список
    
    # сканируем файлы txt и формируем списки каналов и программ
    for name_files in lst_txt:
        # открываем файлы txt построчно сохраняем в список
        with open(name_files, 'w', encoding='utf-8') as file_r:
            str_txt = file_r.readlines()
        
        # устанавливаем первый день недели, канал, программу
        name_Day = 'ПОНЕДЕЛЬНИК'
        name_Ch = ''
        name_Pr = ''
     
        # обрабатываем список с программой из файла источника 
        for str_line in str_txt:
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
    

# основное тело программы
def main():

    #подготовка экрана
    clear
    print('Программа для обработки программы телеканалов ')
    print('---------------------------------------------')

    # определяем окружение
    path_prog = os.getcwd()
    
   # заполняем список сканируемых файлов каналов
    txt_to_list(path_prog)

    # считываем каналы 
    txt_to_Channel(path_prog)


 
    # сделать запрос поправки на часовой пояс, по умолчанию поставить 2 часа
    #read_divH()



    # создаем заготовки списков программ по дням
    # fill_Day()

    # считываем программы 
    # txt_to_prog(path_prog)
 
   


# точка входа.
if __name__ == '__main__':
    main()


