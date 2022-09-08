import datetime
from gettext import find
from operator import truediv
import os
from time import strptime
from docx import Document
from docx.shared import Pt
from docx.shared import Mm


lst_Ch = []
lst_Repl = []
lst_Remove = []
lst_CapsWord = []
lst_StopWord = []
lst_txt = []
divH = 2
list_week = ['ПОНЕДЕЛЬНИК', 'ВТОРНИК', 'СРЕДА', 'ЧЕТВЕРГ', 'ПЯТНИЦА', 'СУББОТА', 'ВОСКРЕСЕНЬЕ']

vozrast = []
for i in range(0,20):
    vozrast.extend([' ' + str(i) + '+', '(' + str(i) + '+'])

god_film = []
for i in range(1900,2050):
    god_film.append(str(i))


doc1 = Document()
doc2 = Document()
doc3 = Document()
doc4 = Document()
doc5 = Document()
doc6 = Document()
doc7 = Document()
docN = Document()

# возвращаем название канала по имени файла
def id_to_name_Ch(name_Ch_id):
    for el in lst_Ch:
        if el[0]==name_Ch_id: 
            Rezult = el[1]
            break
        else:
            Rezult = name_Ch_id
    return Rezult

# возращаем надо делать корректировку времени или нет
def fl_to_name_Ch(name_Ch_id):
    Rezult = False
    for el in lst_Ch:
        if el[0]==name_Ch_id: 
            Rezult = (el[2]=='1')
            break
    return Rezult

# отрисовка прогресс спИна
def progressSpin(i):
    tmp_i = i%4
    if tmp_i == 0: tmp_s='-'
    if tmp_i == 1: tmp_s='\\'
    if tmp_i == 2: tmp_s='|'
    if tmp_i == 3: tmp_s='/'
    return tmp_s

#подготовка экрана
def set_scr():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Парсер для обработки программ телеканалов ')
    print('Макеев Петр тел. 8-912-34-161-34 ')
    print('-----------------------------------------------')
 

# поправка на часовой пояс
def timeDiv(strTime, fl_change):
    if fl_change:
        if strTime.find(':')>-1 or  strTime.find('.')>-1:
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
        else:
            Rezult = strTime
    else:
        if strTime.find(':')>-1 or  strTime.find('.')>-1:
            if ':' in strTime:
                strHourN = int(strTime.split(':')[0]) 
            else:
                strHourN = int(strTime.split('.')[0]) 
            if strHourN<10:
                Rezult = '0' + str(strHourN) + '.' + strTime[-2:]
            else:
                Rezult = str(strHourN) + '.' + strTime[-2:]
        else:
            Rezult = strTime
    return Rezult


# готовим список каналов и справочники обработок
def txt_to_list(path_prog):

    global lst_txt
    global divH

    # создаем список файлов источников
    list_in = os.listdir(path_prog + '\\in')
    for name_files_in in list_in:
        if name_files_in[-3:]=='txt':
            lst_txt.append(path_prog + '\\in\\' + name_files_in)

    # считываем файл с телеканалами Chanenl.txt
    try:
        with open('Channel.txt', 'r') as file_r:
            str_txt_ch = file_r.readlines()
    except:
        # cправочник каналов Channel.txt недоступен
        print('Не найден файл со списком каналов - Channel.txt!')
        exit()

    # заполняем справочник каналов 
    for i, el in enumerate(str_txt_ch):
        if not (el[0] == '#' or el.strip()==''):
            lst_Ch.append(el.replace('\n','').split('|'))
            print('Считываем настройки - ' + progressSpin(i), end='\r')

    # считываем файл с заменами Replace.txt
    try:
        with open('Replace.txt', 'r') as file_r:
            str_txt_rpl = file_r.readlines()
    except:
        # cправочник каналов Replace.txt недоступен
        print('Не найден файл со списком замен - Replace.txt!')
        exit()

    # заполняем справочник замен 
    for i, el in enumerate(str_txt_rpl):
        if not (el[0] == '#' or el.strip()==''):
            lst_Repl.append(el.replace('\n','').split('|'))
            print('Считываем настройки - ' + progressSpin(i), end='\r')      

    try:
        # считываем файл с заменами Remove.txt
        with open('Remove.txt', 'r') as file_r:
            str_txt_rem = file_r.readlines()
    except:
        # cправочник каналов Replace.txt недоступен
        print('Не найден файл со списком удалений - Remove.txt!')
        exit()

    # заполняем справочник удалений 
    for i, el in enumerate(str_txt_rem):
        if not (el[0] == '#' or el.strip()==''):
            lst_Remove.append(el.replace('\n',''))
            print('Считываем настройки - ' + progressSpin(i), end='\r')      

    try:
        # считываем файл с исключениями CapsWord.txt
        with open('CapsWord.txt', 'r') as file_r:
            str_txt_cpsl = file_r.readlines()
    except:
        # cправочник каналов CapsWord.txt недоступен
        print('Не найден файл со списком удалений - CapsWord.txt!')
        exit()

    # заполняем справочник капслоков 
    for i, el in enumerate(str_txt_cpsl):
        if not (el[0] == '#' or el.strip()==''):
            lst_CapsWord.append(el.replace('\n',''))
            print('Считываем настройки - ' + progressSpin(i), end='\r')      

    try:
        # считываем файл с исключениями StopWord.txt
        with open('StopWord.txt', 'r') as file_r:
            str_txt_stopw = file_r.readlines()
    except:
        # cправочник каналов StopWord.txt недоступен
        print('Не найден файл со списком удалений - StopWord.txt!')
        exit()

    # заполняем справочник капслоков 
    for i, el in enumerate(str_txt_stopw):
        if not (el[0] == '#' or el.strip()==''):
            lst_StopWord.append(el.replace('\n',''))
            print('Считываем настройки - ' + progressSpin(i), end='\r')      

    print('Считываем настройки - ВЫПОЛНЕНО!')   



# готовим  списки телепрограмм по дням недели для наполнения
def fill_Day():        
    
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



