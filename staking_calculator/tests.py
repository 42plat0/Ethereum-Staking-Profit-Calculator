import unittest
from datetime import date
from staking_calculator import EthereumStakingCalculator


class TestCalcInitValues(unittest.TestCase):
    def test_amount_not_number(self):
        with self.assertRaises(ValueError):
            EthereumStakingCalculator("10", 7, date(2020, 10, 15), 24, 15, True)

    def test_amount_not_positive(self):
        with self.assertRaises(ValueError):
            EthereumStakingCalculator(-10, 7, date(2020, 10, 15), 24, 15, True)

    def test_reward_rate_not_number(self):
        with self.assertRaises(ValueError):
            EthereumStakingCalculator(10, "7", date(2020, 10, 15), 24, 15, True)

    def test_reward_rate_not_positive(self):
        with self.assertRaises(ValueError):
            EthereumStakingCalculator(10, -7, date(2020, 10, 15), 24, 15, True)

    def test_start_date_not_date(self):
        with self.assertRaises(ValueError):
            EthereumStakingCalculator(10, 7, "2024-12-3", 24, 15, True)

    def test_duration_not_number(self):
        with self.assertRaises(ValueError):
            EthereumStakingCalculator(10, 7, date(2020, 10, 15), "24", 15, True)

    def test_duration_not_positive_number(self):
        with self.assertRaises(ValueError):
            EthereumStakingCalculator(10, 7, date(2020, 10, 15), -24, 15, True)

    def test_reward_day_not_number(self):
        with self.assertRaises(ValueError):
            EthereumStakingCalculator(10, 7, date(2020, 10, 15), 24, "15", True)
    
    def test_reward_day_impossible(self):
        with self.assertRaises(ValueError):
            EthereumStakingCalculator(10, 7, date(2024, 11, 10), 24, 32, True)
            EthereumStakingCalculator(10, 7, date(2024, 11, 10), 24, 0, True)
            EthereumStakingCalculator(10, 7, date(2024, 11, 10), 24, -10, True)
            EthereumStakingCalculator(10, 7, date(2024, 11, 10), 24, 10.3, True)

    def test_reward_day_not_positive_number(self):
        with self.assertRaises(ValueError):
            EthereumStakingCalculator(10, 7, date(2020, 10, 15), 24, -15, True)

    def test_reinvest_not_bool(self):
        with self.assertRaises(ValueError):
            EthereumStakingCalculator(10, 7, date(2020, 10, 15), 24, 15, "True")
            EthereumStakingCalculator(10, 7, date(2020, 10, 15), 24, 15, None)

    def test_rate_change_not_date(self):
        with self.assertRaises(ValueError):
            EthereumStakingCalculator(
                10, 7, date(2020, 10, 15), 24, 15, True, "2024-12-3"
            )

    def test_changed_rate_not_number(self):
        with self.assertRaises(ValueError):
            EthereumStakingCalculator(
                10, 7, date(2020, 10, 15), 24, 15, True, date(2020, 12, 15), "1"
            )

    def test_changed_rate_not_positive_number(self):
        with self.assertRaises(ValueError):
            EthereumStakingCalculator(
                10, 7, date(2020, 10, 15), 24, 15, True, date(2020, 12, 15), -1
            )

    def test_rate_change_earlier_than_start(self):
        with self.assertRaises(ValueError):
            EthereumStakingCalculator(
                10, 7, date(2020, 10, 15), 24, 15, date(2020, 9, 15), 1
            )


