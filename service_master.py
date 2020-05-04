#!/usr/bin/env python3
import PySimpleGUI as sg
import pandas as pd
import random
import string
from service_db import ServiceDb
from workshop_db import WorkshopDb
from carinfo_db import CarInfoDb

"""
    Basic use of the Table Element
"""

sg.change_look_and_feel('Light Green 1')
#df = pd.read_csv("service_master.csv", sep=',', engine='python', header=None)

# ------ Make the Table Data ------
svc_db = ServiceDb()
data = svc_db.list_all_records2()
#header_list = data[0:1][0]
header_list = ("SvcId","SvcDate","Model","Plate","Workshop","Mileage","Nxt_Mileage","Nxt_Date","Labor","Amount")
# data = df.values.tolist()               
# read everything else into a list of rows
# Uses the first row (which should be column names) as columns names
# read everything else into a list of rows
#header_list = df.iloc[0].tolist()



# ------ Window Layout ------
layout = [[sg.Table(values=data[0:][:],headings=header_list, max_col_width=25, background_color='lightblue',
                    auto_size_columns=True,
                    display_row_numbers=False, 
                    justification='left',
                    num_rows=20,
                    alternating_row_color='lightyellow',
                    key='-TABLE-',
                    tooltip='This is a table')],
          [sg.Button('Add Record'), sg.Button('Edit Record'), sg.Button('Delete Record'), sg.Button('Exit')]]
        #   [sg.Text('Add Record = read which rows are selected')],
        #   [sg.Text('Edit Record = double the amount of data in the table')],
        #   [sg.Text('Delete Record = Changes the colors of rows 8 and 9')]]

# ------ Create Window ------
win_svc = sg.Window('My Car Service History', layout, size=(1000,600), resizable=False).Finalize()
#win_svc.Maximize()

win_edit_active=False
rec_id = 1
# ------ Event Loop ------
while True:
    win_svc.FindElement('-TABLE-').update(select_rows=(rec_id-1,rec_id-1))
    event_1, values_1 = win_svc.read()
    #print(event, values)
    if event_1 is None or event_1 == 'Exit':
        break
    if event_1 == 'Edit Record' and not win_edit_active:
        win_edit_active = True
        win_svc.hide()
        
        try:

            wkshpdb = WorkshopDb()
            carinfo = CarInfoDb()
            service = ServiceDb()
            rec_id = values_1['-TABLE-'][0]+1
            records = service.get_record(rec_id)
            # removing decimal point from mileage
            s = records[5]
            records[5] = s[:s.index('.')]
            # removing decimal point from next mileage
            p = records[6]
            records[6] = p[:p.index('.')]

            # note must create a layout from scratch every time. No reuse
            layout2 = [[sg.Text('Service No ' + str(values_1['-TABLE-'][0]+1,), pad=(5,0), font=('Any 11'))],
                        [sg.Text('-'*150)],
                        [sg.Text('Service Date'), sg.In(records[1], size=(20,1), key='-SVCDATE-'),
                        sg.CalendarButton('calendar', target='-SVCDATE-', format='%d/%m/%Y', pad=(0,0))],
                    [sg.Text('Car Model'), sg.Combo(carinfo.ListCarInfoShort(), key='-MODEL-', change_submits=True, default_value=records[2], pad=(20,10), size=(20,1)),
                    sg.Text('Plate No'), sg.Input(records[3], size=(20,10), disabled=True, key='-PLATE-')],
                    [sg.Text('Workshop'), sg.Combo(wkshpdb.ListWkshpInfoShort(), default_value=records[4], key='-WKSHP-', pad=(20,10))],
                    [sg.Text('-'*150)],
                    [sg.Text('Mileage', pad=(19,1), justification='left'), sg.Input(records[5], key='-MILE-', size=(20,1)), sg.Text('Next Mileage'), sg.In(records[6], key='-NXTMILE-', size=(20,1))],
                    [sg.Text('Next Date', pad=(11,1)), sg.Input(records[7], size=(20,1), key='-NSVCDATE-'), 
                    sg.CalendarButton('calendar', target='-NSVCDATE-', format='%d/%m/%Y', pad=(0,0))],
                    [sg.Text('-'*150)],
                    [sg.Text('Labour', pad=(22,1)), sg.Input(records[8], size=(20,1), key='-LAB-'), sg.Text('Amount', pad=(20,0)), sg.Input(records[9], key='-AMT-', size=(20,1))],
                    [sg.Text(''*100)],
                    [sg.Text(''*150), sg.Button('Update'), sg.Button('Cancel')]]

            win_edit = sg.Window(title='Edit Service', size=(800, 600),
                                layout=layout2)
            while True:
                event_2, values_2 = win_edit.Read()
                #print(event_2, values_2)
                if event_2 is None or event_2 == 'Cancel':
                    win_edit.close()
                    win_edit_active = False
                    win_svc.UnHide()
                    break
                elif event_2 == 'Update':
                    svc_date = values_2['-SVCDATE-']
                    car_mdel = values_2['-MODEL-']
                    car_mdel_id = carinfo.GetModelId(values_2['-MODEL-'])
                    #print('car model id :' + str(car_mdel_id))
                    plate_no = values_2['-PLATE-']
                    wkshp = values_2['-WKSHP-']
                    mileage = values_2['-MILE-']
                    nxtmile = values_2['-NXTMILE-']
                    nsvc_date = values_2['-NSVCDATE-']
                    labour = values_2['-LAB-']
                    amount = values_2['-AMT-']
                    service.update_record(rec_id, svc_date, car_mdel_id, plate_no, wkshp, mileage, nxtmile, nsvc_date, labour, amount)
                    sg.Popup('Service was updated.')
                    win_edit.Close()
                    win_svc.UnHide()
                    win_svc['-TABLE-'].Update(values=service.list_all_records2())
                    win_svc['-TABLE-'].update(select_rows=(rec_id-1,rec_id-1))
                   

        except IndexError:
            win_svc.UnHide()
            sg.PopupError('Please select a record to edit')
            win_edit_active = False
    elif event_1 == 'Delete Record':
        win_svc.FindElement('-TABLE-').update(select_rows=(3-1,4-1,8-7))
        #win_svc['-TABLE-'].update(row_colors=((8, 'white', 'red'), (9, 'green')))

win_svc.close()