# сканируем файлы txt и формируем  программы
def txt_to_prog(path_prog):
    
    progressInt = 0
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
        fl_merge = False
        fl_merge2 = False
        for str_line in str_txt:
            # проверяем первый знак 
            str_tmp = str_line[:-1].strip()
            # и пустые строки
            if len(str_tmp)<3: continue

            print('Загружаем телепрограммы - ' + progressSpin(progressInt), end='\r')  
            progressInt += 1
 
            str_sub_lineD = str_tmp.split(',',2)
            if str_sub_lineD[0].upper() in list_week:
                # в строке день недели
                name_Day = str_sub_lineD[0].upper()
            else:
                # в строке программа
                # отделяем время программы от названия программы
                if len(str_sub_lineD)>0:
                    str_sub_lineD = str_tmp.split(' ',1)
                    
                    # если начинается строка с буквы или кавычки
                    if str_sub_lineD[0][0].isalpha() or str_sub_lineD[0][0] == '"'  or str_sub_lineD[0][0] == '«'  or name_Pr=='None' :
                        if fl_merge:
                            fl_merge2 = True
                        fl_merge = True
                    else:
                        fl_merge = False
                        fl_merge2 = False
                        
                    # если второе объединение строки то соединеям |  а не   пробелом
                    if fl_merge:
                        if fl_merge2:
                            name_Pr = name_Pr + ' ' + str_tmp
                        else:
                            name_Pr = name_Pr + '|' + str_tmp
                    else:
                        if len(str_sub_lineD)==1:
                            name_Pr = timeDiv(str_sub_lineD[0], fl_to_name_Ch(name_Ch_id))
                        else:    
                            name_Pr = timeDiv(str_sub_lineD[0], fl_to_name_Ch(name_Ch_id)) + '|' + str_sub_lineD[1] 
    
                    # собираем список [канал, [программа]] 
                    if name_Day == 'ПОНЕДЕЛЬНИК':
                        for i, el in enumerate(lst_Ch):
                            if el[1]==name_Ch:
                                if fl_merge:
                                    if fl_merge2:
                                        lst_D1[i][-1] = lst_D1[i][-1] + ' ' + str_tmp
                                    else:
                                        lst_D1[i][-1] = name_Pr
                                else:
                                    lst_D1[i].append(name_Pr.strip())                            

                    elif name_Day == 'ВТОРНИК':
                        for i, el in enumerate(lst_Ch):
                            if el[1]==name_Ch:
                                if fl_merge:
                                    lst_D2[i][-1] = lst_D2[i][-1] + '|' + str_tmp
                                else:
                                    lst_D2[i].append(name_Pr.strip())                            

                    elif name_Day == 'СРЕДА':
                        for i, el in enumerate(lst_Ch):
                            if el[1]==name_Ch:
                                if fl_merge:
                                    lst_D3[i][-1] = lst_D3[i][-1] + '|' + str_tmp
                                else:
                                    lst_D3[i].append(name_Pr.strip())                            

                    elif name_Day == 'ЧЕТВЕРГ':
                        for i, el in enumerate(lst_Ch):
                            if el[1]==name_Ch:
                                if fl_merge:
                                    lst_D4[i][-1] = lst_D4[i][-1] + '|' + str_tmp
                                else:
                                    lst_D4[i].append(name_Pr.strip())                            

                    elif name_Day == 'ПЯТНИЦА':
                         for i, el in enumerate(lst_Ch):
                            if el[1]==name_Ch:
                                if fl_merge:
                                    lst_D5[i][-1] = lst_D5[i][-1] + '|' + str_tmp
                                else:
                                    lst_D5[i].append(name_Pr.strip())                            

                    elif name_Day == 'СУББОТА':
                        for i, el in enumerate(lst_Ch):
                            if el[1]==name_Ch:
                                if fl_merge:
                                    lst_D6[i][-1] = lst_D6[i][-1] + '|' + str_tmp
                                else:
                                    lst_D6[i].append(name_Pr.strip())                            

                    elif name_Day == 'ВОСКРЕСЕНЬЕ':
                        for i, el in enumerate(lst_Ch):
                            if el[1]==name_Ch:
                                if fl_merge:
                                    lst_D7[i][-1] = lst_D7[i][-1] + '|' + str_tmp
                                else:
                                    lst_D7[i].append(name_Pr.strip())                            
    print('Загружаем телепрограммы - ВЫПОЛНЕНО!')  


# перебираем списки программ для вызова анализа
def analiz_prog():

    progressInt = 0

    # перебираем программы Понедельника
    for l, el_D in enumerate(lst_D1):
        for i, el_Pr in enumerate(el_D):
            if i>0:
                # сохранение телепрограмм 
               lst_D1[l][i] = el_Pr.split('|', 1)[0] + '|' + replace_in_prog(el_Pr.split('|', 1)[1])

    print('Анализ телепрограмм - ' + progressSpin(progressInt) , end='\r')
    progressInt +=  1

    # перебираем программы Вторника
    for l, el_D in enumerate(lst_D2):
        for i, el_Pr in enumerate(el_D):
            if i>0:
                # сохранение телепрограмм 
               lst_D2[l][i] = el_Pr.split('|', 1)[0] + '|' + replace_in_prog(el_Pr.split('|', 1)[1])

    print('Анализ телепрограмм - ' + progressSpin(progressInt) , end='\r')
    progressInt +=  1

    # перебираем программы Среды
    for l, el_D in enumerate(lst_D3):
        for i, el_Pr in enumerate(el_D):
            if i>0:
                # сохранение телепрограмм 
               lst_D3[l][i] = el_Pr.split('|', 1)[0] + '|' + replace_in_prog(el_Pr.split('|', 1)[1])

    print('Анализ телепрограмм - ' + progressSpin(progressInt) , end='\r')
    progressInt +=  1

    # перебираем программы Четверга
    for l, el_D in enumerate(lst_D4):
        for i, el_Pr in enumerate(el_D):
            if i>0:
                # сохранение телепрограмм 
               lst_D4[l][i] = el_Pr.split('|', 1)[0] + '|' + replace_in_prog(el_Pr.split('|', 1)[1])

    print('Анализ телепрограмм - ' + progressSpin(progressInt) , end='\r')
    progressInt +=  1

    # перебираем программы Пятницы
    for l, el_D in enumerate(lst_D5):
        for i, el_Pr in enumerate(el_D):
            if i>0:
                # сохранение телепрограмм 
               lst_D5[l][i] = el_Pr.split('|', 1)[0] + '|' + replace_in_prog(el_Pr.split('|', 1)[1])

    print('Анализ телепрограмм - ' + progressSpin(progressInt) , end='\r')
    progressInt +=  1

    # перебираем программы Субботы
    for l, el_D in enumerate(lst_D6):
        for i, el_Pr in enumerate(el_D):
            if i>0:
                # сохранение телепрограмм 
               lst_D6[l][i] = el_Pr.split('|', 1)[0] + '|' + replace_in_prog(el_Pr.split('|', 1)[1])

    print('Анализ телепрограмм - ' + progressSpin(progressInt) , end='\r')
    progressInt +=  1

    # перебираем программы Вторника
    for l, el_D in enumerate(lst_D7):
        for i, el_Pr in enumerate(el_D):
            if i>0:
                # сохранение телепрограмм 
               lst_D7[l][i] = el_Pr.split('|', 1)[0] + '|' + replace_in_prog(el_Pr.split('|', 1)[1])

    print('Анализ телепрограмм - ВЫПОЛНЕНО')


