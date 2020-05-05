#!/usr/bin/env python3
import PySimpleGUI as sg
import pandas as pd
import random
import string
from service_db import ServiceDb
from workshop_db import WorkshopDb
from carinfo_db import CarInfoDb
from layout import service_layout, service_layout_edit

"""
    Screen Car Service Management
"""
# Screen Theme
sg.change_look_and_feel('Light Green 1')

# ------ Make the Table Data ------
svc_db = ServiceDb()
data = svc_db.list_all_records2()

# ------ Get Service Window Layout ------
layout = service_layout(data)

# ------ Create Window ------
win_svc = sg.Window('My Car Service History', layout, size=(1000,600), resizable=False).Finalize()
#win_svc.Maximize()

win_edit_active=False
rec_id = 1
# ------ Event Loop ------
while True:
    win_svc.FindElement('-TABLE-').update(select_rows=(rec_id-1,rec_id-1))
    ev_1, val_1 = win_svc.read()
    #print(event, values)
    if ev_1 is None or ev_1 == 'Exit':
        break
    if ev_1 == 'Edit Record' and not win_edit_active:
        win_edit_active = True
        win_svc.hide()
        try:
            # Initialize classes and variables
            wkshpdb = WorkshopDb()
            carinfo = CarInfoDb()
            service = ServiceDb()
            rec_id = val_1['-TABLE-'][0]+1
            records = service.get_record(rec_id)

            # ------ Get Edit Service Window Layout ------
            # note must create a layout from scratch every time. No reuse
            layout2 = service_layout_edit(records, carinfo, wkshpdb, val_1)

            win_edit = sg.Window(title='Edit Service', size=(800, 600),
                                layout=layout2)
            while True:
                ev_2, val_2 = win_edit.Read()
                #print(event_2, val_2)
                if ev_2 is None or ev_2 == 'Cancel':
                    win_edit.close()
                    win_edit_active = False
                    win_svc.UnHide()
                    break
                elif ev_2 == 'Update':
                    service.update_record(rec_id, val_2['-SVCDATE-'], carinfo.GetModelId(val_2['-MODEL-']), 
                               val_2['-PLATE-'], val_2['-WKSHP-'], val_2['-MILE-'], val_2['-NXTMILE-'], 
                               val_2['-NSVCDATE-'], val_2['-LAB-'], val_2['-AMT-'])
                    sg.PopupAutoClose('Service was updated.')
                    win_edit.Close()
                    win_svc.UnHide()
                    # refresh table
                    win_svc['-TABLE-'].Update(values=service.list_all_records2())
                    # retain selected row
                    win_svc['-TABLE-'].update(select_rows=(rec_id-1,rec_id-1))
                  
        except IndexError:
            win_svc.UnHide()
            sg.PopupError('Please select a record to edit')
            win_edit_active = False
    elif ev_1 == 'Delete Record':
        win_svc.FindElement('-TABLE-').update(select_rows=(3-1,4-1,8-7))
        #win_svc['-TABLE-'].update(row_colors=((8, 'white', 'red'), (9, 'green')))

win_svc.close()

