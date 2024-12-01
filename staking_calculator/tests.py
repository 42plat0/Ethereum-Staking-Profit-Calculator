import unittest
from datetime import date 
from staking_calculator import EthereumStakingCalculator

ETH_INVESTED = 10
STAKING_REWARD = 7 # %
DURATION_MONTHS = 24
REWARD_DAY = 15
TO_REINVEST = True

class TestRewardLog(unittest.TestCase):

    def test_reward_start_days_match(self):
        staker = EthereumStakingCalculator(10, STAKING_REWARD, date(2020, 10, 15), DURATION_MONTHS, 15, TO_REINVEST)
        log = staker.get_staking_log()
        self.assertEqual(len(log), 24, f"Should be {DURATION_MONTHS} records")

    def test_start_day_before_reward(self):
        staker = EthereumStakingCalculator(10, STAKING_REWARD, date(2020, 10, 10), DURATION_MONTHS, 15, TO_REINVEST)
        log = staker.get_staking_log()
        self.assertEqual(len(log), 25, f"Should be {DURATION_MONTHS + 1} records")

    def test_start_day_after_reward(self):
        staker = EthereumStakingCalculator(10, STAKING_REWARD, date(2020, 10, 20), DURATION_MONTHS, 15, TO_REINVEST)
        log = staker.get_staking_log()
        self.assertEqual(len(log), 25, f"Should be {DURATION_MONTHS + 1} records")

if __name__ == "__main__":
    unittest.main()