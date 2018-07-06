import unittest
import responses
import requests
from bp import BP
from monitor import BPMonitor
from config import HOST
from data import fake_json, fake_json_1, fake_info, fake_info_1, fake_table_data,fake_table_data_1
import time


class TestBPMonitor(unittest.TestCase):

    @responses.activate
    def test_in_top21_list(self):
        print("###################test in top 21 #####################")
        responses.add(responses.POST, HOST + '/v1/chain/get_producers',
                      json=fake_json, status=200)
        responses.add(responses.POST, HOST + '/v1/chain/get_table_rows',
                      json=fake_table_data, status=200)

        bp = BP("eoslaomaocom", True)
        bp_monitor = BPMonitor(bp)
        bp_monitor.check_is_top21()
        self.assertTrue(bp.is_top21)
        self.assertFalse(bp.is_new_top21)
        print("###################test in top 21 ##################### \n")
        print("\n")

    @responses.activate
    def test_not_in_top21_list(self):
        print("###################test not in top 21 #####################")
        responses.add(responses.POST, HOST + '/v1/chain/get_producers',
                      json=fake_json, status=200)
        responses.add(responses.POST, HOST + '/v1/chain/get_table_rows',
                      json=fake_table_data, status=200)
        bp = BP("eoslemonscom", False)
        bp_monitor = BPMonitor(bp)
        bp_monitor.check_is_top21()
        self.assertFalse(bp.is_top21)
        self.assertFalse(bp.is_new_top21)
        print("###################test not in top 21 #####################\n")
        print("\n")

    @responses.activate
    def test_bpc_to_bp(self):
        print("##########################test from bpc -> bp #####################")
        responses.add(responses.POST, HOST + '/v1/chain/get_producers',
                      json=fake_json, status=200)
        responses.add(responses.POST, HOST + '/v1/chain/get_table_rows',
                      json=fake_table_data, status=200)
        bp = BP("eoslemonscom", False)
        bp_monitor = BPMonitor(bp)
        bp_monitor.check_is_top21()
        self.assertFalse(bp.is_top21)
        self.assertFalse(bp.is_new_top21)
        responses.remove(responses.POST, HOST + '/v1/chain/get_producers')

        responses.add(responses.POST, HOST + '/v1/chain/get_producers',
                      json=fake_json_1, status=200)
        responses.add(responses.POST, HOST + '/v1/chain/get_table_rows',
                      json=fake_table_data, status=200)
        # become the bp
        bp_monitor.check_is_top21()
        self.assertTrue(bp.is_top21)
        self.assertTrue(bp.is_new_top21)
        print("##########################test from bpc -> bp #####################\n")
        print("\n")

    @responses.activate
    def test_bp_to_bpc(self):
        print("##################test from bp -> bpc####################")
        responses.add(responses.POST, HOST + '/v1/chain/get_producers',
                      json=fake_json_1, status=200)
        responses.add(responses.POST, HOST + '/v1/chain/get_table_rows',
                      json=fake_table_data, status=200)
        bp = BP("eoslemonscom", True)
        bp_monitor = BPMonitor(bp)
        bp_monitor.check_is_top21()
        self.assertTrue(bp.is_top21)
        self.assertFalse(bp.is_new_top21)
        responses.remove(responses.POST, HOST + '/v1/chain/get_producers')

        responses.add(responses.POST, HOST + '/v1/chain/get_producers',
                      json=fake_json, status=200)
        responses.add(responses.POST, HOST + '/v1/chain/get_table_rows',
                      json=fake_table_data, status=200)
        # be the bpc
        bp_monitor.check_is_top21()
        self.assertFalse(bp.is_top21)
        self.assertFalse(bp.is_new_top21)
        print("##################test from bp -> bpc####################\n")
        print("\n")

    @responses.activate
    def test_check_is_producing(self):
        print("##################test check is producing####################")
        responses.add(responses.GET, HOST + '/v1/chain/get_info',
                      json=fake_info, status=200)
        responses.add(responses.POST, HOST + '/v1/chain/get_table_rows',
                      json=fake_table_data, status=200)
        bp = BP('eoslaomaocom', True)
        bp_monitor = BPMonitor(bp)

        self.assertTrue(bp_monitor.check_is_producing())
        self.assertTrue(bp.is_top21)
        print("##################test check is producing####################\n")
        print("\n")

    @responses.activate
    def test_check_is_not_producin(self):
        print("##################test check is not producing####################")
        responses.add(responses.GET, HOST + '/v1/chain/get_info',
                      json=fake_info_1, status=200)
        responses.add(responses.POST, HOST + '/v1/chain/get_table_rows',
                      json=fake_table_data_1, status=200)
        bp = BP('eoslaomaocom', True)
        bp_monitor = BPMonitor(bp)
        bp_monitor.count = 63

        self.assertFalse(bp_monitor.check_is_producing())
        self.assertTrue(bp.is_top21)
        print("##################test check is not producing####################\n")
        print("\n")

    def tearDown(self):
        responses.remove(responses.POST, HOST + '/v1/chain/get_producers')
        responses.remove(responses.GET, HOST + '/v1/chain/get_info')
        responses.remove(responses.POST, HOST + '/v1/chain/get_table_rows')


if __name__ == '__main__':
    unittest.main()
