import pandas as pd


class CarInfoDb:
    def __init__(
        self, filename="/home/saharul/Projects/csa_ver3/data/carinfo_master.csv"
    ):
        self.dbfilename = filename

    def GetModelId(self, model):

        if type(model) != str:
            raise TypeError("Car Model must be in str")

        if len(model) == 0:
            raise ValueError("Car Model cannot be empty")

        # read file car_info.csv
        df = pd.read_csv(self.dbfilename)

        # check model name contains the given string and to ignore case
        # df1 = df[df['Model'].str.contains("(?i)" + model)]
        df1 = df[df["Model"] == model]

        if df1.empty or len(model) == 0:
            return 1
        else:
            # get the id value
            return df1.iloc[0]["Id"]

    # function to get car information by is id in the db
    def GetCarInfoById(self, car_id):
        carinfolist = self.ListCarInfo()

        if type(car_id) != str:
            raise TypeError("car id must be type str")

        for car in carinfolist:
            if car[0] == str(car_id):
                return car

    # function to view all the car model in the csv file
    """ will return car informatio i.e

        ['2', 'EXORA 1.6 (A)', 'AGU4004', '', '', '', 'SILVER', 'SAHARUL']

    """
    def ListCarInfo(self):
        carinfolist = []
        with open(self.dbfilename, "r") as f:
            for line in f:
                line = line.rstrip()
                carinfo = line.split(",", 8)
                if not line:
                    continue
                if carinfo[0] == "Id":
                    continue
                carinfolist.append(carinfo)  # add car information
        return carinfolist

    # function to ask user for model to choose from
    # and return back the car info of the chosen model
    def SelectCarInfo(self, defmodel=""):
        carinfolist = self.ListCarInfo()

        # get default model id
        defid = self.GetModelId(defmodel)

        print("\nCHOOSE YOUR CAR MODEL: ")
        for car in carinfolist:
            print(car[0] + ". " + car[1])

        choice = ""
        while True:
            try:
                # ask user to make choice and show the default value as well
                choice = int(
                    input("\nSelect your car model (1,2), default [%s]: " % defid)
                )
                # choice is assigned to user choice  or default value
                choice = choice or defid
                carinfo = carinfolist[choice - 1]
            except IndexError:
                print("\nInvalid Selection!")
                continue
            except ValueError:
                if not choice:  # check if choice empty string (user press 'Enter')
                    carinfo = carinfolist[int(defid - 1)]
                    break
                else:
                    print("\nInvalid Input!")
                    continue
            else:
                # print(carinfo)
                return carinfo

        return carinfo

    # function to view all the car model in the csv file
    def ListCarInfoShort(self):
        carinfolist = []
        with open(self.dbfilename, "r") as f:
            for line in f:
                line = line.rstrip()
                if not line:
                    continue
                carinfo = line.split(",", 8)
                if carinfo[0] == "Id":
                    continue  # skip the header
                carinfolist.append(carinfo[1])
        return carinfolist

    # def get_record(self, record_id):
    #    with open("service_master.csv","r") as f:
    #       for line in f:
    #          line = line.rstrip()
    #          line = line.split(",", 9)
    #          if (line[0] == str(record_id)):
    #             return line


# main function for running the program
def main():
    ci = CarInfoDb()
    print(type(ci.GetModelId("EXORA 1.6 (A)")))
    # print(ci.ListCarInfoShort())
    # print(ci.GetCarInfoById("2"))


# print(ci.GetCarInfoById(2))
# print(ci.GetModelId("EXORA 1.6 (A)"))


if __name__ == "__main__":
    main()
