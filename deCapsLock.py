# проверяем и делаем деКапсЛок
def deCapsLock(str_dcl, lst_CapsWord):
    str_dcl = str_dcl.strip()
    fl_caps = True
    fl_CapsWord = False
    lst_dcl = str_dcl.split(' ')
    tmp_str = ''
    for i, el in enumerate(lst_dcl):

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


        # если слово начинается с кавычек 
        if i>0 and (lst_dcl[i][0]== '«' or lst_dcl[i][0]== '\'') and fl_caps:
            tmp_str = lst_dcl[i][:1].upper()  + lst_dcl[i][2:].lower()

        # если предыдущее слово заканчивается точкой
        elif i>0 and lst_dcl[i-1][-1]=='.':            
            tmp_str = tmp_str + ' ' + lst_dcl[i][0].upper()  + lst_dcl[i][1:].lower() 

        # все прописные
        else:
            tmp_str = tmp_str + ' ' + lst_dcl[i].lower()

    # if fl_caps:
    #     str_dcl = str_dcl[0] + str_dcl[1:].lower()
    str_dcl = tmp_str.strip()
    
    return str_dcl
