import io
import os
import tempfile
import unittest
from collections import namedtuple
from unittest.mock import mock_open, patch, Mock
# from tempfile import TemporaryDirectory as TempDir   # "tempfile" is a module in the standard library
# from testfixtures import TempDirectory

import pandas as pd

class ServiceError(Exception):
    """ Exception class for Service """


class ServiceDb(object):
    def __init__(
        self,
        filename="/home/saharul/Projects/csa_ver3/data/service_master.csv",
        filename_2="/home/saharul/Projects/csa_ver3/data/service_parts.csv",
    ):
        self.dbfilename = filename
        self.dbfilename_2 = filename_2

    def is_number(self, s):
        """ Returns True is string is a number. """
        try:
            float(s)
            return True
        except ValueError:
            return False

    # METHOD TO VALIDATE RECORD INPUT BY USER
    def _validate_input(self, new_record):
        if not isinstance(new_record, tuple):
            raise ServiceError("Invalid input value")

        if not len(new_record) == 10:
            raise ServiceError(f'Input value requires 10 items but "{len(new_record)}" was given')

        for i, itm in enumerate(new_record, start=0):
            if i == 0 and not new_record[i].isdigit():
                raise ServiceError("Svc Id value must be a string of number")
            elif i in (8, 9) and not self.is_number(new_record[i]):
                raise ServiceError("Labor Cost and Amount must be numbers")
            elif not new_record[i]:
                raise ServiceError("Input value of empty string is not allowed")
            elif not type(new_record[i]) is str:
                raise ServiceError("Input value must be all of type string")

    # METHOD TO SAVE SPARE PART SERVICE TO FILE
    def save_part_record(self, new_record):
        # Open dataframe from csv_file
        try:
            df = pd.read_csv(self.dbfilename_2)
            df_newrow = pd.DataFrame(
                {
                    "Id": [new_record[0]],
                    "SvcId": [new_record[1]],
                    "Date": [new_record[2]],
                    "Name": [new_record[3].upper()],
                    "Qty": [new_record[4]],
                    "UnitPrice": ["{:.2f}".format(float(new_record[5]))],
                    "Disc": ["{:.2f}".format(float(new_record[6]))],
                    "Amount": ["{:.2f}".format(float(new_record[7]))],
                }
            )
        except ValueError:
            raise ServiceError("Expected value float for Unit Price/Disc/Amount but was given string")
        except FileNotFoundError:
            raise ServiceError(f'Filepath "{self.dbfilename_2}" was not found')
        except IndexError:
            raise ServiceError("Invalid input value was given")
        # # Append new row to dataframe
        df = df.append(df_newrow, ignore_index=True, sort=False)
        # sort the dataset
        df.sort_values(["Id", "SvcId", "Name"])

        # # Write back new dataframe to csv file
        df.to_csv(self.dbfilename_2, index=False, header=True)
        return(df)

    # METHOD TO SAVE SERVICE TO FILE
    def save_record(self, new_record):

        self._validate_input(new_record)

        try:
            with open(self.dbfilename, "a+") as f:
                f.write(",".join(new_record))
        except FileNotFoundError:
            raise ServiceError(f'File "{self.dbfilename}" was not found')
        # finally:
        #     os.remove(self.dbfilename)


