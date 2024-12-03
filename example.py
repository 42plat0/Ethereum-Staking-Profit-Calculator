import config
from helpers.helpers import save_csv

from staking_calculator.staking_calculator import EthereumStakingCalculator


def run_example():
    example_task = config.example

    example_task_staker = EthereumStakingCalculator(
        example_task["ETH_INVESTED"],
        example_task["STAKING_REWARD"],
        example_task["START_DATE"],
        example_task["DURATION_MONTHS"],
        example_task["REWARD_DAY"],
        example_task["TO_REINVEST"],
    )

    example_task_log = example_task_staker.get_staking_log()

    save_csv(
        config.dir_path + example_task["file_path"], example_task_log, config.separator
    )


if __name__ == "__main__":
    run_example()
