#!/usr/bin/env python3
import PySimpleGUI as sg
import pandas as pd
import random
import sys
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
win_add_active=False
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
            layout2 = service_layout_edit("edit", records, carinfo, wkshpdb, val_1)

            win_edit = sg.Window(title='Edit Service', size=(800, 600), layout=layout2)
            while True:
                ev_2, val_2 = win_edit.Read()
                #print(event_2, val_3)
                if ev_2 is None or ev_2 == 'Cancel':
                    win_edit.close()
                    win_edit_active = False
                    win_svc.UnHide()
                    break
                elif ev_2 == '-MODEL-':
                    car_members = carinfo.ListCarInfo()
                    for c in car_members:
                        if (c[1] == val_2['-MODEL-']):
                            break
                    win_edit.FindElement('-PLATE-').Update(c[2])
                    win_edit.FindElement('-WKSHP-').SetFocus()

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
        service = ServiceDb()
        rec_id = val_1['-TABLE-'][0]+1

        butt = sg.PopupYesNo('Are you sure you want to delete record ' + str(rec_id))
        if butt == "Yes":
            service.delete_record(str(rec_id))
            sg.PopupAutoClose("record successfully deleted.")
            rec_id = 1  # set selected row to first row
            # refresh table
            win_svc['-TABLE-'].Update(values=service.list_all_records2())

        else:
            #sets selected row to value before
            win_svc['-TABLE-'].update(select_rows=(rec_id,rec_id))
    elif ev_1 == 'Add Record' and not win_add_active:

        win_add_active = True
        win_svc.hide()
        try:        

            wkshpdb = WorkshopDb()
            carinfo = CarInfoDb()
            service = ServiceDb()
            rec_id = 1
            records = []

            # ------ Get Edit Service Window Layout ------
            # note must create a layout from scratch every time. No reuse
            layout3 = service_layout_edit("add", records, carinfo, wkshpdb, val_1)
            win_add = sg.Window(title='Add New Service', size=(800, 600), layout=layout3)

            while True:
                ev_3, val_3 = win_add.Read()
                if ev_3 is None or ev_3 == 'Cancel':
                    win_add.close()
                    win_add_active = False
                    win_svc.UnHide()
                    break
                elif ev_3 == 'Ok':
                    win_add.close()
                    service.add_record(val_3['-SVCDATE-'], carinfo.GetModelId(val_3['-MODEL-']), 
                                val_3['-PLATE-'], val_3['-WKSHP-'], val_3['-MILE-'], val_3['-NXTMILE-'], 
                                val_3['-NSVCDATE-'], val_3['-LAB-'], val_3['-AMT-'])
                    sg.PopupAutoClose('Service Record added successfully')
                    win_svc.UnHide()
                    # refresh table
                    win_svc['-TABLE-'].Update(values=service.list_all_records2())

                elif ev_3 == '-MODEL-':
                    car_members = carinfo.ListCarInfo()
                    for c in car_members:
                        if (c[1] == val_3['-MODEL-']):
                            break
                    win_add.FindElement('-PLATE-').Update(c[2])
                    win_add.FindElement('-WKSHP-').SetFocus()

        except Exception:
            e = sys.exc_info()[0]
            sg.PopupAutoClose("Error: %s" % e )            
            win_svc.UnHide()


win_svc.close()

