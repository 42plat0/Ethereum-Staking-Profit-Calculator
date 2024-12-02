from dateutil.relativedelta import relativedelta
from datetime import date, timedelta

from numbers import Number


class EthereumStakingCalculator:

    def __init__(
        self,
        eth_amount: Number,
        reward_rate_prc: Number,
        start_date: date,
        duration_months: int,
        reward_payment_day: int,
        reinvest_reward: bool,
        rate_change_date: date = None,
        new_rate_prc: Number = None,
    ) -> None:

        self.eth_stake_amount = eth_amount
        self.stake_reward = reward_rate_prc
        self.start_date = start_date
        self.duration_months = duration_months
        self.reward_payment_day = reward_payment_day
        self.reinvest_reward = reinvest_reward

        self.rate_change_date = (
            rate_change_date if rate_change_date is not None else None
        )
        self.new_rate = new_rate_prc if new_rate_prc is not None else None

        self.__check_init_values()
        self.__set_end_date()
        self.__set_active_date()
        self.__set_reward_tracking()
        self.__set_daily_reward_rate()

        self.__calculate_profit_schedule()

    def __check_init_values(self) -> None | ValueError:
        if (
            not isinstance(self.eth_stake_amount, (int, float))
            or self.eth_stake_amount <= 0
        ):
            raise ValueError("Stake amount should be a positive number")

        # TODO
        # Would be good change to check if reward is more than 0
        elif not isinstance(self.stake_reward, (int, float)) or self.stake_reward < 0:
            raise ValueError("Stake reward should be a positive number")

        elif not isinstance(self.start_date, date):
            raise ValueError("Staking start date should be a date")

        elif not isinstance(self.duration_months, int) or self.duration_months <= 0:
            raise ValueError("Stake duration should be a positive number (months)")

        elif (
            not isinstance(self.reward_payment_day, int)
            or self.reward_payment_day <= 0
            or self.reward_payment_day > 31
        ):
            raise ValueError(
                "Stake reward payment day should be a number between 1 and 31"
            )

        elif not isinstance(self.reinvest_reward, bool):
            raise ValueError("Reinvest reward should be a boolean value")

        elif (
            not isinstance(self.rate_change_date, date)
            and self.rate_change_date is not None
        ):
            raise ValueError("Rate change date should be a date")

        elif self.new_rate is not None:
            if not isinstance(self.new_rate, (int, float)) or self.new_rate < 0:
                raise ValueError("Changed rate should be a number")

        elif self.start_date is not None and self.new_rate is not None:
            if (self.rate_change_date - self.start_date).days < 0:
                raise ValueError(
                    "Rate change date cannot be earlier than starting day of staking"
                )

    def __set_reward_tracking(self) -> None:
        self.reward_records = []
        self.reward_amount, self.total_reward_amount = (0, 0)

    def __set_daily_reward_rate(self) -> None:
        self.daily_reward_rate = (self.stake_reward / 100) / 365 * self.eth_stake_amount

    def __set_end_date(self) -> None:
        self.end_date = self.start_date + relativedelta(months=self.duration_months)

    def __set_active_date(self) -> None:
        self.active_date = self.start_date

    def __set_days_to_next_reward_payment(self) -> None:
        # When reward day is on the same month as start date
        # By default will create next date in same month
        year = self.active_date.year
        month = self.active_date.month

        # Days till reward when reward is following year
        if self.active_date.month == 12 and not self.active_date.day < self.reward_payment_day:
            year += 1
            month = 1
        # Days till next month on same year
        elif not self.active_date.day < self.reward_payment_day:
            month += 1

        ######
        ### problem is that it gets next reward payment day on same month even with max day limiting
        ### but we dont go to next months pay day!
        ### PROBLEM WE'RE SOLVING:
        ### what if reward day is higher than max active month day?
        try: 
            self.reward_upcoming_date = date(year, month, self.reward_payment_day)
        except ValueError: # Means that selected month has less days than reward is paid on
            payment_day = self.reward_payment_day - 1
            
            # Get active month last day
            # To generate reward when payment day is higher than active month's last day
            active_month_days = (date(year, month + 1, 1) - timedelta(days=1)).day
            if active_month_days > payment_day:
                while active_month_days > payment_day:
                    payment_day -= 1
            elif active_month_days < payment_day:
                while active_month_days < payment_day:
                    payment_day -= 1

            self.reward_upcoming_date = date(year, month, payment_day)
            


        self.days_to_next_reward_payment = (
            self.reward_upcoming_date - self.active_date
        ).days

    def __adjust_reward_payment_days(self) -> None:
        # Adjust next reward days when start date day is not on reward day
        # Because we'd run past staking end day
        # e.g. start date day is higher/lower than reward day
        self.days_to_next_reward_payment = (self.end_date - self.active_date).days - 1 # why -1 tho? TODO

    def __is_final_staking_period(self) -> bool:
        # Days till reward payment day is less than a month = final staking period
        return (self.end_date - self.active_date).days < 28

    def __get_old_rate_days(self) -> int:
        return (self.rate_change_date - self.active_date).days

    def __is_rate_change_date_near(self) -> bool:
        return 0 <= (self.rate_change_date - self.active_date).days < 28

    def __get_reward_record(self, current_line: int, reward_amount: Number) -> dict:
        # Create dict for each reward payout
        # To avoid key/value count misallignment if we stored keys and values in separate lists
        return {
            "Line #": current_line,
            "Reward Date": self.reward_upcoming_date,
            "Investment Amount": f"{self.eth_stake_amount: .6f}",
            "Current Month Reward Amount": f"{reward_amount: .6f}",
            "Total Reward Amount To Date": f"{self.total_reward_amount: .6f}",
            "Staking Reward Rate": f"{self.stake_reward:.2f}%",
            "Days of reward": self.days_to_next_reward_payment,
            "daily rate": self.daily_reward_rate,
            "result": f"{ self.days_to_next_reward_payment * self.daily_reward_rate:.6f}",
            "total_days": (self.end_date - self.start_date).days,
            "daily_rate": self.daily_reward_rate,
            "total_amount_should_be": f"{ (self.end_date - self.start_date).days * self.daily_reward_rate:.6f}"
        }

    def __calculate_profit_schedule(self) -> None:
        current_line = 1
        o = 0
        while True:
            self.__set_days_to_next_reward_payment()

            if self.active_date >= self.end_date:
                break

            if self.__is_final_staking_period():
                self.__adjust_reward_payment_days()

            if self.reward_payment_day > self.reward_upcoming_date.day:
                self.days_to_next_reward_payment += 1

            self.reward_amount = (
                self.daily_reward_rate * self.days_to_next_reward_payment
            )

            if self.rate_change_date and self.new_rate:
                # Add reward amounts of old and new rates
                # Old rate * days till new rate change date + new rate * days till reward day
                if self.__is_rate_change_date_near():
                    old_rate_days = self.__get_old_rate_days()

                    # Calculate reward amount for days that old rate still applies
                    self.reward_amount = self.daily_reward_rate * old_rate_days

                    # Change rate to a new one and apply reward with new rate till reward payment day
                    self.stake_reward = self.new_rate

                    # We have to recalculate daily reward rate because reward percentage changed
                    # And also rate is changed for other stakes too
                    self.__set_daily_reward_rate()

                    # Add reward amount with new rate applied
                    self.reward_amount += self.daily_reward_rate * (
                        self.days_to_next_reward_payment - old_rate_days
                    )

            self.total_reward_amount += self.reward_amount

            # Change active date to upcoming reward date
            # Because we already calculated rewards for current date
            self.active_date += timedelta(days=self.days_to_next_reward_payment)
                
            reward = self.__get_reward_record(current_line, self.reward_amount)




            # Save records which later will be written to CSV
            self.reward_records.append(reward)

            if self.reinvest_reward:
                self.eth_stake_amount += self.reward_amount

                # Update daily reward rate on each iteration
                # Because it changes when reinvesting the reward
                self.__set_daily_reward_rate()

            current_line += 1

    def get_staking_log(self) -> list[dict]:
        return self.reward_records