# сохранение сведений о телепрограмме
def save_prog(doc_, doc_N, el_Pr_, el_D_, i, str_prog_, str_prog_N):
    if i<1:
        if len(el_D_) > 1:
            str_prog_= str_prog_ + 'STYLE K ' + el_Pr_.upper() + '\n'
            str_prog_N=  str_prog_N + ' ' + el_Pr_.upper() + '\n'
            # doc
            paragraph = doc_.add_paragraph('STYLE K ' + el_Pr_.upper() )
            paragraph.paragraph_format.space_before = Mm(0)
            paragraph.paragraph_format.space_after = Mm(0)

            paragraph = doc_N.add_paragraph('-------------------------------')
            paragraph.paragraph_format.space_before = Mm(0)
            paragraph.paragraph_format.space_after = Mm(0)
            paragraph = doc_N.add_paragraph(' ' + el_Pr_.upper() )
            paragraph.paragraph_format.space_before = Mm(0)
            paragraph.paragraph_format.space_after = Mm(0)
        else:
            str_prog_ = str_prog_+ 'STYLE K ' + el_Pr_.upper() + ' !!!! ПРОПУЩЕН !!!!' +  '\n'
            str_prog_N =  str_prog_N + ' ' + el_Pr_.upper() + ' !!!! ПРОПУЩЕН !!!!' +  '\n'
            # doc
            paragraph = doc_.add_paragraph('STYLE K ' + el_Pr_.upper() + ' !!!! ПРОПУЩЕН !!!!')
            paragraph.paragraph_format.space_before = Mm(0)
            paragraph.paragraph_format.space_after = Mm(0)

            paragraph = doc_N.add_paragraph('-------------------------------')
            paragraph.paragraph_format.space_before = Mm(0)
            paragraph.paragraph_format.space_after = Mm(0)
            paragraph = doc_N.add_paragraph(' ' + el_Pr_.upper() + ' !!!! ПРОПУЩЕН !!!!')
            paragraph.paragraph_format.space_before = Mm(0)
            paragraph.paragraph_format.space_after = Mm(0)
            
    else:

        #анализируем и обрабатываем строку
        repl_str_prog = el_Pr_.split('|',1)[1]

        if '^' in repl_str_prog:
            vozrast_id = repl_str_prog.split('^')[-1]
        else:
            vozrast_id =''

        str_prog_ = str_prog_ + el_Pr_.split('|',1)[0] + ' ' + repl_str_prog + '\n'
        str_prog_N = str_prog_N + el_Pr_.split('|',1)[0] + ' ' + repl_str_prog + '\n'     
                   
        # doc
        paragraph = doc_.add_paragraph()
        paragraph.add_run(el_Pr_.split('|',1)[0] ).bold = True
        paragraph.add_run(' ' + repl_str_prog.split('^')[0]).bold = False
        if not vozrast_id == '':
            paragraph.add_run(vozrast_id).font.superscript = True
        paragraph.paragraph_format.space_before = Mm(0)
        paragraph.paragraph_format.space_after = Mm(0)

        paragraph = doc_N.add_paragraph()
        paragraph.add_run(el_Pr_.split('|',1)[0] ).bold = True
        paragraph.add_run(' ' + repl_str_prog.split('^')[0]).bold = False
        if not vozrast_id == '':
            paragraph.add_run(vozrast_id).font.superscript = True
        paragraph.paragraph_format.space_before = Mm(0)
        paragraph.paragraph_format.space_after = Mm(0)
    return [str_prog_, str_prog_N]