class TestSaveRecord(unittest.TestCase):

    def test_save_record(self):
        expected_text = """SvcId,SvcDate,Model,Plate,Workshop,Mileage,Nxt_Mileage,Nxt_Date,Labor,Amount\n1,line 1,line 2,line 3,line 4,line 5,line 6,line 7,0.00,350.00"""
        # create a temporary file and write some data to it
        file = 'foo_save_record_test.txt'

        self.svcdb = ServiceDb(filename=file)

        with open(file,"w+") as f:
            f.write("SvcId,SvcDate,Model,Plate,Workshop,Mileage,Nxt_Mileage,Nxt_Date,Labor,Amount\n")

        record = namedtuple(
            "record",
            "record_id service_date model plate workshop mileage nxt_mileage nxt_date labor amount")
        new_record = record('1', 'line 1', 'line 2', 'line 3', 'line 4', 'line 5', 'line 6',
                                'line 7', '0.00', '350.00')
        try:
            self.svcdb.save_record(new_record)

            with open(file, 'r') as f:
                text = f.read()
        finally:
            os.remove(file)

        self.assertEqual(expected_text, text)

    def test_save_record_with_patch(self):
        record = namedtuple(
            "record",
            "record_id service_date model plate workshop mileage nxt_mileage nxt_date labor amount")

        new_record = record('1', 'line 1', 'line 2', 'line 3', 'line 4', 'line 5', 'line 6',
                                'line 7', '0.00', '350.00')

        file_content = ",".join(new_record)


        fake_file_path = "fake/file/path"
        self.svcdb = ServiceDb(fake_file_path)

        # file = tempfile.TemporaryFile(mode="w+")
        # self.svcdb = ServiceDb(filename=str(file))
        # file.close()

        with patch("builtins.open", mock_open()) as mock_file:
            self.svcdb.save_record(new_record)
            mock_file.assert_called_with(fake_file_path, "a+")
            mock_file().write.assert_called_with(file_content)

    def test_save_record_but_file_given_does_not_exist(self):
        fake_file_path = "fake/file/path"
        self.svcdb = ServiceDb(fake_file_path)
        content = """1,line 1,line 2,line 3,line 4,line 5,line 6,line 7,line 8,line 9"""
        record = namedtuple(
            "record",
            "record_id service_date model plate workshop mileage nxt_mileage nxt_date labor amount")

        new_record = record('1', 'line 1', 'line 2', 'line 3', 'line 4', 'line 5', 'line 6',
                            'line 7', 'line 8', 'line 9')
        # self.svcdb.save_record(new_record)
        self.assertRaises(ServiceError, self.svcdb.save_record, new_record)

    def test_save_record_input_not_a_tuple(self):
        fake_file_path = "fake/file/path"
        self.svcdb = ServiceDb(fake_file_path)

        new_record = ''
        self.assertRaises(ServiceError, self.svcdb.save_record, new_record)

    def test_save_record_value_in_tuple_not_string(self):

        record = namedtuple(
            "record",
            "record_id service_date model plate workshop mileage nxt_mileage nxt_date labor amount")

        new_record = record('1', 'line 1', 'line 2', 3, 'line 4', 'line 5', 'line 6',
                            'line 7', '0.00', '350.00')

        with tempfile.TemporaryFile() as fp:
             # fp.write(b'Hello world!')
             self.svcdb = ServiceDb(filename=str(fp))
             self.assertRaises(ServiceError, self.svcdb.save_record, new_record)

    def test_save_record_tuple_values_not_equal_10(self):
        record = namedtuple(
            "record",
            "record_id service_date model plate workshop nxt_date labor amount")  # value 'mileage' and 'nxt_mileage' not there

        new_record = record('1', 'line 1', 'line 2', 'line 3', 'line 4', 'line 7', '0.00', '350.00')

        with tempfile.TemporaryFile() as fp:
            # fp.write(b'Hello world!')
            self.svcdb = ServiceDb(filename=str(fp))
            self.assertRaises(ServiceError, self.svcdb.save_record, new_record)

            with self.assertRaises(ServiceError) as cm:
                self.svcdb.save_record(new_record)
                self.assertEqual(
                    'Input value requires 10 items but "{len(new_record)}" was given', str(cm.exception)
                )

    def test_save_record_svcid_value_not_string_number(self):

        record = namedtuple(
            "record",
            "record_id service_date model plate workshop mileage nxt_mileage nxt_date labor amount")

        new_record = record('A', 'line 1', 'line 2', 'line 3', 'line 4', 'line 5', 'line 6',
                            'line 7', '0.00', '350.00')

        with tempfile.TemporaryFile() as fp:
            # fp.write(b'Hello world!')
            self.svcdb = ServiceDb(filename=str(fp))
            self.assertRaises(ServiceError, self.svcdb.save_record, new_record)

            with self.assertRaises(ServiceError) as cm:
                self.svcdb.save_record(new_record)
            self.assertEqual(
                'Svc Id value must be a string of number',
                str(cm.exception)
            )

    def test_save_record_laborcost_amount_value_not_string_number(self):

        record = namedtuple(
            "record",
            "record_id service_date model plate workshop mileage nxt_mileage nxt_date labor amount")

        new_record = record('7', 'line 1', 'line 2', 'line 3', 'line 4', 'line 5', 'line 6',
                            'line 7', 'line 8', 'line 9')

        with tempfile.TemporaryFile() as fp:
            # fp.write(b'Hello world!')
            self.svcdb = ServiceDb(filename=str(fp))
            self.assertRaises(ServiceError, self.svcdb.save_record, new_record)

            with self.assertRaises(ServiceError) as cm:
                self.svcdb.save_record(new_record)
            self.assertEqual(
                'Labor Cost and Amount must be numbers',
                str(cm.exception)
            )

    def test_save_record_input_value_is_empty_string(self):
        record = namedtuple(
            "record",
            "record_id service_date model plate workshop mileage nxt_mileage nxt_date labor amount")

        new_record = record('1', '', '', '', '', '', '', '', '', '')

        with tempfile.TemporaryFile() as fp:
            # fp.write(b'Hello world!')
            self.svcdb = ServiceDb(filename=str(fp))
            self.assertRaises(ServiceError, self.svcdb.save_record, new_record)

            with self.assertRaises(ServiceError) as cm:
                self.svcdb.save_record(new_record)
            self.assertEqual(
                'Input value of empty string is not allowed',
                str(cm.exception)
            )


