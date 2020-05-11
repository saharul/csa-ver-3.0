    
import PySimpleGUI as sg


def is_valid_number(valwin_chknum_list):

    is_valid = True

    for v in valwin_chknum_list:
        # if last char entered not a digit
        if len(v[0]) and v[0][-1] not in ('0123456789'):
            # delete last char from input
            v[1].update(v[0][:-1])
            is_valid = False
    
    return(is_valid)


def is_valid_float(valwin_chkfloat_list):

    is_float = True

    for v in valwin_chkfloat_list:
        try:
            _in_as_float = float(v[0])
        except:
            if ((len(v[0]) == 1 and v[0][0] == '-') or len(v[0]) == 0):
                continue
            v[1].update(v[0][:-1])
            is_float = False
            # sg.PopupAutoClose('error')

    return(is_float)


def is_field_empty(val_chkempty_list):
    is_empty = False
    msg = ""

    for v in val_chkempty_list:
        if len(v[0].strip()) == 0:
            msg += v[1] + " is empty\n"
            is_empty = True
    
    if not len(msg) == 0:
        sg.PopupAutoClose(msg)

    return(is_empty)