# экспорт в файлы 
def exp_prog(path_prog): 


    # задаем стиль текста по умолчанию
    style = doc1.styles['Normal']
    # название шрифта
    style.font.name = 'Arial'
    # размер шрифта
    style.font.size = Pt(12)
        
    progressInt = 0

    # понедельник
    str_prog1 = 'STYLE D \n'
    str_progN = '-------------------------------\n' + ' ПОНЕДЕЛЬНИК\n'

    # doc
    paragraph = doc1.add_paragraph('STYLE D ')
    paragraph.paragraph_format.space_before = Mm(0)
    paragraph.paragraph_format.space_after = Mm(0)
    
    paragraph = docN.add_paragraph('-------------------------------')
    paragraph.paragraph_format.space_before = Mm(0)
    paragraph.paragraph_format.space_after = Mm(0)
    paragraph = docN.add_paragraph(' ПОНЕДЕЛЬНИК')
    paragraph.paragraph_format.space_before = Mm(0)
    paragraph.paragraph_format.space_after = Mm(0)

    for el_D in lst_D1:
        # перебираем программы
        for i, el_Pr in enumerate(el_D):

            # сохранение телепрограмм 
            lst_tmp = save_prog(doc1, docN, el_Pr, el_D, i, str_prog1, str_progN)
            str_prog1 = lst_tmp[0]
            str_progN = lst_tmp[1]

            print(('Сохранение телепрограмм Понедельника - ' + progressSpin(progressInt)).ljust(60, " ") , end='\r')
            progressInt +=  1


     # вторник
    str_prog2 = 'STYLE D \n'
    str_progN =  str_progN + '-------------------------------\n' + ' ВТОРНИК\n'
    
    # doc
    paragraph = docN.add_paragraph('-------------------------------')
    paragraph.paragraph_format.space_before = Mm(0)
    paragraph.paragraph_format.space_after = Mm(0)
    paragraph = docN.add_paragraph(' ВТОРНИК')
    paragraph.paragraph_format.space_before = Mm(0)
    paragraph.paragraph_format.space_after = Mm(0)

    paragraph = doc2.add_paragraph('STYLE D ')
    paragraph.paragraph_format.space_before = Mm(0)
    paragraph.paragraph_format.space_after = Mm(0)

    for el_D in lst_D2:
        # перебираем программы
        for i, el_Pr in enumerate(el_D):

            # сохранение телепрограмм 
            lst_tmp = save_prog(doc2, docN, el_Pr, el_D, i, str_prog2, str_progN)
            str_prog2 = lst_tmp[0]
            str_progN = lst_tmp[1]

            print(('Сохранение телепрограмм Вторника - ' + progressSpin(progressInt)).ljust(60, " ") , end='\r')
            progressInt +=  1


    # вторник
    str_prog3 = 'STYLE D \n'
    str_progN = str_progN + '-------------------------------\n' + ' СРЕДА\n'


    # doc
    paragraph = docN.add_paragraph('-------------------------------')
    paragraph.paragraph_format.space_before = Mm(0)
    paragraph.paragraph_format.space_after = Mm(0)
    paragraph = docN.add_paragraph(' СРЕДА')
    paragraph.paragraph_format.space_before = Mm(0)
    paragraph.paragraph_format.space_after = Mm(0)

    paragraph = doc3.add_paragraph('STYLE D ')
    paragraph.paragraph_format.space_before = Mm(0)
    paragraph.paragraph_format.space_after = Mm(0)

    for el_D in lst_D3:
        # перебираем программы
        for i, el_Pr in enumerate(el_D):

            # сохранение телепрограмм 
            lst_tmp = save_prog(doc3, docN, el_Pr, el_D, i, str_prog3, str_progN)
            str_prog3 = lst_tmp[0]
            str_progN = lst_tmp[1]

            print(('Сохранение телепрограмм Среды - ' + progressSpin(progressInt)).ljust(60, " ") , end='\r')
            progressInt +=  1


    # четверг
    str_progN = str_progN + '-------------------------------\n' + ' ЧЕТВЕРГ\n'
    str_prog4 = 'STYLE D \n'
    # doc
    paragraph = docN.add_paragraph('-------------------------------')
    paragraph.paragraph_format.space_before = Mm(0)
    paragraph.paragraph_format.space_after = Mm(0)
    paragraph = docN.add_paragraph(' ЧЕТВЕРГ')
    paragraph.paragraph_format.space_before = Mm(0)
    paragraph.paragraph_format.space_after = Mm(0)

    paragraph = doc4.add_paragraph('STYLE D ')
    paragraph.paragraph_format.space_before = Mm(0)
    paragraph.paragraph_format.space_after = Mm(0)

    for el_D in lst_D4:
        # перебираем программы
        for i, el_Pr in enumerate(el_D):

            # сохранение телепрограмм 
            lst_tmp = save_prog(doc4, docN, el_Pr, el_D, i, str_prog4, str_progN)
            str_prog4 = lst_tmp[0]
            str_progN = lst_tmp[1]

            print(('Сохранение телепрограмм Четверга - ' + progressSpin(progressInt)).ljust(60, " ") , end='\r')
            progressInt +=  1


    # пятница
    str_progN = str_progN + '-------------------------------\n' + ' ПЯТНИЦА\n'
    str_prog5 = 'STYLE D \n'
    # doc
    paragraph = docN.add_paragraph('-------------------------------')
    paragraph.paragraph_format.space_before = Mm(0)
    paragraph.paragraph_format.space_after = Mm(0)
    paragraph = docN.add_paragraph(' ПЯТНИЦА')
    paragraph.paragraph_format.space_before = Mm(0)
    paragraph.paragraph_format.space_after = Mm(0)

    paragraph = doc5.add_paragraph('STYLE D ')
    paragraph.paragraph_format.space_before = Mm(0)
    paragraph.paragraph_format.space_after = Mm(0)

    for el_D in lst_D5:
        # перебираем программы
        for i, el_Pr in enumerate(el_D):

            # сохранение телепрограмм 
            lst_tmp = save_prog(doc5, docN, el_Pr, el_D, i, str_prog5, str_progN)
            str_prog5 = lst_tmp[0]
            str_progN = lst_tmp[1]

            print(('Сохранение телепрограмм Пятницы - ' + progressSpin(progressInt)).ljust(60, " ") , end='\r')
            progressInt +=  1


    # суббота
    str_progN = str_progN + '-------------------------------\n' + ' СУББОТА\n'
    str_prog6 = 'STYLE D \n'
    # doc
    paragraph = docN.add_paragraph('-------------------------------')
    paragraph.paragraph_format.space_before = Mm(0)
    paragraph.paragraph_format.space_after = Mm(0)
    paragraph = docN.add_paragraph(' СУББОТА')
    paragraph.paragraph_format.space_before = Mm(0)
    paragraph.paragraph_format.space_after = Mm(0)

    paragraph = doc6.add_paragraph('STYLE D ')
    paragraph.paragraph_format.space_before = Mm(0)
    paragraph.paragraph_format.space_after = Mm(0)

    for el_D in lst_D6:
        # перебираем программы
        for i, el_Pr in enumerate(el_D):
                        
            # сохранение телепрограмм 
            lst_tmp = save_prog(doc6, docN, el_Pr, el_D, i, str_prog6, str_progN)
            str_prog6 = lst_tmp[0]
            str_progN = lst_tmp[1]

            print(('Сохранение телепрограмм Субботы - ' + progressSpin(progressInt)).ljust(60, " ") , end='\r')
            progressInt +=  1


    # воскресенье
    str_progN = str_progN + '-------------------------------\n' + ' ВОСКРЕСЕНЬЕ\n'
    str_prog7 = 'STYLE D \n'
    # doc
    paragraph = docN.add_paragraph('-------------------------------')
    paragraph.paragraph_format.space_before = Mm(0)
    paragraph.paragraph_format.space_after = Mm(0)
    paragraph = docN.add_paragraph(' ВОСКРЕСЕНЬЕ')
    paragraph.paragraph_format.space_before = Mm(0)
    paragraph.paragraph_format.space_after = Mm(0)

    paragraph = doc7.add_paragraph('STYLE D ')
    paragraph.paragraph_format.space_before = Mm(0)
    paragraph.paragraph_format.space_after = Mm(0)
    for el_D in lst_D7:
        # перебираем программы
        for i, el_Pr in enumerate(el_D):

            # сохранение телепрограмм 
            lst_tmp = save_prog(doc7, docN, el_Pr, el_D, i, str_prog7, str_progN)
            str_prog7 = lst_tmp[0]
            str_progN = lst_tmp[1]

            print(('Сохранение телепрограмм Воскресенья - ' + progressSpin(progressInt)).ljust(60, " ") , end='\r')
            progressInt +=  1

    # сохраняем данные 
    try:
        with open(path_prog +'\\OUT\\REZULT.REZ', 'w') as file_w:
            file_w.writelines(str_progN)
    except:
        print('Файл REZULT.REZ заблокирован для вывода списка каналов!')            

    print(('Сохранение результатов в файлы - ' + progressSpin(progressInt)).ljust(60, " ")  , end='\r')
    progressInt +=  1

    try:
        with open(path_prog +'\\OUT\\1.REZ', 'w') as file_w:
            file_w.writelines(str_prog1)
    except:
        print('Файл 1.REZ заблокирован для вывода списка каналов!')            

    print(('Сохранение результатов в файлы - ' + progressSpin(progressInt) ).ljust(60, " ") , end='\r')
    progressInt +=  1

    try:
        with open(path_prog +'\\OUT\\2.REZ', 'w') as file_w:
            file_w.writelines(str_prog2)
    except:
        print('Файл 2.REZ заблокирован для вывода списка каналов!')   

    print(('Сохранение результатов в файлы - ' + progressSpin(progressInt) ).ljust(60, " ") , end='\r')
    progressInt +=  1

    try:
        with open(path_prog +'\\OUT\\3.REZ', 'w') as file_w:
            file_w.writelines(str_prog3)
    except:
        print('Файл 3.REZ заблокирован для вывода списка каналов!')    
               
    print(('Сохранение результатов в файлы - ' + progressSpin(progressInt) ).ljust(60, " ")  , end='\r')
    progressInt +=  1

    try:
        with open(path_prog +'\\OUT\\4.REZ', 'w') as file_w:
            file_w.writelines(str_prog4)
    except:
        print('Файл 4.REZ заблокирован для вывода списка каналов!')    

    print(('Сохранение результатов в файлы - ' + progressSpin(progressInt)).ljust(60, " ")  , end='\r')
    progressInt +=  1

    try:
        with open(path_prog +'\\OUT\\5.REZ', 'w') as file_w:
            file_w.writelines(str_prog5)
    except:
        print('Файл 5.REZ заблокирован для вывода списка каналов!')  

    print(('Сохранение результатов в файлы - ' + progressSpin(progressInt)).ljust(60, " ")  , end='\r')
    progressInt +=  1

    try:
        with open(path_prog +'\\OUT\\6.REZ', 'w') as file_w:
            file_w.writelines(str_prog6)
    except:
        print('Файл 6.REZ заблокирован для вывода списка каналов!')   

    print(('Сохранение результатов в файлы - ' + progressSpin(progressInt) ).ljust(60, " ") , end='\r')
    progressInt +=  1

    try:
        with open(path_prog +'\\OUT\\7.REZ', 'w') as file_w:
            file_w.writelines(str_prog7)
    except:
        print('Файл 7.REZ заблокирован для вывода списка каналов!')     

    print(('Сохранение результатов в файлы - ' + progressSpin(progressInt) ).ljust(60, " ") , end='\r')
    progressInt +=  1

    #doc
    try:
        doc1.save(path_prog + '\\OUT\\1.docx')       
    except:
        print('Файл 1.docx заблокирован для вывода списка каналов!')     

    print(('Сохранение результатов в файлы - ' + progressSpin(progressInt)).ljust(60, " ")  , end='\r')
    progressInt +=  1

    try:
        doc2.save(path_prog + '\\OUT\\2.docx')       
    except:
        print('Файл 2.docx заблокирован для вывода списка каналов!')     

    print(('Сохранение результатов в файлы - ' + progressSpin(progressInt) ).ljust(60, " ") , end='\r')
    progressInt +=  1

    try:
        doc3.save(path_prog + '\\OUT\\3.docx')       
    except:
        print('Файл 3.docx заблокирован для вывода списка каналов!')     

    print(('Сохранение результатов в файлы - ' + progressSpin(progressInt) ).ljust(60, " ") , end='\r')
    progressInt +=  1

    try:
        doc4.save(path_prog + '\\OUT\\4.docx')       
    except:
        print('Файл 1.docx заблокирован для вывода списка каналов!')     

    print(('Сохранение результатов в файлы - ' + progressSpin(progressInt) ).ljust(60, " ") , end='\r')
    progressInt +=  1

    try:
        doc5.save(path_prog + '\\OUT\\4.docx')       
    except:
        print('Файл 1.docx заблокирован для вывода списка каналов!')     

    print(('Сохранение результатов в файлы - ' + progressSpin(progressInt) ).ljust(60, " ") , end='\r')
    progressInt +=  1

    try:
        doc6.save(path_prog + '\\OUT\\5.docx')       
    except:
        print('Файл 5.docx заблокирован для вывода списка каналов!')     

    print(('Сохранение результатов в файлы - ' + progressSpin(progressInt)).ljust(60, " ")  , end='\r')
    progressInt +=  1

    try:
        doc1.save(path_prog + '\\OUT\\6.docx')       
    except:
        print('Файл 7.docx заблокирован для вывода списка каналов!')     

    print(('Сохранение результатов в файлы - ' + progressSpin(progressInt) ).ljust(60, " ") , end='\r')
    progressInt +=  1

    try:
        doc7.save(path_prog + '\\OUT\\7.docx')       
    except:
        print('Файл 1.docx заблокирован для вывода списка каналов!')     

    print(('Сохранение результатов в файлы - ' + progressSpin(progressInt) ).ljust(60, " ") , end='\r')
    progressInt +=  1

    try:
        docN.save(path_prog + '\\OUT\\Rezult.docx')       
    except:
        print('Файл Rezult.docx заблокирован для вывода списка каналов!')     

    print('Сохранение результатов в файлы - ВЫПОЛНЕНО!')




