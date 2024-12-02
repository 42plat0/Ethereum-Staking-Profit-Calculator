from datetime import date

# Variables for saving files
separator = ","
dir_path = "record_files/"
input_save_path = dir_path + "stake_input.csv"

# Examples
task_defs = {
    "example_task": {
        "file_path": "example_task.csv",
        "ETH_INVESTED": 10,
        "STAKING_REWARD": 7,
        "START_DATE": date(2020, 11, 10),
        "DURATION_MONTHS": 24,
        "REWARD_DAY": 15,
        "TO_REINVEST": True,
    },
    "main_task": {
        "file_path": "main_task.csv",
        "ETH_INVESTED": 25,
        "STAKING_REWARD": 10,
        "START_DATE": date(2024, 4, 15),
        "DURATION_MONTHS": 24,
        "REWARD_DAY": 23,
        "TO_REINVEST": True,
    },
    "bonus_task_rate_change": {
        "file_path": "bonus_task_rate_change.csv",
        "ETH_INVESTED": 25,
        "STAKING_REWARD": 10,
        "START_DATE": date(2024, 4, 15),
        "DURATION_MONTHS": 24,
        "REWARD_DAY": 23,
        "TO_REINVEST": True,
        "RATE_CHANGE_DATE": date(2025, 4, 15),
        "RATE_CHANGE_TO": 8,  # %
    },
}
