import unittest
from datetime import date 
from staking_calculator import EthereumStakingCalculator
from decimal import Decimal

class TestRewardLog(unittest.TestCase):

    def test_reward_start_days_match(self):
        staker = EthereumStakingCalculator(10, 
                                           7, 
                                           date(2020, 10, 15), 
                                           24, 
                                           15, 
                                           True
                                           )
        log = staker.get_staking_log()
        
        inv_amount_sum, curr_month_rew_sum, total_rew_sum = 0, 0, 0

        for i in range(0, len(log)):
            inv_amount_sum += log[i]["Investment Amount"]
            curr_month_rew_sum += log[i]["Current Month Reward Amount"]
            total_rew_sum += log[i]["Total Reward Amount To Date"]

        self.assertEqual(len(log), 24, "Should be 24 records")
        self.assertEqual(inv_amount_sum, 256.807995, "Should be 256.807995")
        self.assertEqual(round(curr_month_rew_sum, 6), 1.498057, "Should be 1.498057")
        self.assertEqual(round(total_rew_sum, 6), 18.306051, "Should be 18.306051")

    def test_start_day_before_reward(self):
        staker = EthereumStakingCalculator(10, 
                                           7, 
                                           date(2020, 11, 10), 
                                           24, 
                                           15, 
                                           True
                                           )
        log = staker.get_staking_log()

        inv_amount_sum, curr_month_rew_sum, total_rew_sum = 0, 0, 0
        
        for i in range(0, len(log)):
            inv_amount_sum += log[i]["Investment Amount"]
            curr_month_rew_sum += round(log[i]["Current Month Reward Amount"], 6)
            total_rew_sum += log[i]["Total Reward Amount To Date"]

        self.assertEqual(len(log), 25, "Should be 25 records")
        self.assertEqual(inv_amount_sum, 267.025671, "Should be 267.025671")
        self.assertEqual(round(curr_month_rew_sum, 6), 1.498111, "Should be 1.498111")
        self.assertEqual(round(total_rew_sum, 5), 18.52378, "Should be 18.52378")

    def test_start_day_after_reward(self):
        staker = EthereumStakingCalculator(10, 
                                           7, 
                                           date(2020, 10, 20), 
                                           24, 
                                           15, 
                                           True
                                           )
        log = staker.get_staking_log()
        self.assertEqual(len(log), 25, "Should be 25 records")

    def test_rate_change_rewards(self):

        staker = EthereumStakingCalculator(25, 
                                           0, 
                                           date(2024, 3, 15), 
                                           25, 
                                           23, 
                                           True,
                                           date(2024, 4, 15),
                                           10
                                           )
        log = staker.get_staking_log()
        
        inv_amount_sum, curr_month_rew_sum, total_rew_sum = 0, 0, 0

        for i in range(1, len(log)):
            inv_amount_sum += log[i]["Investment Amount"]
            curr_month_rew_sum += log[i]["Current Month Reward Amount"]
            total_rew_sum += log[i]["Total Reward Amount To Date"]

        self.assertEqual(len(log), 26, "Should be 26")
        self.assertEqual(inv_amount_sum, 687.70612, "Should be 687.70612")
        self.assertEqual(round(curr_month_rew_sum, 6), 5.510171, "Should be 5.510171")
        self.assertEqual(total_rew_sum, 68.216292, "Should be 68.216292")

        #### params
        # DEFINITIONS
        # ETH_INVESTED = 25
        # STAKING_REWARD = 0 # %
        # START_DATE = date.fromisoformat('2024-03-15')
        # DURATION_MONTHS = 25
        # REWARD_DAY = 23
        # TO_REINVEST = True

        # RATE_CHANGE_DATE = date(2024, 4, 15)
        # RATE_CHANGE_TO = 10 # %
        # "main_task": {
        #         "file_path": "record_files/main_task.csv",
        #         "ETH_INVESTED": 25,
        #         "STAKING_REWARD": 10,
        #         "START_DATE": date(2024, 4, 15),
        #         "DURATION_MONTHS": 24,
        #         "REWARD_DAY": 23,
        #         "TO_REINVEST": True,
        #     },

        # sumos turi sutapti ismetant pirmo nario skaicius is rate change reward logo
        pass


if __name__ == "__main__":
    unittest.main()