# проверяем и делаем деКапсЛок
def deCapsLock(str_dcl):
    str_dcl = str_dcl.strip()
    fl_caps = True
    fl_CapsWord = False
    lst_dcl = str_dcl.split(' ')
    tmp_str = ''
    for i, el in enumerate(lst_dcl):

        if lst_dcl[i]=='':
            continue

        # если первое слово и заглавные то устанавливаем первыю заглавную
        if i==0 and fl_caps:
            if lst_dcl[i][0].isalpha():
                tmp_str = lst_dcl[i][0].upper()  + lst_dcl[i][1:].lower()
            elif len(lst_dcl[i])>1:
                tmp_str = lst_dcl[i][:2].upper()  + lst_dcl[i][2:].lower()
            else:
                tmp_str = lst_dcl[i]
            continue

        #проверяем исключения по Капслоку
        for el_cpsl in lst_CapsWord:
            pos_cpsl = el.upper().find(el_cpsl.upper())
            if pos_cpsl>-1:
                if pos_cpsl==0:
                    if len(tmp_str.strip())>0:
                        tmp_str = tmp_str + ' ' + el_cpsl + el[len(el_cpsl):]    
                    else:
                        tmp_str = el_cpsl
                else:
                    if len(tmp_str.strip())>0:
                        tmp_str = tmp_str + ' ' + el_cpsl + el[len(el_cpsl)+pos_cpsl:]   
                    else:
                        tmp_str = el[:pos_cpsl] + el_cpsl + el[len(el_cpsl)+pos_cpsl:]
                fl_CapsWord = True
                break
            else:
                fl_CapsWord = False

        # если попалось исключение по CapsWord берем следующее слово
        if fl_CapsWord: 
            continue

        fl_caps = True
        # по буквам проверяем слово на заглавные
        for j, sub_el in enumerate(el):
            if sub_el.isalpha() and fl_caps:
                if not sub_el.istitle(): 
                    # если попалась не заглавная сбрасываем флаг
                    fl_caps = False
                    break


        # если слово начинается с кавычек 
        if i>0 and (lst_dcl[i][0]== '«' or lst_dcl[i][0]== '\'') and fl_caps:
            tmp_str = tmp_str + ' ' +  lst_dcl[i][0].upper()  + lst_dcl[i][1].upper()  + lst_dcl[i][2:].lower()

        # если предыдущее слово заканчивается точкой
        elif i>0 and (not lst_dcl[i-1]==''):
            if lst_dcl[i-1][-1]=='.':            
                tmp_str = tmp_str + ' ' + lst_dcl[i][0].upper()  + lst_dcl[i][1:].lower() 
            else:
                tmp_str = tmp_str + ' ' + lst_dcl[i].lower() 

        # все прописные
        else:
            tmp_str = tmp_str + ' ' + lst_dcl[i].lower()

    # if fl_caps:
    #     str_dcl = str_dcl[0] + str_dcl[1:].lower()
    str_dcl = tmp_str.strip()
    
    return str_dcl


# делаем анализ строки программы 
# проводим замены и синтезируем строку 
# str_sub_repl - строка замены 
# str_sub_vozrast - строка возрастное ограничение
# str_sub_name_prog - строка программы внутри кавычек елочкой
# str_sub_ser - строка с сериями
# str_sub_sez - строка с сезонами 
# str_sub_rol - строка в ролях 
# str_sub_rezh - строка режиссер

