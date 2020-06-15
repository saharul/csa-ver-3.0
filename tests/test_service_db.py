import os
import io
import unittest
from collections import namedtuple
from unittest.mock import mock_open, patch

import pandas as pd

from Projects.csa_ver3.service_db import ServiceDb as svcdb, ServiceError


class TestServiceDb(unittest.TestCase):
    # def setUp(self):
    #     self.svcdb = svcdb()

    def test_get_max_id(self):
        # pass the desired content as parameter
        m = mock_open(read_data="15")
        self.svcdb = svcdb("path/to/foo/file")

        with patch("Projects.csa_ver3.service_db.open", m):
            # it does not matter what file path you pass,
            # the file contents are mocked
            assert self.svcdb.get_max_id() == int("15")

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

    def test_get_max_id_empty_file(self):
        file_content_mock = """"""
        fake_file_path = "file/path/mock"
        self.svcdb = svcdb(fake_file_path)

        with patch(
            "Projects.csa_ver3.service_db.open".format(__name__),
            new=mock_open(read_data=file_content_mock),
        ) as _file:
            # actual = self.svcdb.get_max_id()
            self.assertRaises(ServiceError, self.svcdb.get_max_id)

    def test_get_max_id_file_not_exist(self):
        self.svcdb = svcdb(filename="path/to/foo/file")

        # test function return FileNotFoundError if file not exist
        self.assertRaises(ServiceError, self.svcdb.get_max_id)
 
    def test_get_max_part_id(self):
        # pass the desired content as parameter
        m = mock_open(read_data="77")
        self.svcdb = svcdb(filename="path/to/foo/file", filename_2="path/to/foo/file")

        with patch("Projects.csa_ver3.service_db.open", m):
            # it does not matter what file path you pass,
            # the file contents are mocked
            assert self.svcdb.get_max_part_id() == int("77")
    
    def test_get_max_part_id_file_not_exist(self):
        self.svcdb = svcdb(filename_2="path/to/foo/file")
        # test function return FileNotFoundError if file is empty
        self.assertRaises(ServiceError, self.svcdb.get_max_part_id)

    def test_get_max_part_id_empty_file(self):
        file_content_mock = """"""
        fake_file_path = "file/path/mock"        
        self.svcdb = svcdb(filename_2=fake_file_path)

        with patch(
            "Projects.csa_ver3.service_db.open".format(__name__),
            new=mock_open(read_data=file_content_mock),
        ) as _file:
            # test function return UnboundLocalError if file is empty
            self.assertRaises(ServiceError, self.svcdb.get_max_part_id)

    def test_get_max_part_id_only_header_exits(self):
        file_content_mock = """Id,SvcId,Date,Name,Qty,UnitPrice,Disc,Amount"""
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
 
        # f = StringIO()

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

    def test_get_service_record(self):
        data= [[1,'16/04/2019','EXORA 1.6 (A)','AGU4004','CAR SPA SDN BHD','120715','125715','14/07/2019','0.00','466.60'],
               [2,'20/09/2018','EXORA 1.6 (A)','AGU4004','CAR SPA SDN BHD','111783','116783','19/12/2018','0.00','429.35'],
               [3,'18/04/2019','EXORA 1.6 (A)','AGU4004','BENGKEL KERETA WAN','120715','125715','14/07/2019','0.00','60.00']]


        with patch.object(svcdb,'list_all_records2',return_value=data) as mock_method:
            fake_file_path = "fake/file/path"
            self.svcdb = svcdb(filename=fake_file_path)
            value = self.svcdb.get_service_record(2)

            self.assertEqual(value,
                             [3,'18/04/2019','EXORA 1.6 (A)','AGU4004','BENGKEL KERETA WAN','120715','125715','14/07/2019','0.00','60.00']
                            )

    def test_list_all_records2(self):
        file_content = """SvcId,SvcDate,Model,Plate,Workshop,Mileage,Nxt_Mileage,Nxt_Date,Labor,Amount
1,16/04/2019,EXORA 1.6 (A),AGU4004,CAR SPA SDN BHD,120715,125715,14/07/2019,0.00,466.60
2,20/09/2018,EXORA 1.6 (A),AGU4004,CAR SPA SDN BHD,111783,116783,19/12/2018,0.00,429.35
3,18/04/2019,EXORA 1.6 (A),AGU4004,BENGKEL KERETA WAN,120715,125715,14/07/2019,0.00,60.00"""

        expected_result = [
                           [1, '16/04/2019', 'EXORA 1.6 (A)', 'AGU4004', 'CAR SPA SDN BHD', 120715, 125715, '14/07/2019', '0.00', '466.60'], 
                           [2, '20/09/2018', 'EXORA 1.6 (A)', 'AGU4004', 'CAR SPA SDN BHD', 111783, 116783, '19/12/2018', '0.00', '429.35'], 
                           [3, '18/04/2019', 'EXORA 1.6 (A)', 'AGU4004', 'BENGKEL KERETA WAN', 120715, 125715, '14/07/2019', '0.00', '60.00']
                          ]

        fs = io.StringIO(file_content)
        # df.to_csv(stream, sep=",", index=False)

        # fs = io.StringIO(stream.getvalue())
        self.svcdb = svcdb(filename=fs)
        rec_list = self.svcdb.list_all_records2()

        self.assertEqual(len(rec_list), 3)
        self.assertEqual(rec_list, expected_result)

    def test_list_all_records(self):
        file_content = """SvcId,SvcDate,Model,Plate,Workshop,Mileage,Nxt_Mileage,Nxt_Date,Labor,Amount
1,16/04/2019,EXORA 1.6 (A),AGU4004,CAR SPA SDN BHD,120715,125715,14/07/2019,0.00,466.60
2,20/09/2018,EXORA 1.6 (A),AGU4004,CAR SPA SDN BHD,111783,116783,19/12/2018,0.00,429.35
3,18/04/2019,EXORA 1.6 (A),AGU4004,BENGKEL KERETA WAN,120715,125715,14/07/2019,0.00,60.00"""        

        expected_result = [
                           ['svc_id', 'svc_date', 'model', 'svc_shop', 'mileage', 'nxt_mile', 'nxt_date', 'labour', 'amount'],
                           [1, '16/04/2019', 'EXORA 1.6 (A)', 'CAR SPA SDN BHD', 120715, 125715, '14/07/2019', 0.0, 466.6],
                           [2, '20/09/2018', 'EXORA 1.6 (A)', 'CAR SPA SDN BHD', 111783, 116783, '19/12/2018', 0.0, 429.35],
                           [3, '18/04/2019', 'EXORA 1.6 (A)', 'BENGKEL KERETA WAN', 120715, 125715, '14/07/2019', 0.0, 60.0]
                          ]
        fs = io.StringIO(file_content)
        # df.to_csv(stream, sep=",", index=False)

        # fs = io.StringIO(stream.getvalue())
        self.svcdb = svcdb(filename=fs)
        rec_list = self.svcdb.list_all_records()

        self.assertEqual(len(rec_list), 4)
        self.assertEqual(rec_list, expected_result)

    def test_list_all_records_old(self):
        fake_file_path = "fake/file/path"
        self.svcdb = svcdb(fake_file_path)

        file_content_mock = """SvcId,SvcDate,Model,Plate,Workshop,Mileage,Nxt_Mileage,Nxt_Date,Labor,Amount
1,16/04/2019,EXORA 1.6 (A),AGU4004,CAR SPA SDN BHD,120715,125715,14/07/2019,0.00,466.60
2,20/09/2018,EXORA 1.6 (A),AGU4004,CAR SPA SDN BHD,111783,116783,19/12/2018,0.00,429.35
3,18/04/2019,EXORA 1.6 (A),AGU4004,BENGKEL KERETA WAN,120715,125715,14/07/2019,0.00,60.00"""

        expected_result = [
                            ['SvcId', 'SvcDate', 'Model', 'Plate', 'Workshop', 'Mileage', 'Nxt_Mileage', 'Nxt_Date', 'Labor', 'Amount'], 
                            ['1', '16/04/2019', 'EXORA 1.6 (A)', 'AGU4004', 'CAR SPA SDN BHD', '120715', '125715', '14/07/2019', '0.00', '466.60'], 
                            ['2', '20/09/2018', 'EXORA 1.6 (A)', 'AGU4004', 'CAR SPA SDN BHD', '111783', '116783', '19/12/2018', '0.00', '429.35'], 
                            ['3', '18/04/2019', 'EXORA 1.6 (A)', 'AGU4004', 'BENGKEL KERETA WAN', '120715', '125715', '14/07/2019', '0.00', '60.00']
                          ]

        with patch('builtins.open', new=mock_open(read_data=file_content_mock)) as _file:
            rec_list = self.svcdb.list_all_records_old()

            # assert if opened file on write mode 'w'
            _file.assert_called_once_with(fake_file_path, 'r')
            self.assertEqual(rec_list, expected_result)


    def test_list_all_part_records(self):
        file_content = """Id,SvcId,Date,Name,Qty,UnitPrice,Disc,Amount
1,1,16/04/2019,ATF9 TRANS OIL,5,32.47,0.0,162.35
2,1,16/04/2019,BRAKE FLUID DOT 4,2,24.0,0.0,48.0
3,1,16/04/2019,GASKET-PLUG-OIL DRAIN,1,3.19,0.0,3.19"""

        expected_result = [
                          ['SvcId', 'Date', 'Name', 'Qty', 'UnitPrice', 'Disc', 'Amount'], 
                          [1, 1, '16/04/2019', 'ATF9 TRANS OIL', 5, 32.47, 0.0, 162.35], 
                          [2, 1, '16/04/2019', 'BRAKE FLUID DOT 4', 2, 24.0, 0.0, 48.0], 
                          [3, 1, '16/04/2019', 'GASKET-PLUG-OIL DRAIN', 1, 3.19, 0.0, 3.19]
                          ]

        fs = io.StringIO(file_content)
        self.svcdb = svcdb(filename_2=fs)
        rec_list = self.svcdb.list_all_part_records()

        self.assertEqual(len(rec_list), 4)
        self.assertEqual(rec_list, expected_result)


    def test_list_all_part_records2(self):
        file_content = """Id,SvcId,Date,Name,Qty,UnitPrice,Disc,Amount
1,1,16/04/2019,ATF9 TRANS OIL,5,32.47,0.0,162.35
2,1,16/04/2019,BRAKE FLUID DOT 4,2,24.0,0.0,48.0
3,1,16/04/2019,GASKET-PLUG-OIL DRAIN,1,3.19,0.0,3.19"""

        expected_result = [
                          ['SvcId', 'Date', 'Name', 'Qty', 'UnitPrice', 'Disc', 'Amount'], 
                          [1, 1, '16/04/2019', 'ATF9 TRANS OIL', 5, 32.47, 0.0, 162.35], 
                          [2, 1, '16/04/2019', 'BRAKE FLUID DOT 4', 2, 24.0, 0.0, 48.0], 
                          [3, 1, '16/04/2019', 'GASKET-PLUG-OIL DRAIN', 1, 3.19, 0.0, 3.19]
                          ]

        fs = io.StringIO(file_content)
        self.svcdb = svcdb(filename_2=fs)
        rec_list = self.svcdb.list_all_part_records()

        self.assertEqual(len(rec_list), 4)
        self.assertEqual(rec_list, expected_result)


    def test_delete_part_record(self):
        # Test Setup
        file_content = """Id,SvcId,Date,Name,Qty,UnitPrice,Disc,Amount
1,1,16/04/2019,ATF9 TRANS OIL,5,32.47,0.0,162.35
2,1,16/04/2019,BRAKE FLUID DOT 4,2,24.0,0.0,48.0
3,1,16/04/2019,GASKET-PLUG-OIL DRAIN,1,3.19,0.0,3.19"""

        expected_result = [
                          [1, 1, '16/04/2019', 'ATF9 TRANS OIL', 5, 32.47, 0.0, 162.35], 
                          [2, 1, '16/04/2019', 'BRAKE FLUID DOT 4', 2, 24.0, 0.0, 48.0], 
                          ]

        fs = io.StringIO(file_content)
        self.svcdb = svcdb(filename_2=fs)

        try:
            # Test action
            df = self.svcdb.delete_part_record(3)

        finally:
            m=fs.getvalue()


        # print(expected_result)
        # print(df.values.tolist())
        self.assertEqual(expected_result, df.values.tolist())


    def test_show_parts(self):
        self.file_content = """Id,SvcId,Date,Name,Qty,UnitPrice,Disc,Amount
1,1,16/04/2019,ATF9 TRANS OIL,5,32.47,0.0,162.35
2,1,16/04/2019,BRAKE FLUID DOT 4,2,24.0,0.0,48.0
3,1,16/04/2019,GASKET-PLUG-OIL DRAIN,1,3.19,0.0,3.19
4,2,20/09/2018,GASKET-PLUG-OIL DRAIN,1,3.19,0.0,3.19"""

        self.expected_result = [['ATF9 TRANS OIL'], ['BRAKE FLUID DOT 4'], ['GASKET-PLUG-OIL DRAIN']]

        fs = io.StringIO(self.file_content)
        self.svcdb = svcdb(filename_2=fs)

        self.rec_list = self.svcdb.show_parts()
        self.assertEqual(self.expected_result, self.rec_list)


    def test_show_parts2(self):
        self.file_content = """Id,SvcId,Date,Name,Qty,UnitPrice,Disc,Amount
1,1,16/04/2019,ATF9 TRANS OIL,5,32.47,0.0,162.35
2,1,16/04/2019,BRAKE FLUID DOT 4,2,24.0,0.0,48.0
3,1,16/04/2019,GASKET-PLUG-OIL DRAIN,1,3.19,0.0,3.19
4,2,20/09/2018,GASKET-PLUG-OIL DRAIN,1,3.19,0.0,3.19"""

        self.expected_result = [[1, 'ATF9 TRANS OIL'], [2, 'BRAKE FLUID DOT 4'], [3, 'GASKET-PLUG-OIL DRAIN']]

        fs = io.StringIO(self.file_content)
        self.svcdb = svcdb(filename_2=fs)

        self.rec_list = self.svcdb.show_parts2()
        self.assertEqual(self.expected_result, self.rec_list)


    def test_get_record_parts(self):

        file_content = """Id,SvcId,Date,Name,Qty,UnitPrice,Disc,Amount
1,1,16/04/2019,ATF9 TRANS OIL,5,32.47,0.0,162.35
2,1,16/04/2019,BRAKE FLUID DOT 4,2,24.0,0.0,48.0
3,1,16/04/2019,GASKET-PLUG-OIL DRAIN,1,3.19,0.0,3.19
4,2,20/09/2018,GASKET-PLUG-OIL DRAIN,1,3.19,0.0,3.19"""

        expected_result = [
                            [1, '16/04/2019', 'ATF9 TRANS OIL', 5, '32.47', '0.00', '162.35'], 
                            [2, '16/04/2019', 'BRAKE FLUID DOT 4', 2, '24.00', '0.00', '48.00'], 
                            [3, '16/04/2019', 'GASKET-PLUG-OIL DRAIN', 1, '3.19', '0.00', '3.19']
                          ]

        fs = io.StringIO(file_content)

        self.svcdb = svcdb(filename_2=fs)
        rec_list = self.svcdb.get_record_parts(1)
        # print(rec_list)
        # print(expected_result)
        self.assertEqual(rec_list, expected_result)

    def test_get_one_record_part(self):
        file_content = """Id,SvcId,Date,Name,Qty,UnitPrice,Disc,Amount
1,1,16/04/2019,ATF9 TRANS OIL,5,32.47,0.0,162.35
2,1,16/04/2019,BRAKE FLUID DOT 4,2,24.0,0.0,48.0
3,1,16/04/2019,GASKET-PLUG-OIL DRAIN,1,3.19,0.0,3.19
4,2,20/09/2018,GASKET-PLUG-OIL DRAIN,1,3.19,0.0,3.19"""

        expected_result = [2, 1, '16/04/2019', 'BRAKE FLUID DOT 4', 2, 24.0, 0.0, 48.0]

        fs = io.StringIO(file_content)

        self.svcdb = svcdb(filename_2=fs)
        rec_list = self.svcdb.get_one_record_part(1, 1)
        self.assertEqual(rec_list, expected_result)

    def test_get_record_parts_prev(self):
        file_content = """Id,SvcId,Date,Name,Qty,UnitPrice,Disc,Amount
1,1,16/04/2019,ATF9 TRANS OIL,5,32.47,0.0,162.35
2,1,16/04/2019,BRAKE FLUID DOT 4,2,24.0,0.0,48.0
3,1,16/04/2019,GASKET-PLUG-OIL DRAIN,1,3.19,0.0,3.19
4,2,20/09/2018,GASKET-PLUG-OIL DRAIN,1,3.19,0.0,3.19"""

        expected_result = [
                           ['No', 'SvcId', 'Date', 'Name', 'Qty', 'UnitPrice', 'Disc', 'Amount'], 
                           [0, 1, 1, '16/04/2019', 'ATF9 TRANS OIL', 5, 32.47, 0.0, 162.35], 
                           [1, 2, 1, '16/04/2019', 'BRAKE FLUID DOT 4', 2, 24.0, 0.0, 48.0], 
                           [2, 3, 1, '16/04/2019', 'GASKET-PLUG-OIL DRAIN', 1, 3.19, 0.0, 3.19]
                          ]
                           

        fs = io.StringIO(file_content)

        self.svcdb = svcdb(filename_2=fs)
        rec_list = self.svcdb.get_record_parts_prev(1)
        self.assertEqual(rec_list, expected_result)



if __name__ == "__main__":
    unittest.main()
