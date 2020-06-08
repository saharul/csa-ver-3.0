import unittest
from unittest.mock import mock_open, patch
from Projects.csa_ver3.service_db import ServiceDb as svcdb
from collections import namedtuple
import os


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

    # def test_get_max_id_only_header_exist(self):
    #     filename = "/home/saharul/Projects/csa-ver-3.0/test/data/service_master_header_only.csv"

    #     self.svcdb = svcdb(filename)

    #     # test function return 0 if only header exist
    #     self.assertEqual(self.svcdb.get_max_id(), 0)

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

    # def test_get_max_id_empty_file(self):
    #     filename = (
    #         "/home/saharul/Projects/csa-ver-3.0/test/data/service_master_empty_file.csv"
    #     )

    #     self.svcdb = svcdb(filename)

    #     # test function return UnboundLocalError if file is empty
    #     self.assertRaises(UnboundLocalError, self.svcdb.get_max_id)

    def test_get_max_id_file_not_exist(self):
        self.svcdb = svcdb(filename="path/to/foo/file")

        # test function return FileNotFoundError if file not exist
        self.assertRaises(FileNotFoundError, self.svcdb.get_max_id)

 
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
        self.assertRaises(FileNotFoundError, self.svcdb.get_max_part_id)

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