def del_dubl_prog():
    progressInt = 0
    
    # перебираем программы понедельника
    for k, el_prog in enumerate(lst_D1):
        for i, el in enumerate(el_prog):
            if i>0:
                lst_el = el.split('|',1)[1]
                lst_del = []
                for j, el_seek in enumerate(el_prog):
                    if j>i:
                        lst_el_seek = el_seek.split('|',1)[1]
                        if lst_el==lst_el_seek:
                            # найден дубль в j для i
                            lst_D1[k][i] = lst_D1[k][i].split("|")[0] + ', ' + lst_D1[k][j].split('|')[0] + '|' + lst_D1[k][i].split("|")[1]
                            lst_del.append(j)

                for n in reversed(lst_del):
                    del lst_D1[k][n]    

    print('Собираем дубликаты программ - ' + progressSpin(progressInt) , end='\r')
    progressInt +=  1

    # перебираем программы Вторника
    for k, el_prog in enumerate(lst_D2):
        for i, el in enumerate(el_prog):
            if i>0:
                lst_el = el.split('|',1)[1]
                lst_del = []
                for j, el_seek in enumerate(el_prog):
                    if j>i:
                        lst_el_seek = el_seek.split('|',1)[1]
                        if lst_el==lst_el_seek:
                            # найден дубль в j для i
                            lst_D2[k][i] = lst_D2[k][i].split("|")[0] + ', ' + lst_D2[k][j].split('|')[0] + '|' + lst_D2[k][i].split("|")[1]
                            lst_del.append(j)

                for n in reversed(lst_del):
                    del lst_D2[k][n]    

    print('Собираем дубликаты программ - ' + progressSpin(progressInt) , end='\r')
    progressInt +=  1

    # перебираем программы среда
    for k, el_prog in enumerate(lst_D3):
        for i, el in enumerate(el_prog):
            if i>0:
                lst_el = el.split('|',1)[1]
                lst_del = []
                for j, el_seek in enumerate(el_prog):
                    if j>i:
                        lst_el_seek = el_seek.split('|',1)[1]
                        if lst_el==lst_el_seek:
                            # найден дубль в j для i
                            lst_D3[k][i] = lst_D3[k][i].split("|")[0] + ', ' + lst_D3[k][j].split('|')[0] + '|' + lst_D3[k][i].split("|")[1]
                            lst_del.append(j)

                for n in reversed(lst_del):
                    del lst_D3[k][n]    

    print('Собираем дубликаты программ - ' + progressSpin(progressInt) , end='\r')
    progressInt +=  1

     # перебираем программы четверг
    for k, el_prog in enumerate(lst_D4):
        for i, el in enumerate(el_prog):
            if i>0:
                lst_el = el.split('|',1)[1]
                lst_del = []
                for j, el_seek in enumerate(el_prog):
                    if j>i:
                        lst_el_seek = el_seek.split('|',1)[1]
                        if lst_el==lst_el_seek:
                            # найден дубль в j для i
                            lst_D4[k][i] = lst_D4[k][i].split("|")[0] + ', ' + lst_D4[k][j].split('|')[0] + '|' + lst_D4[k][i].split("|")[1]
                            lst_del.append(j)

                for n in reversed(lst_del):
                    del lst_D4[k][n]    
          
    print('Собираем дубликаты программ - ' + progressSpin(progressInt) , end='\r')
    progressInt +=  1

    # перебираем программы пятница
    for k, el_prog in enumerate(lst_D5):
        for i, el in enumerate(el_prog):
            if i>0:
                lst_el = el.split('|',1)[1]
                lst_del = []
                for j, el_seek in enumerate(el_prog):
                    if j>i:
                        lst_el_seek = el_seek.split('|',1)[1]
                        if lst_el==lst_el_seek:
                            # найден дубль в j для i
                            lst_D5[k][i] = lst_D5[k][i].split("|")[0] + ', ' + lst_D5[k][j].split('|')[0] + '|' + lst_D5[k][i].split("|")[1]
                            lst_del.append(j)

                for n in reversed(lst_del):
                    del lst_D5[k][n]    
    
    print('Собираем дубликаты программ - ' + progressSpin(progressInt) , end='\r')
    progressInt +=  1

    # перебираем программы суббота
    for k, el_prog in enumerate(lst_D6):
        for i, el in enumerate(el_prog):
            if i>0:
                lst_el = el.split('|',1)[1]
                lst_del = []
                for j, el_seek in enumerate(el_prog):
                    if j>i:
                        lst_el_seek = el_seek.split('|',1)[1]
                        if lst_el==lst_el_seek:
                            # найден дубль в j для i
                            lst_D6[k][i] = lst_D6[k][i].split("|")[0] + ', ' + lst_D6[k][j].split('|')[0] + '|' + lst_D6[k][i].split("|")[1]
                            lst_del.append(j)

                for n in reversed(lst_del):
                    del lst_D6[k][n]    

    print('Собираем дубликаты программ - ' + progressSpin(progressInt) , end='\r')
    progressInt +=  1

    # перебираем программы воскресенье
    for k, el_prog in enumerate(lst_D7):
        for i, el in enumerate(el_prog):
            if i>0:
                lst_el = el.split('|',1)[1]
                lst_del = []
                for j, el_seek in enumerate(el_prog):
                    if j>i:
                        lst_el_seek = el_seek.split('|',1)[1]
                        if lst_el==lst_el_seek:
                            # найден дубль в j для i
                            lst_D7[k][i] = lst_D7[k][i].split("|")[0] + ', ' + lst_D7[k][j].split('|')[0] + '|' + lst_D7[k][i].split("|")[1]
                            lst_del.append(j)

                for n in reversed(lst_del):
                    del lst_D7[k][n]    

    print('Собираем дубликаты программ - ВЫПОНЕНО!' )
    progressInt +=  1


