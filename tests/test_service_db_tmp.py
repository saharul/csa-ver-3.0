import unittest
from unittest.mock import mock_open, patch, Mock
from Projects.csa_ver3.service_db import ServiceDb as svcdb
from collections import namedtuple
import pandas as pd
import io
from io import BytesIO
from io import StringIO
import os


class TestServiceDb(unittest.TestCase):
    def test_get_max_id_only_header_exits(self):
        file_content_mock = """SvcId,SvcDate,Model,Plate,Workshop,Mileage,Nxt_Mileage,Nxt_Date,Labor,Amount"""
        fake_file_path = "file/path/mock"
        self.svcdb = svcdb(fake_file_path)

        with patch(
            "Projects.csa_ver3.service_db.open".format(__name__),
            new=mock_open(read_data=file_content_mock),
        ) as _file:
            actual = self.svcdb.get_max_id()
            _file.assert_called_once_with(fake_file_path, "r")

        expected = 0
        self.assertEqual(expected, actual)

    def test_get_max_id_empty_file(self):
        file_content_mock = """"""
        fake_file_path = "file/path/mock"
        self.svcdb = svcdb(fake_file_path)

        with patch(
            "Projects.csa_ver3.service_db.open".format(__name__),
            new=mock_open(read_data=file_content_mock),
        ) as _file:
            # actual = self.svcdb.get_max_id()
            self.assertRaises(UnboundLocalError, self.svcdb.get_max_id)

    def test_get_max_part_id_empty_file(self):
        file_content_mock = """"""
        fake_file_path = "file/path/mock"
        self.svcdb = svcdb(filename_2=fake_file_path)

        with patch(
            "Projects.csa_ver3.service_db.open".format(__name__),
            new=mock_open(read_data=file_content_mock),
        ) as _file:
            # test function return UnboundLocalError if file is empty
            self.assertRaises(UnboundLocalError, self.svcdb.get_max_part_id)

    def test_get_max_part_id(self):
        self.svcdb = svcdb(
            filename_2="Projects/csa_ver3/tests/data/service_parts.csv"
        )
        # test function return correct value of max part id = 66
        self.assertEqual(self.svcdb.get_max_part_id(), 66)

    def test_get_max_part_id(self):
        # pass the desired content as parameter
        m = mock_open(read_data="77")
        self.svcdb = svcdb(filename="path/to/foo/file")

        with patch("Projects.csa_ver3.service_db.open", m):
            # it does not matter what file path you pass,
            # the file contents are mocked
            assert self.svcdb.get_max_part_id() == int("77")

    # def test_save_part_record(self):
    #     fake_file_path = "fake/file/path"
    #     self.svcdb = svcdb(fake_file_path)
    #     content = """item 0,item 1,item 2,item 3,item 4,item 5,item 6,item 7"""
    #     record = namedtuple(
    #         "part_record", "id svc_id svc_date part_name qty unit_price discount amount")

    #     new_record = record('item 0', 'item 1', 'item 2', 'item 3', 'item 4', '1.00', '0.00',
    #                         '5.00')

    #     m = mock_open()
    #     with patch('Projects.csa_ver3.service_db.open', m) as mocked_file:
    #         self.svcdb.save_part_record(new_record)

    #         # assert if opened file on write mode 'w'
    #         # mocked_file.assert_called_once_with(fake_file_path, 'r')

    #         # assert if write(content) was called from the file opened
    #         # in another words, assert if the specific content was written in file
    #         mocked_file().write.assert_called_once_with(content)

    @patch.object(svcdb, 'save_part_record')
    def test_run_save_part_record(self, read_write_csv_mock: Mock):
        fake_file_path = "fake/file/path"
        self.svcdb = svcdb(fake_file_path)
        record = namedtuple(
            "part_record", "id svc_id svc_date part_name qty unit_price discount amount")

        new_record = record('item 0', 'item 1', 'item 2', 'item 3', 'item 4', '1.00', '0.00', '5.00')

        # read_write_csv_mock.return_value =  pd.DataFrame(
        #                              {
        #                               "Id": ['item 0'],
        #                               "SvcId": ['item 1'],
        #                               "Date": ['item 2'],
        #                               "Name": ['item 3'.upper()],
        #                               "Qty": ['item 4'],
        #                               "UnitPrice": ["{:.2f}".format(float('1.00'))],
        #                               "Disc": ["{:.2f}".format(float('0.00'))],
        #                               "Amount": ["{:.2f}".format(float('5.00'))],
        #                               }
        #                     )
        self.svcdb.save_part_record(new_record)
        read_write_csv_mock.assert_called_once_with(new_record)
        # print(read_csv_mock.call_count)


        # # Define a DF as the contents for your csv file.
        # df =  pd.DataFrame(
        #                              {
        #                               "Id": ['item 0'],
        #                               "SvcId": ['item 1'],
        #                               "Date": ['item 2'],
        #                               "Name": ['item 3'.upper()],
        #                               "Qty": ['item 4'],
        #                               "UnitPrice": ["{:.2f}".format(float('1.00'))],
        #                               "Disc": ["{:.2f}".format(float('0.00'))],
        #                               "Amount": ["{:.2f}".format(float('5.00'))],
        #                               }
        #                     )
        # # Create your in memory BytesIO file.
        # output = BytesIO()
        # # writer = pd.ExcelWriter(output, engine="xlsxwriter")
        # df.to_csv(output, index=False, header=True)
        # # writer.save()
        # output.seek(0)  # Contains the Excel file in memory file.

        # # Create an in-memory text stream
        # textStream = StringIO();
        # # Write the DataFrame contents to the text stream's buffer as a CSV
        # df.to_csv(textStream,index=False, header=True);
        # textStream.seek(0)

        # read_csv_mock.return_value = textStream

        # pd.testing.assert_frame_equal(df, textStream)

    def test_save_part_record(self):
        expected_text = """Id,SvcId,Date,Name,Qty,UnitPrice,Disc,Amount\n, item 0,item 1,item 2,ITEM 3,item 4,1.00,0.00,5.00\n"""

        filename = 'foo_save_part_record.txt'
        foo = svcdb(filename_2=filename)

        with open(filename,"w+") as f:
            f.write("Id,SvcId,Date,Name,Qty,UnitPrice,Disc,Amount")

        record = namedtuple(
            "part_record", "id svc_id svc_date part_name qty unit_price discount amount")

        new_record = record('item 0', 'item 1', 'item 2', 'item 3', 'item 4', '1.00', '0.00', '5.00')
        try:

            foo.save_part_record(new_record)

            with open(filename, 'r') as f:
                text = f.readlines()
        finally:
            os.remove(filename)

        # print(expected_text)
        # print(', '.join(text))
        self.assertEqual(expected_text, ', '.join(text))

    def test_add_part_record(self):
        expected_items = """Id,SvcId,Date,Name,Qty,UnitPrice,Disc,Amount\n, 1,item 1,item 2,ITEM 3,item 4,1.00,0.00,5.00\n"""
        filename = "foo_add_part_record_test.txt"
        foo = svcdb(filename_2=filename)

        f = StringIO()

        with open(filename,"w+") as f:
            f.write("Id,SvcId,Date,Name,Qty,UnitPrice,Disc,Amount")

        try:
            foo.add_part_record('item 1', 'item 2', 'item 3', 'item 4', '1.00', '0.00', '5.00')

            with open(filename, 'r') as f:
                items = f.readlines()
        finally:
            os.remove(filename)

        # print(expected_items)
        # print(', '.join(items))
        self.assertEqual(expected_items, ', '.join(items))

    def test_update_part_record(self):
        # Test Setup
        expected_text = """Id,SvcId,Date,Name,Qty,UnitPrice,Disc,Amount\n, 1,item 1,item two,ITEM TRI,item for,3.00,1.00,15.00\n"""
        filename = "foo_update_part_record_test.txt"

        foo = svcdb(filename_2=filename)
        with open(filename,"w+") as f:
            file_text = """Id,SvcId,Date,Name,Qty,UnitPrice,Disc,Amount\n1,item 1,item 2,item 3,item 4,1.00,0.00,5.00\n"""
            f.write(file_text)

        try:
            # Test action
            foo.update_part_record(1, 'item 1', 'item two', 'item tri', 'item for', '3.00', '1.00', '15.00')

            with open(filename, 'r') as f:
                items = f.readlines()
        finally:
            os.remove(filename)

        # print(expected_text)
        # print(', '.join(items))
        self.assertEqual(expected_text, ', '.join(items))

    def test_save_record(self):
        fake_file_path = "fake/file/path"
        self.svcdb = svcdb(fake_file_path)
        content = """line 0,line 1,line 2,line 3,line 4,line 5,line 6,line 7,line 8,line 9"""
        record = namedtuple(
            "record",
            "record_id service_date model plate workshop mileage nxt_mileage nxt_date labor amount")

        new_record = record('line 0', 'line 1', 'line 2', 'line 3', 'line 4', 'line 5', 'line 6',
                            'line 7', 'line 8', 'line 9')


        with patch('Projects.csa_ver3.service_db.open', mock_open()) as mocked_file:
            self.svcdb.save_record(new_record)

            # assert if opened file on write mode 'w'
            mocked_file.assert_called_once_with(fake_file_path, 'a+')

            # assert if write(content) was called from the file opened
            # in another words, assert if the specific content was written in file
            mocked_file().write.assert_called_once_with(content)


    def test_update_record(self):
        # Test Setup
        expected_text="""SvcId,SvcDate,Model,Plate,Workshop,Mileage,Nxt_Mileage,Nxt_Date,Labor,Amount\n1,24/05/2018,BEZZA - 1300 X (AUTO),AKX6455,PERODUA SALES TASEK IPOH,55108,65108,10/09/2020,30.00,380.30\n"""

        df  = pd.DataFrame(
        {
            "SvcId": [1],
            "SvcDate": ["16/04/2019"],
            "Model": ["EXORA 1.6 (A)"],
            "Plate": ["AGU4004"],
            "Workshop": ["CAR SPA SDN BHD"],
            "Mileage": ["120715"],
            "Nxt_Mileage": ["125715"],
            "Nxt_Date": ["14/07/2019"],
            "Labor": ["0.00"],
            "Amount": ["466.60"],
        })

        stream = io.StringIO()
        df.to_csv(stream, sep=",", index=False)

        fs = io.StringIO(stream.getvalue())
        foo = svcdb(filename=fs)

        # with open(fs,"w+") as f:
        #     file_text = """Id,SvcId,Date,Name,Qty,UnitPrice,Disc,Amount\n1,item 1,item 2,item 3,item 4,1.00,0.00,5.00\n"""
        #     f.write(file_text)

        try:
            # Test action
            foo.update_record(
                        1,
                        "24/05/2018",
                        "1",
                        "AKX6455",
                        "PERODUA SALES TASEK IPOH",
                        "55108",
                        "65108",
                        "10/09/2020",
                        "30.00",
                        "380.30"
                        )

            # with open(filename, 'r') as f:
            #     items = f.readlines()
        finally:
            # os.remove(filename)
            m=fs.getvalue()[165:346]


        # print('\n'+ expected_text)
        # print(m)
        self.assertEqual(expected_text, m)



    def test_delete_record(self):
        fake_file_path = "fake/file/path"
        self.svcdb = svcdb(fake_file_path)

        file_content_mock = """SvcId,SvcDate,Model,Plate,Workshop,Mileage,Nxt_Mileage,Nxt_Date,Labor,Amount
1,16/04/2019,EXORA 1.6 (A),AGU4004,CAR SPA SDN BHD,120715,125715,14/07/2019,0.00,466.60
2,20/09/2018,EXORA 1.6 (A),AGU4004,CAR SPA SDN BHD,111783,116783,19/12/2018,0.00,429.35
3,18/04/2019,EXORA 1.6 (A),AGU4004,BENGKEL KERETA WAN,120715,125715,14/07/2019,0.00,60.00"""

        with patch('Projects.csa_ver3.service_db.open', new=mock_open(read_data=file_content_mock)) as _file:
            self.svcdb.delete_record("1")

            # assert if opened file on write mode 'w'
            _file.assert_called_once_with(fake_file_path, 'r+')

            # assert if write(content) was called from the file opened
            # in another words, assert if the specific content was written in file
            _file().write.assert_any_call("""SvcId,SvcDate,Model,Plate,Workshop,Mileage,Nxt_Mileage,Nxt_Date,Labor,Amount\n""")
            _file().write.assert_any_call("""2,20/09/2018,EXORA 1.6 (A),AGU4004,CAR SPA SDN BHD,111783,116783,19/12/2018,0.00,429.35\n""")
            _file().write.assert_any_call("""3,18/04/2019,EXORA 1.6 (A),AGU4004,BENGKEL KERETA WAN,120715,125715,14/07/2019,0.00,60.00""")
            assert _file().write.call_count == 3


    def test_get_record(self):
        fake_file_path = "fake/file/path"
        self.svcdb = svcdb(filename=fake_file_path)

        file_content_mock = """SvcId,SvcDate,Model,Plate,Workshop,Mileage,Nxt_Mileage,Nxt_Date,Labor,Amount
1,16/04/2019,EXORA 1.6 (A),AGU4004,CAR SPA SDN BHD,120715,125715,14/07/2019,0.00,466.60
2,20/09/2018,EXORA 1.6 (A),AGU4004,CAR SPA SDN BHD,111783,116783,19/12/2018,0.00,429.35
3,18/04/2019,EXORA 1.6 (A),AGU4004,BENGKEL KERETA WAN,120715,125715,14/07/2019,0.00,60.00"""

        with patch('builtins.open', new=mock_open(read_data=file_content_mock)) as file:
            line = self.svcdb.get_record("3")

            # assert if opened file on write mode 'w'
            file.assert_called_once_with(fake_file_path, 'r')

            self.assertEqual(line[0], '3')
            self.assertEqual(line[4], 'BENGKEL KERETA WAN')


if __name__ == "__main__":
    unittest.main()
