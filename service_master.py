#!/usr/bin/env python3
import PySimpleGUI as sg
import pandas as pd
import random
import sys
import string
from service_db import ServiceDb
from workshop_db import WorkshopDb
from carinfo_db import CarInfoDb
from layout import service_layout, service_layout_edit, service_layout_spart
from layout import spart_layout_edit

"""
    Screen Car Service Management
"""
# Screen Theme
sg.change_look_and_feel('Light Green 1')

# ------ Make the Table Data ------
svc_db = ServiceDb()
data = svc_db.list_all_records2()

# ------ Get Service Screen Window Layout ------
layout = service_layout(data)

# ------ Create Window ------
win_svc = sg.Window('My Car Service History', layout, size=(1000,600), resizable=False).Finalize()

win_edit_active=False
win_add_active=False
win_part_active=False
row_id = 1
# ------ Event Loop ------
while True:
    if row_id == 0: row_id = 1
    win_svc.FindElement('-TABLE-').update(select_rows=(row_id-1,row_id-1))
    ev_1, val_1 = win_svc.read()
    #print(event, values)
    if ev_1 is None or ev_1 == 'Exit Program':
        break
    if ev_1 == 'Edit Record' and not win_edit_active:
        win_edit_active = True
        win_svc.hide()
        try:
            # Initialize classes and variables
            wkshpdb = WorkshopDb()
            carinfo = CarInfoDb()
            service = ServiceDb()
            row_id = val_1['-TABLE-'][0]+1
            records = service.get_record(row_id)

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
                    service.update_record(row_id, val_2['-SVCDATE-'], carinfo.GetModelId(val_2['-MODEL-']), 
                               val_2['-PLATE-'], val_2['-WKSHP-'], val_2['-MILE-'], val_2['-NXTMILE-'], 
                               val_2['-NSVCDATE-'], val_2['-LAB-'], val_2['-AMT-'])
                    sg.PopupAutoClose('Service was updated.')
                    win_edit.Close()
                    win_svc.UnHide()
                    # refresh table
                    win_svc['-TABLE-'].Update(values=service.list_all_records2())
                    # retain selected row
                    win_svc['-TABLE-'].update(select_rows=(row_id-1,row_id-1))
                  
        except IndexError:
            win_svc.UnHide()
            sg.PopupError('Please select a record to edit')
            win_edit_active = False
    elif ev_1 == 'Delete Record':
        rec_id = val_1['-TABLE-'][0]+1

        butt = sg.PopupYesNo('Are you sure you want to delete record ' + str(rec_id))
        if butt == "Yes":
            svc_db.delete_record(str(rec_id))
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
    elif ev_1 == 'Service Parts' and not win_part_active:
        win_svc.Hide()

        # Initialize classes and variables
        wkshpdb = WorkshopDb()
        carinfo = CarInfoDb()
        #service = ServiceDb()
        row_id = val_1['-TABLE-'][0]
        service_rec = svc_db.get_service_record(row_id)
        svc_id = service_rec[0]
        sparts_rec = svc_db.get_record_parts(svc_id)
        win_spart_edit_active = False
        win_spart_add_active = False

        # check if there is empty or no spare part for the service id
        if sparts_rec == []: sparts_rec = [["", "", "", "", "", "", ""]]
            # sg.PopupAutoClose('No Spare Parts found!')
            # win_svc.UnHide()
            # continue

        # ------ Get Spare Part Window Layout ------
        layout = service_layout_spart(sparts_rec, service_rec, carinfo, wkshpdb, val_1)

        # ------ Create Window ------
        win_spart = sg.Window('Spare Parts Info', layout, size=(700,600), resizable=False).Finalize()
        row_id = 0
        while True:
            win_spart.FindElement('-PTABLE-').update(select_rows=(row_id,row_id))
            ev_4, val_4 = win_spart.read()
            #print(event, values)
            if ev_4 is None or ev_4 == 'Close':
                win_spart.Close()
                win_part_active = False
                win_svc.UnHide()
                break
            elif ev_4 == "Edit Part" and not win_spart_edit_active:
                # if record empty, abort the task.
                if sparts_rec == [["","","","","","",""]]:
                    sg.PopupAutoClose('Empty record!')
                    continue

                try:
                    row_id = val_4['-PTABLE-'][0]
                    #print('svc_id: ' + str(svc_id), 'row_id ' + str(row_id))
                    sparts_one_rec = svc_db.get_one_record_part(svc_id, row_id)

                    # get spare part data
                    part_data = svc_db.show_parts()
                    win_spart.Hide()
                    win_spart_edit_active = True

                    # ------ Get Spare Part Edit Window Layout ------
                    layout = spart_layout_edit("edit", sparts_one_rec, part_data)

                    # ------ Open the Spare Part Edit Window  ------
                    win_spart_edit = sg.Window('Edit Spare Parts', layout, size=(700,600), resizable=False).Finalize()
                    while True:
                        ev_5, val_5 = win_spart_edit.Read()
                        
                        if ev_5 is None or ev_5 == 'Cancel':
                            win_spart_edit.Close()
                            win_spart_edit_active = False
                            win_spart.UnHide()
                            break
                        elif ev_5 == 'Update':
                            win_spart_edit.Close()      # close window spare part edit
                            win_spart_edit_active = False   # set flag window spare part active = False
                            # update spare part record
                            svc_db.update_part_record(int(val_5['-PID-']), val_5['-SID-'], val_5['-SVCDATE-'], val_5['-PNAME-'], 
                                                val_5['-QTY-'], val_5['-PRICE-'], val_5['-DISC-'], val_5['-AMT-'])
                            # display popup message 
                            sg.PopupAutoClose('Spare Part record updated successfully')
                            # refresh spare part Table
                            win_spart['-PTABLE-'].Update(values=svc_db.get_record_parts(svc_id))
                            # show window spare part view
                            win_spart.UnHide()
                except Exception:
                    e = sys.exc_info()[0]
                    sg.PopupAutoClose("Error: %s" % e )            
                    win_svc.UnHide()
            elif ev_4 == "Add Part" and not win_spart_add_active:
                    win_spart.Hide()
                    win_spart_add_active = True
                    sparts_one_rec = [["", svc_id, service_rec[1], "", "", "", ""]]
                    # get spare part data
                    part_data = svc_db.show_parts2()

                    # ------ Get Spare Part Edit Window Layout ------
                    layout = spart_layout_edit("add", sparts_one_rec, part_data)

                    # ------ Open the Spare Part Edit Window  ------
                    win_spart_add = sg.Window('Add Spare Parts', layout, size=(700,600), resizable=False).Finalize()
                    while True:
                        ev_6, val_6 = win_spart_add.Read()
                        
                        # user click 'Cancel' button or 'X'
                        if ev_6 is None or ev_6 == 'Cancel':
                            # close window spare part add
                            win_spart_add.Close()
                            # set flag to false
                            win_spart_add_active = False
                            # show again window spare part view
                            win_spart.UnHide()
                            break
                        elif ev_6 == 'Save':
                            win_spart_add.Close()      # close window spare part edit
                            win_spart_add_active = False   # set flag window spare part active = False
                            # save the new spare part record
                            svc_db.add_part_record(val_6['-SID-'], val_6['-SVCDATE-'], val_6['-PNAME-'], 
                                                val_6['-QTY-'], val_6['-PRICE-'], val_6['-DISC-'], val_6['-AMT-'])

                            # display popup message 
                            sg.PopupAutoClose('Spare Part record added successfully')
                            # refresh spare part Table
                            win_spart['-PTABLE-'].Update(values=svc_db.get_record_parts(svc_id))
                            # show window spare part view
                            win_spart.UnHide()                            
            elif ev_4 == "Delete Part":

                # if record empty, abort the task.
                if sparts_rec == [["","","","","","",""]]:
                    sg.PopupAutoClose('Nothing to delete!')
                    continue

                row_id = val_4['-PTABLE-'][0]
                sparts_one_rec = svc_db.get_one_record_part(svc_id, row_id)

                butt = sg.PopupYesNo('Are you sure you want to delete record part id ' + str(sparts_one_rec[0]))
                if butt == "Yes":
                    svc_db.delete_part_record(sparts_one_rec[0])
                    sg.PopupAutoClose("record successfully deleted.")

                    # check if there is empty or no spare part in the window
                    # after deletion
                    sparts_rec = svc_db.get_record_parts(svc_id)
                    if sparts_rec == []: 
                       sparts_rec = [["", "", "", "", "", "", ""]]  # create empty row.
                       row_id = 0  # set selected row to first row
                    
                    # refresh table
                    win_spart['-PTABLE-'].Update(values=sparts_rec)

win_svc.close()