class TestSavePartRecord(unittest.TestCase):

    # @patch.object(ServiceDb, 'save_part_record')
    def test_save_part_record(self):
        file_content = """Id,SvcId,Date,Name,Qty,UnitPrice,Disc,Amount
1,1,16/04/2019,ATF9 TRANS OIL,5,32.47,0.0,162.35
2,1,16/04/2019,BRAKE FLUID DOT 4,2,24.0,0.0,48.0
3,1,16/04/2019,GASKET-PLUG-OIL DRAIN,1,3.19,0.0,3.19"""

        expected_result = [
                            [1, 1, '16/04/2019', 'ATF9 TRANS OIL', 5, 32.47, 0.0, 162.35],
                            [2, 1, '16/04/2019', 'BRAKE FLUID DOT 4', 2, 24.0, 0.0, 48.0],
                            [3, 1, '16/04/2019', 'GASKET-PLUG-OIL DRAIN', 1, 3.19, 0.0, 3.19],
                            [4, 1, 'item 2', 'ITEM 3', 'item 4', '1.00', '0.00', '5.00']]

        fs = io.StringIO(file_content)
        self.svcdb = ServiceDb(filename_2=fs)

        record = namedtuple(
        "part_record", "id svc_id svc_date part_name qty unit_price discount amount")

        new_record = record(4, 1, 'item 2', 'item 3', 'item 4', '1.00', '0.00', '5.00')

        new_rec_df = self.svcdb.save_part_record(new_record)
        # read_write_csv_mock.assert_called_once_with(new_record)
        self.assertEqual(new_rec_df.values.tolist(), expected_result)

    def test_save_part_record_file_not_exist(self):
        fake_file_path = "file/path/mock"
        self.svcdb = ServiceDb(filename_2=fake_file_path)

        record = namedtuple(
        "part_record", "id svc_id svc_date part_name qty unit_price discount amount")

        new_record = record(4, 1, 'item 2', 'item 3', 'item 4', '1.00', '0.00', '5.00')

        self.assertRaises(ServiceError, self.svcdb.save_part_record, new_record)

    def test_save_part_record_invalid_input(self):
        self.svcdb = ServiceDb()
        # invalid input
        new_record = ""
        # self.assertRaises(ServiceError, self.svcdb.save_part_record, new_record)
        with self.assertRaises(ServiceError) as error:
            self.svcdb.save_part_record(new_record)
        self.assertEqual(str(error.exception), 'Invalid input value was given')



if __name__ == "__main__":
    unittest.main()

    # record = namedtuple(
    #     "record",
    #     "record_id service_date model plate workshop mileage nxt_mileage nxt_date labor amount")
    # new_record = record('1', '', '', '', '', '', '', '', '', '')

    # # new_record = ''
    # # create a temporary file using a context manager
    # with tempfile.TemporaryFile(mode="w") as fp:
    #     svcdb = ServiceDb(str(fp))
    #     svcdb.save_record(new_record)

    # if isinstance(new_record, tuple):
    #     print("ha")
    # for i, itm in enumerate(new_record, start=1):
    #     if i-1 == 0 and new_record[i-1].isdigit():
    #         print("record id is a number")
    #     elif not new_record[i-1]:
    #         print("Empty string not allowed")
    #     print(i, itm)

#     try:

#         # fake_file_path = "file/path/mock"
#         # svcdb = ServiceDb(filename_2=fake_file_path)

#         # record = namedtuple(
#         # "part_record", "id svc_id svc_date part_name qty unit_price discount amount")

#         # new_record = record(4, 1, 'item 2', 'item 3', 'item 4', '1.00', '0.00', '5.00')
#         # new_rec_df = svcdb.save_part_record(new_record)
#         file_content = """Id,SvcId,Date,Name,Qty,UnitPrice,Disc,Amount
# 1,1,16/04/2019,ATF9 TRANS OIL,5,32.47,0.0,162.35
# 2,1,16/04/2019,BRAKE FLUID DOT 4,2,24.0,0.0,48.0
# 3,1,16/04/2019,GASKET-PLUG-OIL DRAIN,1,3.19,0.0,3.19"""

#         fs = io.StringIO(file_content)
#         svcdb = ServiceDb(filename_2=fs)

#         record = namedtuple(
#             "part_record", "id svc_id svc_date part_name qty unit_price discount amount")

#         new_record = record(4, 1, 'item 2', 'item 3', 'item 4', '1.00', '0.00', '5.00')

#         print(svcdb.save_part_record(''))
#     except ServiceError as ex:
#         print(ex)
#     except TypeError:
#         print("User provided invalid input value")

    # print(svc.get_service_record(3))
