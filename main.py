from staking_calculator.staking_calculator import EthereumStakingCalculator
from helpers.helpers import save_csv
from datetime import date

task_defs = {
    "main_task": {
        "file_path": "record_files/main_task.csv",
        "ETH_INVESTED": 25,
        "STAKING_REWARD": 10,
        "START_DATE": date(2024, 4, 15),
        "DURATION_MONTHS": 24,
        "REWARD_DAY": 23,
        "TO_REINVEST": True,
    },
    "bonus_task1":{
        "file_path": "record_files/bonus_task1.csv",
        "ETH_INVESTED": 25,
        "STAKING_REWARD": 0,
        "START_DATE": date(2024, 3, 15),
        "DURATION_MONTHS": 25,
        "REWARD_DAY": 23,
        "TO_REINVEST": True,
        "RATE_CHANGE_DATE": date(2024, 4, 15),
        "RATE_CHANGE_TO": 10 # %
    }

}

main_task = task_defs["main_task"]

main_task_staker = EthereumStakingCalculator(main_task["ETH_INVESTED"], 
                                   main_task["STAKING_REWARD"], 
                                   main_task["START_DATE"], 
                                   main_task["DURATION_MONTHS"], 
                                   main_task["REWARD_DAY"], 
                                   main_task["TO_REINVEST"])

main_task_reward_log = main_task_staker.get_staking_log()

bonus_task = task_defs["bonus_task1"]

bonus_task_staker = EthereumStakingCalculator(bonus_task ["ETH_INVESTED"], 
                                   bonus_task ["STAKING_REWARD"], 
                                   bonus_task ["START_DATE"], 
                                   bonus_task ["DURATION_MONTHS"], 
                                   bonus_task ["REWARD_DAY"], 
                                   bonus_task ["TO_REINVEST"],
                                   rate_change= date(2024, 4, 15),
                                   new_rate=10,
                                   )

bonus_task_reward_log = bonus_task_staker.get_staking_log()


if __name__ == "__main__":
    save_csv(main_task["file_path"], main_task_reward_log, ",")
    save_csv(bonus_task["file_path"], bonus_task_reward_log, ",")
    pass


## TODO ###
    # Finish MAIN TASK
    # Add bonus task 1
        # The input data from is the same, but starting from 2025-04-15 cryptocurrency exchange decided that yearly rewardTask 1 rates will be lowered to 8% from initial 10%
    # Add tests
    # Write a program that allows entering input data described above;
    # Add documentation on how to use it
    # Try on different OS'es