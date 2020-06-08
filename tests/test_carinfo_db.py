import unittest
from carinfo_db import CarInfoDb as cidb


class TestCarInfoDb(unittest.TestCase):
    def setUp(self):
        self.ci = cidb()

    def test_getmodelid(self):
        self.assertEqual(self.ci.GetModelId("BEZZA - 1300 X (AUTO)"), 1)
        self.assertEqual(self.ci.GetModelId("EXORA 1.6 (A)"), 2)
        self.assertEqual(self.ci.GetModelId("AXIA - 850 X (AUTO)"), 3)

    def test_listcarinfoshort(self):
        self.assertIsNotNone(self.ci.ListCarInfoShort())
        self.assertEqual(self.ci.ListCarInfoShort()[0], "BEZZA - 1300 X (AUTO)")

    def test_listcarinfo(self):
        self.assertIsNotNone(self.ci.ListCarInfo())
        self.assertEqual(
            self.ci.ListCarInfo()[0],
            [
                "1",
                "BEZZA - 1300 X (AUTO)",
                "AKX6455",
                "28/02/2018",
                "0B00784",
                "PM2B301S003088356",
                "OCEAN BLUE",
                "KHADIJAH ISMAIL",
            ],
        )

    def test_GetCarInfoById(self):
        # test id input is not empty string
        self.assertIsNone(self.ci.GetCarInfoById(""))
        # test the car id string given does not exist
        self.assertIsNone(self.ci.GetCarInfoById("-11"))
        # test for car_id type error entered, not string
        self.assertRaises(TypeError, self.ci.GetCarInfoById, 3)

    def test_GetModelId(self):
        # test id input is not empty string
        self.assertRaises(ValueError, self.ci.GetModelId, "")
        # test id given is not str but an int
        self.assertRaises(TypeError, self.ci.GetModelId, 3)


if __name__ == "__main__":
    unittest.main()