def replace_in_prog(str_prog):

    # сканируем  в поиске возрастной категории
    str_sub_vozrast = ''
    for j, el_v in enumerate(vozrast):
        if el_v in str_prog:
            str_sub_vozrast = vozrast[j]
            break
    # вырезаем из строки 
    # и сохраняем возрастной индекс str_sub_vozrast
    repl_vozr_sub = ''
    if not str_sub_vozrast=='':
        if str_sub_vozrast[0] == '(':
            repl_vozr_sub = str_sub_vozrast + ')'
        else:
            repl_vozr_sub = str_sub_vozrast 
        if not repl_vozr_sub=='':
            str_prog = str_prog.replace(repl_vozr_sub, '') 
            str_sub_vozrast = str_sub_vozrast.replace('(', ' ').strip()
        else:
            str_sub_vozrast = ''


    # определяем наличие стоп слова в строке
    # и сохраняем в переменной str_sub_repl
    fl_stop = False
    for el in lst_StopWord:
        if str_prog.upper().find(el.upper()) > -1 :
            fl_stop = True
            break


    str_sub_repl = ''
    if not fl_stop:

        # определяем замену вырезаем из строки
        # и сохраняем в переменной str_sub_repl
        for el in lst_Repl:
            pos_repl = str_prog.upper().find(el[0].upper())
            if str_prog.upper().find(el[0].upper()) > -1 :
                if str_sub_repl == '':
                    str_sub_repl = el[1]
                str_prog = str_prog[:pos_repl].strip() + ' ' + str_prog[pos_repl + len(el[0]) :].strip()
                break
            else:
                str_sub_repl = ''


        # и вырезаем строку внутри кавычек ёлочек
        pos1 = str_prog.find('«')
        pos2 = str_prog.find('»')
        str_sub_name_prog = ''
        if not ((pos1 > -1) and (pos2 > pos1)):
            # меняем двойной апостроф на кавычки ёлочкой 
            # и вырезаем строку внутри кавычек ёлочек
            find_kav = False
            find_i = len(str_prog)
            pos1 = -1
            pos2 = -1
            for i, str_sub in enumerate(str_prog):
                if str_sub == '"' :
                    if i==0:
                        # кавычка в начале строки
                        pos1 = 0
                        continue
                    try:
                        if str_prog[i-1] == ' ':
                            # кавычка перед словом
                            pos1 = i
                            continue
                    except:
                        pos1 = i
                        continue

                    try:
                        if str_prog[i+1] == ' ' or str_prog[i+1] == '.' :
                            # кавычка после слова
                            find_kav = True
                            pos2 = i
                            continue
                    except:
                        find_kav = True
                        pos2 = i
                        continue          
                    try:
                        if str_prog[i-1].isalpha():
                            find_kav = True
                            pos2 = i
                    except:
                        pos1 = i+1
                    try:
                        if str_prog[i+1].isalpha():
                            pos1 = i
                    except:
                        find_kav = True
                        pos2 = i
                                    
                if find_kav: break

            if pos2>pos1:
                str_sub_name_prog = deCapsLock(str_prog[pos1+1:pos2])
                str_prog = str_prog[:pos1] + ' ' + str_prog[pos2+1:]
            else:
                str_sub_name_prog = ''

        # обработка сезонов и серий: 
        # ищем и удаляем "N-й сезон"    
        str_sub_sez = ''
        if "СЕЗОН" in str_prog.upper():
            pos_sez = str_prog.upper().find('СЕЗОН')
            for i in range(pos_sez-2, 0, -1):
                if not (str_prog[i].isdigit() or
                        str_prog[i].upper() == 'Й' or
                        str_prog[i] == '-'         ):
                    str_sub_sez = str_prog[i+1: pos_sez+5]
                    str_prog = str_prog[:i] + ' ' + str_prog[pos_sez+5:]
                    break
                elif (str_prog[i].isdigit() or
                        str_prog[i].upper() == 'Й' or
                        str_prog[i] == '-'  ):
                    continue     
                else: 
                    break

        # ищем и удаляем "Сезон N"    
        str_sub_sezN = ''
        if "СЕЗОН" in str_prog.upper():
            pos_sezN = str_prog.upper().find('СЕЗОН')
            if pos_sezN+6<=len(str_prog):
                for i in range(pos_sezN+6, len(str_prog), 1):
                    if not str_prog[i].isdigit() :
                        str_sub_sezN = str_prog[pos_sezN: i]
                        str_prog = str_prog[:pos_sezN]+ ' ' + str_prog[i:] 
                        break
                    elif str_prog[i].isdigit() :
                        continue     
                    else: 
                        break

        # ищем и удаляем "N-я серия"
        str_sub_ser = ''
        if "СЕРИЯ" in str_prog.upper():
            pos_ser = str_prog.upper().find('СЕРИЯ')
            for i in range(pos_ser-2, 0, -1):
                if not (str_prog[i].isdigit() or
                        str_prog[i].upper() == 'Я' or
                        str_prog[i] == '-'            ):
                    str_sub_ser = str_sub_ser + str_prog[i+1: pos_ser+5]
                    str_prog = str_prog[:i] + ' ' + str_prog[pos_ser+5:]
                    break
                elif str_prog[i].isdigit() :
                    continue           
                elif (str_prog[i].isdigit() or
                        str_prog[i].upper() == 'Я' or
                        str_prog[i] == '-'  ):
                    continue
                else: 
                    break

        # продолжаем искать и удалять "N-я - N-я - серии"
        str_sub_ser1 = ''
        str_sub_ser2 = ''

        if "СЕРИИ" in str_prog.upper():
            str_sub_ser1 = ''
            pos_ser1 = str_prog.upper().find('СЕРИИ')
            for i in range(pos_ser1-2, 0, -1):
                
                if not (str_prog[i].isdigit() or
                        str_prog[i].upper() == 'Я' or
                        str_prog[i] == '-'            ):
                    str_sub_ser1 = str_prog[i+1: pos_ser1+5]
                    str_prog = str_prog[:i] + ' ' + str_prog[pos_ser1+5:]

                    if '-Я' in str_prog.upper():
                        str_sub_ser2 = ''
                        pos_ser2 = str_prog.upper().find('-Я') 
                        for j in range(pos_ser2-2, 0, -1):

                            if not (str_prog[j].isdigit() or
                                    str_prog[j].upper() == 'Я' or
                                    str_prog[j] == '-'         ):
                                str_sub_ser2 = str_prog[j+1: pos_ser2+2]
                                str_prog = str_prog[:j] + ' ' + str_prog[pos_ser2+2:]                                
                                break

                            elif (str_prog[i].isdigit() or
                                    str_prog[i].upper() == 'Я' or
                                    str_prog[i] == '-'  ):
                                continue
                            else: 
                                break

                    break

                elif (str_prog[i].isdigit() or
                        str_prog[i].upper() == 'Я' or
                        str_prog[i] == '-'  ):
                    continue
                else: 
                    break

        str_sub_ser = str_sub_ser2 + ' - ' + str_sub_ser1

        # ищем и удаляем "Серия N"    
        str_sub_serN = ''
        if "СЕРИЯ" in str_prog.upper():
            pos_serN = str_prog.upper().find('СЕРИЯ')
            if pos_serN+6<=len(str_prog):
                for i in range(pos_serN+6, len(str_prog), 1):
                    if not str_prog[i].isdigit() :
                        str_sub_serN = str_prog[pos_serN: i]
                        str_prog = str_prog[:pos_serN]+ ' ' + str_prog[i:] 
                        break
                    elif str_prog[i].isdigit() :
                        if i+1 == len(str_prog):
                            str_sub_serN = str_prog[pos_serN: i+1]
                            str_prog = str_prog[:pos_serN]+ ' ' + str_prog[i+1:] 
                            break
                        continue     
                    else: 
                        break

        # ищем и удаляем "Часть N"    
        str_sub_chast = ''
        pos_serCh = -1
        if "ЧАСТЬ" in str_prog.upper():
            pos_serCh = str_prog.upper().find('ЧАСТЬ')
            if pos_serCh+6<=len(str_prog):
                for i in range(pos_serCh+6, len(str_prog), 1):
                    if not (str_prog[i].isdigit() or
                                    str_prog[i].upper() == 'Я' or
                                    str_prog[i] == '-'         ) :
                        str_sub_chast = str_prog[pos_serCh: i]
                        str_prog = str_prog[:pos_serCh]+ ' ' + str_prog[i:] 
                        break
                    elif pos_serCh+6<=len(str_prog):
                        if (str_prog[i].isdigit() or
                                        str_prog[i].upper() == 'Я' or
                                        str_prog[i] == '-'         ):
                            if i+1 == len(str_prog):
                                str_sub_chast = str_prog[pos_serCh: i+1]
                                str_prog = str_prog[:pos_serCh]+ ' ' + str_prog[i+1:] 
                                break
                            elif i+2 == len(str_prog):
                                str_sub_chast = str_prog[pos_serCh: i+1]
                                str_prog = str_prog[:pos_serCh]+ ' ' + str_prog[i+1:] 
                                break
                            continue     
                        else: 
                            break

        # ищем и удаляем "Выпуск N"    
        str_sub_vyp = ''
        pos_serVyp = -1
        if "ВЫПУСК" in str_prog.upper():
            pos_serVyp = str_prog.upper().find('ВЫПУСК')
            if pos_serVyp+6<=len(str_prog):
                for i in range(pos_serVyp+6, len(str_prog), 1):
                    if not str_prog[i].isdigit() :
                        str_serVyp = str_prog[pos_serVyp: i]
                        str_prog = str_prog[:pos_serVyp] + ' ' + str_prog[i:] 
                        break
                    elif str_prog[i].isdigit() :
                        if i+1 == len(str_prog):
                            str_serVyp = str_prog[pos_serVyp: i+1]
                            str_prog = str_prog[:pos_serVyp]+ ' ' + str_prog[i+1:] 
                            break
                        continue     
                    else: 
                        break


        # убираем года:
        # # убираем "г." и год
        pos_g = str_prog.find('г.')
        if pos_g > 6:
            if str_prog[pos_g-1]==' ':
                if str_prog[pos_g-2].isdigit():
                    str_prog = str_prog[:pos_g-5] + str_prog[pos_g+1:]
            else:
                if str_prog[pos_g-1].isdigit():
                    str_prog = str_prog[:pos_g-4] + str_prog[pos_g+1:]
        # убирем год без "г."
        for el_god in god_film:
            pos_g = str_prog.find(el_god)
            if not pos_g<0 :
                if not str_prog[pos_g-1] == '-':
                    str_prog = str_prog[:pos_g] + str_prog[pos_g+4:]


        # убираем в ролях и режиссера 
        # ищем В ролях 
        str_sub_rol = ''
        if "В РОЛЯХ" in str_prog.upper():
            pos_ser_rol = str_prog.upper().find('РОЛЯХ')
            str_sub_rol = str_prog[pos_ser_rol:]
            str_prog = str_prog[:pos_ser_rol-1]

        # ищем режиссер 
        str_sub_rezh = ''
        if "РЕЖИССЕР" in str_prog.upper():
            pos_ser_rech = str_prog.upper().find('РЕЖИССЕР')
            str_sub_rezh = str_prog[pos_ser_rech:]
            str_prog = str_prog[:pos_ser_rech-1]


        # ищем и удаляем слова по списку удаления
        str_sub_remove = ''
        for i, el in enumerate(lst_Remove):
            if el in str_prog:
                pos_Rem = str_prog.upper().find(el.upper())
                str_sub_remove = str_prog[pos_Rem: pos_Rem + len(el)]
                str_prog = str_prog[:pos_Rem] + ' ' + str_prog[pos_Rem + len(el):]


        # убираем  мусор: 
        # двойной пробел
        # пробел перед точкой, 
        # двойные точки
        str_prog = str_prog.strip()
                    
        if str_prog.find('  ')>-1: 
            str_prog = str_prog.replace('  ', ' ')

        if str_prog.find('  ')>-1: 
            str_prog = str_prog.replace('  ', ' ')

        if str_prog.find(' .')>-1: 
            str_prog = str_prog.replace(' .', '.')

        if str_prog.find('..')>-1: 
            str_prog = str_prog.replace('..', '.')

        if str_prog.find('..')>-1: 
            str_prog = str_prog.replace('..', '.')

        if str_prog.find('..')>-1: 
            str_prog = str_prog.replace('..', '.')

        # if str_prog.find('(S)')>-1: 
        #     str_prog = str_prog.replace('(S)', ' ')
            
        # if str_prog.find(' , .')>-1: 
        #     str_prog = str_prog.replace(' , .', '')

        # if str_prog.find('( ')>-1: 
        #     str_prog = str_prog.replace('( ', '')

        # if str_prog.find(' (')>-1: 
        #     str_prog = str_prog.replace('(', '')

        # if str_prog.find(' )')>-1: 
        #     str_prog = str_prog.replace(' )', '')

        # if str_prog.find(' ,')>-1: 
        #     str_prog = str_prog.replace(' ,', ',')

        # if str_prog.find('(, .)')>-1: 
        #     str_prog = str_prog.replace('(, .)', '')

        # if str_prog.find('-.')>-1: 
        #     str_prog = str_prog.replace('-.', ' ')

        # if str_prog.find('(, , )')>-1: 
        #     str_prog = str_prog.replace('(, , )', ' ')
            
        # if str_prog.find('(,.)')>-1: 
        #     str_prog = str_prog.replace('(,.)', ' ')

        # if str_prog.find(',.')>-1: 
        #     str_prog = str_prog.replace(',.', ' ')

        # if str_prog.find('(, )')>-1: 
        #     str_prog = str_prog.replace('(, )', ' ')

        # if str_prog.find(').')>-1: 
        #     str_prog = str_prog.replace(').', '')



        # if str_prog.find('( )')>-1: 
        #     str_prog = str_prog.replace('( )', ' ')

        # if str_prog.find(' .')>-1: 
        #     str_prog = str_prog.replace(' .', '.')



        # if str_prog.find('(*)')>-1: 
        #     str_prog = str_prog.replace('(*)', '')

        # if str_prog.find('()')>-1: 
        #     str_prog = str_prog.replace('()', '')

                
        # точка в начале строки
        if len(str_prog)>0 and str_prog[0]=='.': str_prog = str_prog[1:]
        str_prog = str_prog.strip()


        # синтезируем строку программы
        str_sintez = ''
        if not str_sub_repl == '':
            str_sintez =  str_sub_repl
      

        if not str_sub_name_prog == '':
            str_sintez = str_sintez + ' «' + str_sub_name_prog +'»'

        if str_sintez == '':
            str_sintez =  deCapsLock(str_prog)


        # if not str_sintez.strip()[-1]=='.':
        #     str_sintez = str_sintez + '.'


        if not str_sub_vozrast == '':
            str_sintez = str_sintez + ' ^' + str_sub_vozrast


        Rezult = str_sintez.strip()


    else:
        # найдено стоп слово
        if not str_sub_vozrast == '':
            Rezult = deCapsLock(str_prog) + ' ^' + str_sub_vozrast
        else:
             Rezult = deCapsLock(str_prog)

    return Rezult




# основное тело программы
def main():
    
    print('Парсер для обработки программ телеканалов ')
    print('Макеев Петр тел. 8-912-34-161-34 ')
    print('-----------------------------------------------')


    # проверяем дату
    if datetime.date.today().month>8 and datetime.date.today().day>12: 
        input('Закончился демо-режим программы, нажмите Enter для завершения.')
        exit()

    # определяем окружение
    path_prog = os.getcwd()
    
    # сделать запрос поправки на часовой пояс, по умолчанию поставить 2 часа
    #read_divH()

   # считываем тхт файлы
    txt_to_list(path_prog)

    # создаем заготовки списков программ по дням
    fill_Day()

    # считываем каналы 
    txt_to_prog(path_prog)

    # analiz_prog()
    analiz_prog()
    
    # сводим дубликаты программ в одну строку
    del_dubl_prog()

     # сохраняем программы в файлы
    exp_prog(path_prog)

    input('Телепрограммы обработаны, результаты в папке OUT, нажмите Enter для завершения.')
    # print('w')   


# точка входа.
if __name__ == '__main__':
    main()


