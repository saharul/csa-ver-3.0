import pandas as pd


class WorkshopDb():
    def __init__(self, filename="workshop_master.csv"):
        self.dbfilename = filename


    def GetWkshpId(self, wkshp):
        # read file car_info.csv
        df = pd.read_csv(self.dbfilename)
    
        # check garage name contains the given string and to ignore case
        # df1 = df[df['Model'].str.contains("(?i)" + model)]
        df1 = df[df['SvcCtrName'] == wkshp]
        
        if df1.empty or len(wkshp) == 0:
            return(1)
        else:
            # get the id value
            return(df1.iloc[0]['Id'])
        


    def GetWkshpInfoById(self, wkshp_id):
        wkshpinfolist = self.ListWkshpInfo()
        for wkshp in wkshpinfolist:
            if (wkshp[0] == str(wkshp_id)):
                return(wkshp)



    # FUNCTION TO VIEW ALL SERVICE CENTER INFO IN THE DATABASE
    def ListWkshpInfo(self):
        wkshpinfolist = []
        with open(self.dbfilename,"r") as f:
            for line in f:
                line = line.rstrip()
                wkshp = line.split(",", 4)
                if not line: continue
                if wkshp[0] == 'Id': continue
                wkshpinfolist.append(wkshp)   # add garage info

        wkshpinfolist.sort(key=lambda x: x[1])
        return(wkshpinfolist)


    def SelectWkshpInfo(self, defwkshp=""):
        wkshpinfolist = self.ListWkshpInfo()

        # get default garage id
        defid = self.GetWkshpId(defwkshp)
        
        print("\nSELECT THE CAR SERVICE CENTER: ")
        for wkshp in wkshpinfolist:
                print(wkshp[0] + ". " + wkshp[1] )

        choice = ""
        while True: 
            try:
                #GET USER CHOICE or use default
                choice = int(input("\nSelect the Service Center (1,2,3 etc):, default [%s]: " %defid))
                choice = choice or defid
                wkshpinfo = wkshpinfolist[choice-1]
            except IndexError:
                print("\nInvalid Selection!")
                continue
            except ValueError:
                if (not choice):    # check if choice empty string (user press 'Enter')
                    wkshpinfo = wkshpinfolist[int(defid-1)]
                    break
                print("\nInvalid Input!")
                continue
            else:
                return(wkshpinfo)   # return shop name of user choice

        return(wkshpinfo)

    # FUNCTION TO VIEW ALL SERVICE CENTER INFO IN THE DATABASE
    def ListWkshpInfoShort(self):
        wkshpinfolist = []
        with open(self.dbfilename,"r") as f:
            for line in f:
                line = line.rstrip()
                wkshp = line.split(",", 4)
                if not line: continue
                if wkshp[0] == 'Id': continue
                wkshpinfolist.append(wkshp[1])   # add garage info

        wkshpinfolist.sort(key=lambda x: x[0])
        return(wkshpinfolist)
    


def main():
    # today = date.today()
    # threemonths = datetime.datetime.now() + relativedelta(months=3)
    # print("Today's date is ", today)
    # print("3 months from today ", threemonths.strftime("%Y-%m-%d"))
    ws = WorkshopDb()
    ws_list = ws.ListWkshpInfo()
    print(ws_list)
    # for i, ws in enumerate(ws_list):
    #     print(str(i+1) + ". " + ws[0] + " " + ws[1])



if __name__ == "__main__":
    main()
