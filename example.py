import config
from helpers.helpers import save_csv

from staking_calculator.staking_calculator import EthereumStakingCalculator


def run_example():
    example_task = config.task_defs["example_task"]
    main_task = config.task_defs["main_task"]
    bonus_task = config.task_defs["bonus_task_rate_change"]

    example_task_staker = EthereumStakingCalculator(
        example_task["ETH_INVESTED"],
        example_task["STAKING_REWARD"],
        example_task["START_DATE"],
        example_task["DURATION_MONTHS"],
        example_task["REWARD_DAY"],
        example_task["TO_REINVEST"],
    )

    main_task_staker = EthereumStakingCalculator(
        main_task["ETH_INVESTED"],
        main_task["STAKING_REWARD"],
        main_task["START_DATE"],
        main_task["DURATION_MONTHS"],
        main_task["REWARD_DAY"],
        main_task["TO_REINVEST"],
    )

    bonus_task_staker = EthereumStakingCalculator(
        bonus_task["ETH_INVESTED"],
        bonus_task["STAKING_REWARD"],
        bonus_task["START_DATE"],
        bonus_task["DURATION_MONTHS"],
        bonus_task["REWARD_DAY"],
        bonus_task["TO_REINVEST"],
        bonus_task["RATE_CHANGE_DATE"],
        bonus_task["RATE_CHANGE_TO"],
    )

    example_task_log = example_task_staker.get_staking_log()
    main_task_log = main_task_staker.get_staking_log()
    bonus_task_log = bonus_task_staker.get_staking_log()

    save_csv(
        config.dir_path + example_task["file_path"], example_task_log, config.separator
    )
    save_csv(config.dir_path + main_task["file_path"], main_task_log, config.separator)
    save_csv(
        config.dir_path + bonus_task["file_path"], bonus_task_log, config.separator
    )


if __name__ == "__main__":
    run_example()
