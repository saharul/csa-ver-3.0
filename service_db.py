import pandas as pd
import time
import curses
from carinfo_db import CarInfoDb
from workshop_db import WorkshopDb
from collections import namedtuple





class ServiceDb(object):
    def __init__(self, filename="service_master.csv", filename_2="service_parts.csv"):
        self.dbfilename = filename
        self.dbfilename_2 = filename_2


    # FUNCTION TO GET THE MAXIMUM SERVICE ID IN THE DB
    def get_max_id(self):
        with open(self.dbfilename,"r") as f:
            for line in f:
                line = line.rstrip()
                line = line.split(",")
                if not line: continue
            return(int(line[0]))


    # FUNCTION TO GET THE MAXIMUM SERVICE ID IN THE DB
    def get_max_part_id(self):
        with open(self.dbfilename_2,"r") as f:
            for line in f:
                line = line.rstrip()
                line = line.split(",")
                if not line: continue
            return(int(line[0]))


    # FUNCTION TO SAVE SERVICE TO FILE
    def save_record(self, new_record):
        f = open(self.dbfilename,"a+")
        f.write(new_record[0] + ',' + new_record[1] + ',' + new_record[2] + ',' +
            new_record[3] + ',' + new_record[4] + ',' + new_record[5] + ',' + new_record[6] + ',' + new_record[7] + ',' +
            new_record[8] + ',' + new_record[9] + '\n')
        f.close()



    # function to add service record to the csv db
    def add_record(self,  service_date = '', car_id = '', plate = '', workshop = '', 
                        mileage = '', nxt_mileage = '', nxt_date = '', labour_cost = '', amount = ''):
        ci = CarInfoDb()
    	# create a new service id
        record_id = str(self.get_max_id() + 1)
        car = ci.GetCarInfoById(car_id[0]+1)
        model = car[1]
        plate = car[2]
        service_center = workshop
        record = namedtuple("record", "record_id service_date model plate svc_center mileage nxt_mileage nxt_date labour_cost amount")
        new_record = record(record_id, service_date, model, plate, 
    							service_center, mileage, nxt_mileage, nxt_date, labour_cost, amount)
        self.save_record(new_record)


    # FUNCTION TO SAVE SPARE PART SERVICE TO FILE
    def save_part_record(self, new_record):
        # f = open(self.dbfilename_2,"a+")
        # f.write(new_record[0] + ',' + new_record[1] + ',' + new_record[2] + ',' +
        #     new_record[3] + ',' + new_record[4] + ',' + new_record[5] + ',' + new_record[6] + ',' + new_record[7] + '\n')
        # f.close()
        
        # Open dataframe from csv_file
        df = pd.read_csv(self.dbfilename_2)
        
        df_newrow = pd.DataFrame({
        "Id": [new_record[0]],
        "SvcId":[new_record[1]], 
        "Date":[new_record[2]], 
        "Name": [new_record[3].upper()], 
        "Qty": [new_record[4]],
        "UnitPrice": ["{:.2f}".format(float(new_record[5]))],
        "Disc": ["{:.2f}".format(float(new_record[6]))],
        "Amount": ["{:.2f}".format(float(new_record[7]))] })
        
        # # Append new row to dataframe
        df = df.append(df_newrow, ignore_index=True, sort=False)

        # sort the dataset
        df.sort_values(['Id', 'SvcId', 'Name'])

        # # Write back new dataframe to csv file
        df.to_csv (r'service_parts.csv', index = False, header=True)
   
 
    def add_part_record(self, svc_id = '', svc_date = '', part_name = '', qty = '', unit_price ='',
                              discount = '', amount = ''):
        record_id = str(self.get_max_part_id() + 1)
        part_record = namedtuple("part_record", "id svc_id svc_date part_name qty unit_price discount amount")
        new_record = part_record(record_id, svc_id, svc_date, part_name, qty, unit_price, discount, amount)
        self.save_part_record(new_record)



    def update_part_record(self, record_id = '', svc_id = '', svc_date = '', part_name = '', qty = '',
                              unit_price = '', discount = '', amount = ''):
    	# reading the contacts csv file
    	df = pd.read_csv(self.dbfilename_2, index_col="Id")
    	df.at[record_id, 'Date'] = svc_date
    	df.at[record_id, 'Name'] = part_name
    	df.at[record_id, 'Qty'] = qty
    	df.at[record_id, 'UnitPrice'] = unit_price
    	df.at[record_id, 'Disc'] = discount
    	df.at[record_id, 'Amount'] = amount

    	df.to_csv (self.dbfilename_2, index=True, header=["SvcId","Date", "Name", "Qty", "UnitPrice","Disc", "Amount"], 
                        float_format='%.2f')



    def update_record(self, record_id,  service_date = '', car_id = '', plate = '', workshop = '', 
                            mileage = '', nxt_mileage = '', nxt_date = '', labour_cost = '', amount = ''):
    	ci = CarInfoDb()
    	# reading the contacts csv file
    	df = pd.read_csv(self.dbfilename, index_col="SvcId")
    	df.at[record_id, 'SvcDate'] = service_date
    	car = ci.GetCarInfoById(car_id)
    	df.at[record_id, 'Model'] = car[1]
    	df.at[record_id, 'Plate'] = car[2]
    	df.at[record_id, 'Workshop'] = workshop
    	df.at[record_id, 'Mileage'] = mileage
    	df.at[record_id, 'Nxt_Mileage'] = nxt_mileage
    	df.at[record_id, 'Nxt_Date'] = nxt_date
    	df.at[record_id, 'Labor'] = labour_cost
    	df.at[record_id, 'Amount'] = amount

    	df.to_csv ("service_master.csv", index=True, header=["SvcDate", "Model", "Plate", "Svc_Center","Mileage",
                        "Nxt_Mileage", "Nxt_Date", "Labor", "Amount"], float_format='%.2f')
       

    def delete_record(self, record_id):
      f = open(self.dbfilename,"r+")
      d = f.readlines()
      f.seek(0)
      for line in d:
         record = line.rstrip()
         svc_id, svc_date, model, plate, svc_center, mileage, nxt_mileage, nxt_date, labour, amount = line.split(",")
         if svc_id != record_id:
            f.write(line)
            f.truncate()
      f.close()



    def get_record(self, record_id):
       with open(self.dbfilename,"r") as f:
          for line in f:
             line = line.rstrip()
             line = line.split(",", 9)
             if (line[0] == str(record_id)):
                return line



    def get_record_parts_prev(self, record_id):
        records = []
        # reading the service csv file
        df = pd.read_csv("service_parts.csv", index_col=False)
        df = df[df.SvcId == int(record_id)]

        # sort dataframe by SvcId and Part Name
        df_sel = df.sort_values(['SvcId', 'Name'])

        # # reset index to newindex list
        newindex = [''] * len(df_sel)  # set newindex array size
        for i in range(len(df_sel)):
            newindex[i] = i  #set index column
        df_sel.index = newindex
        # # set index name to Key
        df_sel.index.name='No'

        header = ["No","SvcId", "Date", "Name", "Qty", "UnitPrice", "Disc", "Amount"]
        records.append(header)
        for i in range(0, len(df_sel)):
            a = df_sel.iloc[i].values.tolist()
            b = [i]
            c = b + a
            records.append(c)
            #records.append(df_sel.iloc[i].values.tolist())

        return(records)


    def get_record_parts(self, record_id):
        records = []
        # reading the service csv file
        df = pd.read_csv("service_parts.csv", index_col=False)
        df = df[df.SvcId == int(record_id)]

        header = ["Id","SvcId", "Date", "Name", "Qty", "UnitPrice", "Disc", "Amount"]
        records.append(header)
        for i in range(0, len(df)):
            a = df.iloc[i].values.tolist()
            a[5] = "{:.2f}".format(float(a[5]))
            a[6] = "{:.2f}".format(float(a[6]))
            a[7] = "{:.2f}".format(float(a[7]))
            # c = b + a
            records.append(a)
        return(records)


    def get_one_record_part(self, record_id):
        records = []

        # reading the service csv file
        df = pd.read_csv("service_parts.csv", index_col=False)
        df = df[df.Id == int(record_id)]
        for i in range(0, len(df)):
            records = df.iloc[i].values.tolist()

        return(records)



    def list_all_records2(self,):
        # reading the service csv file
        df = pd.read_csv(self.dbfilename, index_col=False, header=None)
        #df = df[df["SvcId"] != 0]
        # convert column "a" to int64 dtype and "b" to complex type
        #df = df.astype({"Mileage": int, "Nxt_Mileage": int, "Amount": float})
        records = df.values.tolist()
        return(records)


    def list_all_records(self,):
        records = []
        # reading the service csv file
        df = pd.read_csv(self.dbfilename, index_col=False, header=0)
        df = df[df["SvcId"] != 0]
        # convert column "a" to int64 dtype and "b" to complex type
        df = df.astype({"Mileage": int, "Nxt_Mileage": int, "Amount": float})
        cols_to_drop = ["Plate"] # drop cols 3 and 5
        df = df.drop(cols_to_drop, axis=1)
        
        records.append(["svc_id", "svc_date", "model", "svc_shop", "mileage", "nxt_mile", "nxt_date","labour", "amount"])
        for i in range(1, len(df)+1):
            records.append(df.loc[i].values.tolist())   #df.to_numpy()
        # for i, x in enumerate(records[:,7]):
        #     records[i, 7] = "{:.2f}".format(x)
        #     records[i, 6] = "{:.2f}".format(records[i,6])
        # #records = df.to_numpy()
        return(records)


    def list_all_records_old(self,):
        records = []
        with open(self.dbfilename,"r") as f:
            for line in f:
                linerec = ['','','','','','','','','','']
                line = line.rstrip()
                svc_id, svc_date, model, plate, svc_center, mileage, nxt_mileage, nxt_date, labour, amount = line.split(",")
                linerec[0], linerec[1], linerec[2], linerec[3], linerec[4], linerec[5], linerec[6],\
                linerec[7], linerec[8], linerec[9] = svc_id, svc_date, model, plate, svc_center, mileage, nxt_mileage,\
                nxt_date, labour, amount
                if (linerec[0] == '0') : continue
                if (linerec[5] == 'Mileage'):
                    pass
                else:
                    linerec[5] = "{:.0f}".format(float(linerec[5]))
                    linerec[6] = "{:.0f}".format(float(linerec[6]))
                records.append(linerec)
                 
        return(records)
    

    def list_all_part_records(self,):
        records = []
        # reading the service csv file
        df = pd.read_csv("service_parts.csv", index_col=False, header=0)
        
        records.append(["SvcId", "Date", "Name", "Qty", "UnitPrice", "Disc", "Amount"])
        for i in range(1, len(df)):
            records.append(df.loc[i].values.tolist())   #df.to_numpy()
        # for i, x in enumerate(records[:,7]):
        #     records[i, 7] = "{:.2f}".format(x)
        #     records[i, 6] = "{:.2f}".format(records[i,6])
        # #records = df.to_numpy()
        return(records)


    def delete_part_record(self, record_id):

        # reading the service csv file
        df = pd.read_csv("service_parts.csv", index_col=False)
        # remove the row
        df1 = df[df.Id != int(record_id)]

        # write back the changes to file
        df1.to_csv ("service_parts.csv", index = False, header=True)

    def show_parts(self):
        df = pd.read_csv(self.dbfilename_2)
        df = df.sort_values(['Name'])
		
		# dropping ALL duplicte values 
        df.drop_duplicates(subset ="Name", keep = "first", inplace = True)
		
		# reset index to newindex list
        newindex = [''] * len(df)  # set newindex array size
        for i in range(len(df)):
           newindex[i] = i  #set index column
        df.index = newindex
        df.index.name = "Key"
		
        df = df[["Name"]]
        
        records = []
        for i in range(1, len(df)):
            b = df.loc[i].values.tolist()
            records += b
        return(records)
			
