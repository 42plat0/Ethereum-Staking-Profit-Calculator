from argparse import ArgumentParser
from datetime import date

from staking_calculator.staking_calculator import EthereumStakingCalculator
from helpers.helpers import save_csv
import config


def main():
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
        "--ratechange", "-rc", help=" CHANGED_RATE_DAY in ISO, CHANGED_RATE", nargs=2
    )

    parser.add_argument("--filename", "-f", help=" filename to save logs in")

    args = parser.parse_args()

    rate_change_date = None
    rate_changed = None

    if args.ratechange:
        try:
            rate_change_date = date.fromisoformat(args.ratechange[0])
            rate_changed = float(args.ratechange[1])
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
        rate_changed,
    )

    if args.filename:
        save_path = config.dir_path + f"{args.filename}.csv"  # Filename
        try:
            save_csv(save_path, calc.get_staking_log(), config.separator)
        except Exception as e:
            raise ValueError(e)
        else:
            return 0

    save_csv(config.input_save_path, calc.get_staking_log(), config.separator)

    return 0


if __name__ == "__main__":
    main()


## TODO ###
# Add documentation on how to use it
# Try on different OS'es
