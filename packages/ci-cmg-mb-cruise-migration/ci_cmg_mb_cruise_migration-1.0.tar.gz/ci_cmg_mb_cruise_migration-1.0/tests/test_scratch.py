import unittest
import datetime


class TestScratch(unittest.TestCase):
    def test_len_empty_list(self):

        mylist = []
        print(len(mylist))

    # def test_yaml_load_list(self):
    #     with open("survey_blacklist_test.yaml", 'r') as yaml_data_file:
    #         blacklist = yaml.safe_load(yaml_data_file)
    #         print(blacklist)

    def test_runtime_warning_to_string(self):
        message = "Message in a bottle"
        try:
            raise RuntimeWarning(message)
        except RuntimeWarning as w:
            warning = str(w)
            self.assertEqual(message, warning)

    def test_date_formatting(self):
        date = datetime.datetime(2020, 5, 18, 1, 2, 4).isoformat()
        print(date)

        # timestamp = "04-SEP-19"
        # timestamp = datetime.datetime.strptime()
        # date_only = timestamp.strftime('%d-%b-%y')
        # print(date_only)

