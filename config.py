from datetime import date

# Variables for saving files
separator = ","
dir_path = "record_files/"
input_save_path = dir_path + "stake_input.csv"

# Examples
example = {
    "file_path": "example_task.csv",
    "ETH_INVESTED": 10,
    "STAKING_REWARD": 7,
    "START_DATE": date(2020, 11, 10),
    "DURATION_MONTHS": 24,
    "REWARD_DAY": 15,
    "TO_REINVEST": True,
}
