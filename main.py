import datetime
from operator import truediv
import os
import pathlib
import copy
#from turtle import clear
from docx import Document
from docx.shared import Pt
from docx.shared import Mm


lst_Ch = []
lst_Repl = []
lst_txt = []
divH = 2
list_week = ['ПОНЕДЕЛЬНИК', 'ВТОРНИК', 'СРЕДА', 'ЧЕТВЕРГ', 'ПЯТНИЦА', 'СУББОТА', 'ВОСКРЕСЕНЬЕ']
vozrast = []
for i in range(0,18):
    #lst_tmp = [' ' + str(i) + '+'], ['(' + str(i) + '+']
    vozrast.extend([' ' + str(i) + '+', '(' + str(i) + '+'])


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
    for i, el in enumerate(str_txt_ch):
        if not (el[0] == '#' or el=='\n'):
            lst_Ch.append(el[:-1].split('|'))
            print('Считываем список телеканалов - ' + progressSpin(i), end='\r')
    print('Считываем список телеканалов - ГОТОВО!')

    try:
        # считываем файл с заменами Replace.txt
        with open('Replace.txt', 'r') as file_r:
            str_txt_rpl = file_r.readlines()
    except:
        # cправочник каналов Replace.txt недоступен
        print('Не найден файл со списком каналов!')
        exit()

    # заполняем справочник замен 
    for i, el in enumerate(str_txt_rpl):
        if not (el[0] == '#' or el=='\n'):
            lst_Repl.append(el[:-1].split('|'))
            print('Считываем список замен - ' + progressSpin(i), end='\r')            
    print('Считываем список замен - ГОТОВО!')   


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



def txt_to_prog(path_prog):
    # сканируем файлы txt и формируем  программы
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
        for str_line in str_txt:
            # проверяем первый знак 
            str_tmp = str_line[:-1].strip()
            # и пустые строки
            if len(str_tmp)<3: continue

            print('Обрабатываем телепрограммы - ' + progressSpin(progressInt), end='\r')  
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
    print('Обрабатываем телепрограммы - ВЫПОЛНЕНО!')  


                
