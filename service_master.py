#!/usr/bin/env python3
import PySimpleGUI as sg
import pandas as pd
import random
import string
from service_db import ServiceDb
from workshop_db import WorkshopDb

"""
    Basic use of the Table Element
"""

sg.change_look_and_feel('Light Green 1')
#df = pd.read_csv("service_master.csv", sep=',', engine='python', header=None)

# ------ Make the Table Data ------
svc_db = ServiceDb()
data = svc_db.list_all_records2()
header_list = data[0:1][0]
# data = df.values.tolist()               
# read everything else into a list of rows
# Uses the first row (which should be column names) as columns names
# read everything else into a list of rows
#header_list = df.iloc[0].tolist()



# ------ Window Layout ------
layout = [[sg.Table(values=data[2:][:], headings=header_list, max_col_width=25, background_color='lightblue',
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
win_svc = sg.Window('My Car Service History', layout, size=(800,600), resizable=False).Finalize()
#win_svc.Maximize()

win_add_active=False
# ------ Event Loop ------
while True:
    win_svc.FindElement('-TABLE-').update(select_rows=(0,0))
    event_1, values_1 = win_svc.read()
    #print(event, values)
    if event_1 is None or event_1 == 'Exit':
        break
    if event_1 == 'Edit Record' and not win_add_active:
        win_add_active = True
        win_svc.hide()
        
        try:

            wkshpdb = WorkshopDb()
            # note must create a layout from scratch every time. No reuse
            layout2 = [[sg.Text('Service Date'), sg.In(size=(20,1), key='-SVCDATE-'),
                        sg.CalendarButton('calendar', target='-SVCDATE-', format='%d-%m-%Y')],
                    [sg.Text('Car Model'), sg.Combo(('BEZZA 1300 X (AUTO)', 'EXORA 1.6 (A)'), pad=(20,0), size=(20,1)),
                    sg.Text('Plate No'), sg.Input(size=(20,1))],
                    [sg.Text('Workshop'), sg.Combo(wkshpdb.ListWkshpInfoShort(), key='-WKSHP-', pad=(20,10))],
                    [sg.Text('_'*100)],
                    [sg.Text('Mileage', pad=(19,1), justification='left'), sg.Input(size=(20,1)), sg.Text('Next Mileage'), sg.In(size=(20,1))],
                    [sg.Text('Next Date', pad=(11,1)), sg.Input(size=(20,1), key='-NSVCDATE-'), 
                    sg.CalendarButton('calendar', target='-NSVCDATE-', format='%d-%m-%Y')],
                    [sg.Text('_'*100)],
                    [sg.Text('Labour', pad=(22,1)), sg.Input(size=(20,1)), sg.Text('Amount', pad=(20,0)), sg.Input(size=(20,1))],
                    [sg.Text(''*100)],
                    [sg.Text(''*150), sg.Button('Ok'), sg.Button('Cancel')]]

            win_add = sg.Window(title='Edit Service Id: ' + str(values_1['-TABLE-'][0]+1), size=(800, 600),
                                layout=layout2)
            while True:
                event_2, values_2 = win_add.Read()
                #print(event_2, values_2)
                if event_2 is None or event_2 == 'Cancel':
                    win_add.close()
                    win_add_active = False
                    win_svc.UnHide()
                    break
        except IndexError:
            win_svc.UnHide()
            sg.PopupError('Please select a record to edit')
            win_add_active = False
    elif event_1 == 'Delete Record':
        win_svc.FindElement('-TABLE-').update(select_rows=(3-1,4-1,8-7))
        #win_svc['-TABLE-'].update(row_colors=((8, 'white', 'red'), (9, 'green')))

win_svc.close()

