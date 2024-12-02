from staking_calculator.staking_calculator import EthereumStakingCalculator
from helpers.helpers import save_csv
from datetime import date

from argparse import ArgumentParser, MetavarTypeHelpFormatter

task_defs = {
    "example_task": {
        "file_path": "record_files/example_task.csv",
        "ETH_INVESTED": 10,
        "STAKING_REWARD": 7,
        "START_DATE": date(2020, 11, 10),
        "DURATION_MONTHS": 24,
        "REWARD_DAY": 15,
        "TO_REINVEST": True,
    },
    "main_task": {
        "file_path": "record_files/main_task.csv",
        "ETH_INVESTED": 25,
        "STAKING_REWARD": 10,
        "START_DATE": date(2024, 4, 15),
        "DURATION_MONTHS": 24,
        "REWARD_DAY": 23,
        "TO_REINVEST": True,
    },
    "bonus_task1": {
        "file_path": "record_files/bonus_task1.csv",
        "ETH_INVESTED": 25,
        "STAKING_REWARD": 10,
        "START_DATE": date(2024, 4, 15),
        "DURATION_MONTHS": 24,
        "REWARD_DAY": 23,
        "TO_REINVEST": True,
        "RATE_CHANGE_DATE": date(2025, 4, 15),
        "RATE_CHANGE_TO": 8,  # %
    },
    "invalid": {
        "ETH_INVESTED": -100,
        "STAKING_REWARD": 10,
        "START_DATE": date(2024, 4, 15),
        "DURATION_MONTHS": 24,
        "REWARD_DAY": 23,
        "TO_REINVEST": True,
        "RATE_CHANGE_DATE": date(2025, 4, 15),
        "RATE_CHANGE_TO": 8,  # %
    },
}

# main_task = task_defs["main_task"]

# main_task_staker = EthereumStakingCalculator(main_task["ETH_INVESTED"],
#                                    main_task["STAKING_REWARD"],
#                                    main_task["START_DATE"],
#                                    main_task["DURATION_MONTHS"],
#                                    main_task["REWARD_DAY"],
#                                    main_task["TO_REINVEST"])

# main_task_reward_log = main_task_staker.get_staking_log()

# bonus_task = task_defs["bonus_task1"]

# bonus_task_staker = EthereumStakingCalculator(bonus_task ["ETH_INVESTED"],
#                                    bonus_task ["STAKING_REWARD"],
#                                    bonus_task ["START_DATE"],
#                                    bonus_task ["DURATION_MONTHS"],
#                                    bonus_task ["REWARD_DAY"],
#                                    bonus_task ["TO_REINVEST"],
#                                    bonus_task ["RATE_CHANGE_DATE"],
#                                    bonus_task ["RATE_CHANGE_TO"],
#                                    )

# bonus_task_reward_log = bonus_task_staker.get_staking_log()

# example_task = task_defs["example_task"]

# example_task_staker = EthereumStakingCalculator(example_task ["ETH_INVESTED"],
#                                    example_task ["STAKING_REWARD"],
#                                    example_task ["START_DATE"],
#                                    example_task ["DURATION_MONTHS"],
#                                    example_task ["REWARD_DAY"],
#                                    example_task ["TO_REINVEST"],
#                                    rate_change_date= date(2024, 4, 15),
#                                    new_rate_prc=10,
#                                    )

# example_task_reward_log = example_task_staker.get_staking_log()


# invalid = task_defs["invalid"]
# invalid_staker =  EthereumStakingCalculator(invalid["ETH_INVESTED"],
#                                    invalid ["STAKING_REWARD"],
#                                    invalid ["START_DATE"],
#                                    invalid ["DURATION_MONTHS"],
#                                    invalid ["REWARD_DAY"],
#                                    invalid ["TO_REINVEST"],
#                                    invalid ["RATE_CHANGE_DATE"],
#                                    invalid ["RATE_CHANGE_TO"],
#                                    )

# invalid_staker.get_staking_log()


if __name__ == "__main__":
    parser = ArgumentParser("main", description="Ethereum Staking Profit Calculator")

    parser.add_argument("Amount", help=" initial investment amount of ETH", type=float)
    parser.add_argument(
        "Rate", help=" yearly staking reward rate in percentage ", type=float
    )
    parser.add_argument("Start_date", help=" staking start date in ISO (2024-12-1)")
    parser.add_argument("Duration", help=" staking duration in months", type=int)
    parser.add_argument("Payment", help=" staking reward payment day", type=int)
    parser.add_argument(
        "Reinvest",
        help=" if reinvest staking rewards on receiving",
        type=int,
        choices=[1, 0],
    )

    parser.add_argument(
        "-rc", help=" CHANGED_RATE_DAY in ISO, CHANGED_RATE", nargs=2
    )

    args = parser.parse_args()

    rate_change_date = None
    rate_changed = None

    if args.rc:
        try:
            rate_change_date = date.fromisoformat(args.rc[0])
            rate_changed = float(args.rc[1])
        except Exception as e:
            raise ValueError(e)


    calc = EthereumStakingCalculator(
        args.Amount,
        args.Rate,
        date.fromisoformat(args.Start_date),
        args.Duration,
        args.Payment,
        bool(args.Reinvest),
        rate_change_date,
        rate_changed
    )
    save_csv("record_files/input.csv", calc.get_staking_log(), ",")


## TODO ###
# Add file name generation (staking_calc_{date}_(1))
# Add documentation on how to use it
# Try on different OS'es

