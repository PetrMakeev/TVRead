from deCapsLock import deCapsLock
from main import vozrast, god_film, lst_Repl, lst_Remove

# делаем анализ строки программы 
# проводим замены и синтезируем строку 
# str_sub_repl - строка замены 
# str_sub_vozrast - строка возрастное ограничение
# str_sub_name_prog - строка программы внутри кавычек елочкой
# str_sub_ser - строка с сериями
# str_sub_sez - строка с сезонами 
# str_sub_rol - строка в ролях 
# str_sub_rezh - строка режиссер

def replace_in_prog(str_prog):

    # определяем замену вырезаем из строки
    # и сохраняем в переменной str_sub_repl
    str_sub_repl = ''
    for el in lst_Repl:
        pos_repl = str_prog.upper().find(el[0].upper())
        if str_prog.upper().find(el[0].upper()) > -1 :
            if str_sub_repl == '':
                str_sub_repl = el[1]
            str_prog = str_prog[:pos_repl].strip() + ' ' + str_prog[pos_repl + len(el[0]) :].strip()
            break
        else:
            str_sub_repl = ''


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
        str_sintez = str_sintez + ' ' + str_sub_repl

    if not str_sub_name_prog == '':
        str_sintez = str_sintez + ' «' + str_sub_name_prog +'»'

    if not str_prog == '':
        if str_sub_name_prog == '':
                str_sintez = str_sintez + ' ' + deCapsLock(str_prog)

    if not str_sintez.strip()[-1]=='.':
        str_sintez = str_sintez + '.'


    if not str_sub_vozrast == '':
        str_sintez = str_sintez + ' ^' + str_sub_vozrast


    Rezult = str_sintez.strip()

    return Rezult

