import PySimpleGUI as sg

def service_layout(data):
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
    return(layout)


def service_layout_edit(mode, records, carinfo, wkshpdb, values_1):
    # Edit Service
    if mode == "edit":
        layout = [[sg.Text('Service No ' + str(values_1['-TABLE-'][0]+1,), pad=(5,0), font=('Any 11'))],
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
    else:
        # Add New Service
        layout = [[sg.Text('Add New Service ', font=('Any 11'))],
                    [sg.Text('-'*150)],
                    [sg.Text('Service Date'), sg.In('', size=(20,1), key='-SVCDATE-'),
                    sg.CalendarButton('calendar', target='-SVCDATE-', format='%d/%m/%Y', pad=(0,0))],
                [sg.Text('Car Model'), sg.Combo(carinfo.ListCarInfoShort(), key='-MODEL-', change_submits=True, default_value='', pad=(20,10), size=(20,1)),
                sg.Text('Plate No'), sg.Input('', size=(20,10), disabled=True, key='-PLATE-')],
                [sg.Text('Workshop'), sg.Combo(wkshpdb.ListWkshpInfoShort(), default_value='', key='-WKSHP-', pad=(20,10))],
                [sg.Text('-'*150)],
                [sg.Text('Mileage', pad=(19,1), justification='left'), sg.Input('', key='-MILE-', size=(20,1)), sg.Text('Next Mileage'), sg.In('', key='-NXTMILE-', size=(20,1))],
                [sg.Text('Next Date', pad=(11,1)), sg.Input('', size=(20,1), key='-NSVCDATE-'), 
                sg.CalendarButton('calendar', target='-NSVCDATE-', format='%d/%m/%Y', pad=(0,0))],
                [sg.Text('-'*150)],
                [sg.Text('Labour', pad=(22,1)), sg.Input('', size=(20,1), key='-LAB-'), sg.Text('Amount', pad=(20,0)), sg.Input('', key='-AMT-', size=(20,1))],
                [sg.Text(''*100)],
                [sg.Text(''*150), sg.Button('Ok'), sg.Button('Cancel')]]

    return(layout)