def replace_in_prog(str_prog):
    # делаем замены с перемещением согласно lst_Repl взятого из Replace.txt
    for el in lst_Repl:
        str_in = el[0]
        str_out = el[1]
        pos_repl = str_prog.upper().find(str_in.upper())
        if str_prog.upper().find(str_in.upper()) > -1 :
            str_prog = str_out + ' ' + str_prog.upper()[:pos_repl].strip() + ' ' + str_prog[pos_repl + len(str_in) :].strip()

    # меняем двойной апостроф на кавычки елочкой
    find_kav = False
    find_i = len(str_prog)

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
                find_kav = True
                find_i = i
           
            try:
                if str_prog[i-1].isalpha():
                    str_prog = str_prog[:i] + '»' + str_prog[i+1:]
                    find_kav = True
                    find_i = i
            except:
                str_prog = str_prog[:i] + '«' + str_prog[i+1:]              

            try:
                if str_prog[i+1].isalpha():
                    str_prog = str_prog[:i] + '«' + str_prog[i+1:]
            except:
                str_prog = str_prog[:i] + '»' + str_prog[i+1:]
                find_kav = True
                find_i = i
        if find_kav: break

    # сканируем обратно строку в поиске возрастной категории
    vozrast_ind = ''
    if len(str_prog)> find_i+2:
        for j in range(len(str_prog), find_i, -1):
            if (str_prog[j-5:j-1] in vozrast) : 
                if str_prog[j-5] == '(':
                    vozrast_ind = ' ' + str_prog [j-4:j-1]
                else:
                    vozrast_ind = str_prog [j-4:j-1]
                break




    # обрезаем строку и вставляем возрастной индекс




    # if find_kav:
    #     if not vozrast_ind == '':
    #         str_prog = str_prog[:i+1] + '^' + vozrast_ind.strip()
    #     else:
    #         str_prog = str_prog[:i+1]

                
                
                
   


    # убираем CapsLock
    for i, str_sub in enumerate(str_prog):
        # ищем CapsLock
        if i<len(str_prog)-1:
            if str_prog[i].isalpha() and str_prog[i+1].isalpha():
                    if str_prog[i].isupper() and str_prog[i+1].isupper():
                        for k in range(i+2, len(str_prog)):
                            if not str_prog[k].isalpha() or str_prog[k]=='.':
                                str_prog = str_prog[:i] + str_prog[i:k].capitalize() + str_prog[k:]   
                                i = k





    Rezult = str_prog

    return Rezult


 
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
        repl_str_prog = replace_in_prog(el_Pr_.split('|',1)[1]) 
        str_prog_ = str_prog_ + el_Pr_.split('|',1)[0] + ' ' + repl_str_prog + '\n'
        str_prog_N = str_prog_N + el_Pr_.split('|',1)[0] + ' ' + repl_str_prog + '\n'                
        # doc
        paragraph = doc_.add_paragraph()
        paragraph.add_run(el_Pr_.split('|',1)[0] ).bold = True
        paragraph.add_run(' ' + repl_str_prog).bold = False
        paragraph.paragraph_format.space_before = Mm(0)
        paragraph.paragraph_format.space_after = Mm(0)

        paragraph = doc_N.add_paragraph()
        paragraph.add_run(el_Pr_.split('|',1)[0] ).bold = True
        paragraph.add_run(' ' + repl_str_prog).bold = False
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

            print('Обработка результатов - ' + progressSpin(progressInt) , end='\r')
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

            print('Сохранение результатов - ' + progressSpin(progressInt) , end='\r')
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

            print('Сохранение результатов - ' + progressSpin(progressInt) , end='\r')
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

            print('Сохранение результатов - ' + progressSpin(progressInt) , end='\r')
            progressInt +=  1

            # сохранение телепрограмм 
            lst_tmp = save_prog(doc4, docN, el_Pr, el_D, i, str_prog4, str_progN)
            str_prog4 = lst_tmp[0]
            str_progN = lst_tmp[1]

            print('Сохранение результатов - ' + progressSpin(progressInt) , end='\r')
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

            print('Сохранение результатов - ' + progressSpin(progressInt) , end='\r')
            progressInt +=  1

            # сохранение телепрограмм 
            lst_tmp = save_prog(doc5, docN, el_Pr, el_D, i, str_prog5, str_progN)
            str_prog5 = lst_tmp[0]
            str_progN = lst_tmp[1]

            print('Сохранение результатов - ' + progressSpin(progressInt) , end='\r')
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
            
            print('Сохранение результатов - ' + progressSpin(progressInt) , end='\r')
            progressInt +=  1
                        
            # сохранение телепрограмм 
            lst_tmp = save_prog(doc6, docN, el_Pr, el_D, i, str_prog6, str_progN)
            str_prog6 = lst_tmp[0]
            str_progN = lst_tmp[1]

            print('Сохранение результатов - ' + progressSpin(progressInt) , end='\r')
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

            print('Сохранение результатов - ' + progressSpin(progressInt) , end='\r')
            progressInt +=  1

            # сохранение телепрограмм 
            lst_tmp = save_prog(doc7, docN, el_Pr, el_D, i, str_prog7, str_progN)
            str_prog7 = lst_tmp[0]
            str_progN = lst_tmp[1]

            print('Сохранение результатов - ' + progressSpin(progressInt) , end='\r')
            progressInt +=  1



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

    #doc
    try:
        doc1.save(path_prog + '\\OUT\\1.docx')       
    except:
        print('Файл 1.docx заблокирован для вывода списка каналов!')     
    try:
        doc2.save(path_prog + '\\OUT\\2.docx')       
    except:
        print('Файл 2.docx заблокирован для вывода списка каналов!')     
    try:
        doc3.save(path_prog + '\\OUT\\3.docx')       
    except:
        print('Файл 3.docx заблокирован для вывода списка каналов!')     
    try:
        doc4.save(path_prog + '\\OUT\\4.docx')       
    except:
        print('Файл 1.docx заблокирован для вывода списка каналов!')     
    try:
        doc5.save(path_prog + '\\OUT\\4.docx')       
    except:
        print('Файл 1.docx заблокирован для вывода списка каналов!')     
    try:
        doc6.save(path_prog + '\\OUT\\5.docx')       
    except:
        print('Файл 5.docx заблокирован для вывода списка каналов!')     
    try:
        doc1.save(path_prog + '\\OUT\\6.docx')       
    except:
        print('Файл 7.docx заблокирован для вывода списка каналов!')     
    try:
        doc7.save(path_prog + '\\OUT\\7.docx')       
    except:
        print('Файл 1.docx заблокирован для вывода списка каналов!')     
    try:
        docN.save(path_prog + '\\OUT\\Rezult.docx')       
    except:
        print('Файл Rezult.docx заблокирован для вывода списка каналов!')     

    print('Сохранение результатов - ГОТОВО!')

       

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
                            lst_D1[k][i] = lst_D1[k][i].split("|")[0] + ', ' + lst_D1[k][j].split('|')[0] + '|' + lst_D1[k][i].split("|")[1]
                            del lst_D1[k][j]

            
    

# основное тело программы
def main():
    
    print('Парсер для обработки программ телеканалов ')
    print('Макеев Петр тел. 8-912-34-161-34 ')
    print('-----------------------------------------------')


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

    input('Телепрограммы обработаны, результаты в папке OUT, нажмите Enter для завершения.')
    # print('w')   


# точка входа.
if __name__ == '__main__':
    main()


