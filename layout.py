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
            [sg.Button('Add Record'), sg.Button('Edit Record'), sg.Button('Delete Record'), sg.Button('Service Parts'), sg.Button('Exit Program')]]
            #   [sg.Text('Add Record = read which rows are selected')],
            #   [sg.Text('Edit Record = double the amount of data in the table')],
            #   [sg.Text('Delete Record = Changes the colors of rows 8 and 9')]]
    return(layout)


def service_layout_edit(mode, service_rec, carinfo, wkshpdb, val_1):
    # Edit Service
    if mode == "edit":
        layout = [[sg.Text('Service No ' + str(val_1['-TABLE-'][0]+1,), pad=(5,0), font=('Any 11'))],
                    [sg.Text('-'*150)],
                    [sg.Text('Service Date'), sg.In(service_rec[1], size=(20,1), key='-SVCDATE-'),
                    sg.CalendarButton('calendar', target='-SVCDATE-', format='%d/%m/%Y', pad=(0,0))],
                [sg.Text('Car Model'), sg.Combo(carinfo.ListCarInfoShort(), key='-MODEL-', change_submits=True, default_value=service_rec[2], pad=(20,10), size=(20,1)),
                sg.Text('Plate No'), sg.Input(service_rec[3], size=(20,10), disabled=True, key='-PLATE-')],
                [sg.Text('Workshop'), sg.Combo(wkshpdb.ListWkshpInfoShort(), default_value=service_rec[4], key='-WKSHP-', pad=(20,10))],
                [sg.Text('-'*150)],
                [sg.Text('Mileage', pad=(19,1), justification='left'), sg.Input(service_rec[5], key='-MILE-', size=(20,1)), sg.Text('Next Mileage'), sg.In(service_rec[6], key='-NXTMILE-', size=(20,1))],
                [sg.Text('Next Date', pad=(11,1)), sg.Input(service_rec[7], size=(20,1), key='-NSVCDATE-'), 
                sg.CalendarButton('calendar', target='-NSVCDATE-', format='%d/%m/%Y', pad=(0,0))],
                [sg.Text('-'*150)],
                [sg.Text('Labour', pad=(22,1)), sg.Input(service_rec[8], size=(20,1), key='-LAB-'), sg.Text('Amount', pad=(20,0)), sg.Input(service_rec[9], key='-AMT-', size=(20,1))],
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

def service_layout_spart(sparts_rec, service_rec, carinfo, wkshpdb, val_1):

    header_list = ("PartId","Date","Name","Qty","UnitPrice","Disc","Amount")
    col = [[sg.Table(values=sparts_rec[0:][:], headings=header_list, max_col_width=20, background_color='lightblue',
            auto_size_columns=False, col_widths=10,
            display_row_numbers=False, 
            justification='right',
            num_rows=20,
            alternating_row_color='lightyellow',
            key='-PTABLE-', hide_vertical_scroll=True,
            tooltip='Service Table')]]

    # ------ Window Layout ------
    layout = [[sg.Text('Service Id ' + str(val_1['-TABLE-'][0]+1,), pad=(5,0), font=('Any 11'))],
                [sg.Text('-'*150)],
                [sg.Text('Service Date'), sg.In(service_rec[1], disabled=True, size=(20,1), key='-SVCDATE-')],
                [sg.Text('Car Model'), sg.Input(service_rec[2], disabled=True, key='-MODEL-', change_submits=True, pad=(20,10), size=(20,1)), sg.Text('Plate No'), sg.Input(service_rec[3], size=(20,10), disabled=True, key='-PLATE-')],
                [sg.Text('Workshop'), sg.Input(service_rec[4], disabled=True, key='-WKSHP-', pad=(20,10))],
                [sg.Text('-'*150)],
                [sg.Text('Mileage', pad=(19,1), justification='left'), sg.Input(service_rec[5], disabled=True, key='-MILE-', size=(20,1)), sg.Text('Next Mileage'), sg.In(service_rec[6], disabled=True, key='-NXTMILE-', size=(20,1))],
                [sg.Text('Next Date', pad=(11,1)), sg.Input(service_rec[7], size=(20,1), disabled=True, key='-NSVCDATE-')], 
                [sg.Text('-'*150)],
                [sg.Text('Labour', pad=(22,1)), sg.Input(service_rec[8], disabled=True, size=(20,1), key='-LAB-'), sg.Text('Amount', pad=(20,0)), sg.Input(service_rec[9], disabled=True, key='-AMT-', size=(20,1))],
                [sg.Text(''*100)], 
                [sg.Column(col, scrollable=True, vertical_scroll_only=False, size=(550,200), justification='center')],
                [sg.Button('Add Part'), sg.Button('Edit Part'), sg.Button('Delete Part'), sg.Button('Close')]]

    return(layout)


def spart_layout_edit(mode, spart_onerec, part_data):

    if mode == 'edit':

        part_id = spart_onerec[0]
        svc_id = spart_onerec[1]
        svc_date = spart_onerec[2]
        part_name = spart_onerec[3]
        qty = spart_onerec[4]
        price = "{:.2f}".format(spart_onerec[5])
        disc = "{:.2f}".format(spart_onerec[6])
        amount = "{:.2f}".format(spart_onerec[7])
        pdata = [p[0] for p in part_data]

        # ------ Spare Part Edit Window Layout ------
        layout = [[sg.Text('Edit Spare Part', pad=(5,0), font=('Consolas 12'))],
                [sg.Text('-'*170)],
                [sg.Text('Part Id', font=('Consolas 11')), sg.Input(part_id, size=(30,1), key=('-PID-'), disabled=True, pad=(45,1)), sg.Text('Svc Id', font=('Consolas 11')), sg.Input(svc_id, size=(30,1), key=('-SID-'), disabled=True)],
                [sg.Text('Service Date',font=('Consolas 11')), sg.Input(svc_date, key=('-SVCDATE-'), disabled=True, size=(30,1))],
                [sg.Text('-' * 170)],
                [sg.Text('Part Name', font=('Consolas 11')), sg.Combo(values=pdata, key=('-PNAME-'), default_value=part_name, pad=(28,0), size=(28,1))],
                [sg.Text('Quantity', font=('Consolas 11')), sg.Input(qty, key=('-QTY-'), size=(30,1), pad=(35,0)), sg.Text('Price', font=('Consolas 11')), sg.Input(price, key=('-PRICE-'), size=(30,1))],
                [sg.Text('Disc (RM)', font=('Consolas 11')), sg.Input(disc, size=(30,1), key=('-DISC-'), pad=(27,0)), sg.Text('Amount', font=('Consolas 11')), sg.Input(amount, key=('-AMT-'), size=(30,1), pad=(5,0))],
                [sg.Text(' '*150)],
                [sg.Button('Update', font=('Consolas 11')), sg.Button('Cancel')]]
    else:
        # get part name value from list of tuples
        data = [p[1] for p in part_data]
        # ------ Spare Part Add Window Layout ------
        layout = [[sg.Text('Add Spare Part', pad=(5,0), font=('Consolas 12'))],
                [sg.Text('-'*170)],
                [sg.Text('Service Id', font=('Consolas 11')), sg.Input(spart_onerec[0][1], disabled=True, size=(30,1), key=('-SID-'), pad=(20,0)),
                        sg.Text('Date',font=('Consolas 11')), sg.Input(spart_onerec[0][2], disabled=True, key=('-SVCDATE-'), size=(30,1), pad=(25,0))],
                [sg.Text('-' * 170)],
                [sg.Text('Part Name', font=('Consolas 11')), sg.Combo(values=data, key=('-PNAME-'), default_value='', pad=(28,0), size=(50,1))],
                [sg.Text('Quantity', font=('Consolas 11')), sg.Input('', key=('-QTY-'), size=(30,1), pad=(35,0)), sg.Text('Price', font=('Consolas 11')), sg.Input('', key=('-PRICE-'), size=(30,1))],
                [sg.Text('Disc (RM)', font=('Consolas 11')), sg.Input('', size=(30,1), key=('-DISC-'), pad=(27,0)), sg.Text('Amount', font=('Consolas 11')), sg.Input('', key=('-AMT-'), size=(30,1), pad=(5,0))],
                [sg.Text(' '*150)],
                [sg.Button('Save', font=('Consolas 11')), sg.Button('Cancel')]]


    return(layout)
   