class TestRewardLog(unittest.TestCase):
    def test_reward_start_days_match(self):
        staker = EthereumStakingCalculator(10, 7, date(2020, 10, 15), 24, 15, True)
        log = staker.get_staking_log()

        inv_amount_sum, curr_month_rew_sum, total_rew_sum = 0, 0, 0

        for i in range(0, len(log)):
            inv_amount_sum += float(log[i]["Investment Amount"])
            curr_month_rew_sum += float(log[i]["Current Month Reward Amount"])
            total_rew_sum += float(log[i]["Total Reward Amount To Date"])

        self.assertEqual(len(log), 24, "Should be 24 records")
        self.assertEqual(
            round(inv_amount_sum, 6),
            256.807995,
            "Investment Amount Should be 256.807995",
        )
        self.assertEqual(
            round(curr_month_rew_sum, 6),
            1.498057,
            "Current Month Reward Amount should be 1.498057",
        )
        self.assertEqual(
            round(total_rew_sum, 6),
            18.306051,
            "Total Reward Amount To Date should be 18.306051",
        )

    def test_start_day_before_reward_day(self):
        staker = EthereumStakingCalculator(10, 7, date(2020, 11, 10), 24, 15, True)
        log = staker.get_staking_log()

        inv_amount_sum, curr_month_rew_sum, total_rew_sum = 0, 0, 0

        for i in range(0, len(log)):
            inv_amount_sum += float(log[i]["Investment Amount"])
            curr_month_rew_sum += float(log[i]["Current Month Reward Amount"])
            total_rew_sum += float(log[i]["Total Reward Amount To Date"])

        self.assertEqual(len(log), 25, "Should be 25 records")
        self.assertEqual(
            round(inv_amount_sum, 6),
            267.025671,
            "Investment Amount Should be 267.025671",
        )
        self.assertEqual(
            round(curr_month_rew_sum, 6),
            1.498111,
            "Current Month Reward Amount should be 1.498111",
        )
        self.assertEqual(
            round(total_rew_sum, 6),
            18.523782,
            "Total Reward Amount To Date should be 18.523782",
        )

    def test_start_day_after_reward_day(self):
        staker = EthereumStakingCalculator(10, 7, date(2020, 10, 20), 24, 15, True)
        log = staker.get_staking_log()

        inv_amount_sum, curr_month_rew_sum, total_rew_sum = 0, 0, 0

        for i in range(0, len(log)):
            inv_amount_sum += float(log[i]["Investment Amount"])
            curr_month_rew_sum += float(log[i]["Current Month Reward Amount"])
            total_rew_sum += float(log[i]["Total Reward Amount To Date"])

        self.assertEqual(len(log), 25, "Should be 25 records")
        self.assertEqual(
            round(inv_amount_sum, 6),
            268.059826,
            "Investment Amount Should be 268.059826",
        )
        self.assertEqual(
            round(curr_month_rew_sum, 6),
            1.498108,
            "Current Month Reward Amount should be 1.498108",
        )
        self.assertEqual(
            round(total_rew_sum, 6),
            19.557937,
            "Total Reward Amount To Date should be 19.557937",
        )

    def test_rate_change_rewards(self):

        staker = EthereumStakingCalculator(
            25, 0, date(2024, 3, 15), 25, 23, True, date(2024, 4, 15), 10
        )
        log = staker.get_staking_log()

        inv_amount_sum, curr_month_rew_sum, total_rew_sum = 0, 0, 0

        # sumos turi sutapti ismetant pirmo nario skaicius is rate change reward logo
        for i in range(1, len(log)):
            inv_amount_sum += float(log[i]["Investment Amount"])
            curr_month_rew_sum += float(log[i]["Current Month Reward Amount"])
            total_rew_sum += float(log[i]["Total Reward Amount To Date"])

        self.assertEqual(len(log), 26, "Should be 26")
        self.assertEqual(
            round(inv_amount_sum, 6), 687.70612, "Investment Amount Should be 687.70612"
        )
        self.assertEqual(
            round(curr_month_rew_sum, 6),
            5.510171,
            "Current Month Reward Amount should be 5.510171",
        )
        self.assertEqual(total_rew_sum, 68.216292, "Should be 68.216292")


if __name__ == "__main__":
    unittest.main()
