from dateutil.relativedelta import relativedelta
from datetime import date, timedelta
import csv

from numbers import Number

class EthereumStakingCalculator():
    def __init__(self, eth_stake_amount: Number, stake_reward_prc: Number, start_date: date, duration_months: int, reward_payment_day: int, reinvest_reward: bool) -> None:
        self.eth_stake_amount = eth_stake_amount
        self.stake_reward_prc = stake_reward_prc / 100
        self.start_date = start_date
        self.duration_months = duration_months
        self.reward_payment_day = reward_payment_day
        self.reinvest_reward = reinvest_reward

        self.__set_end_date()
        self.__set_active_date()
        self.__set_reward_tracking()
        self.__set_daily_reward_rate()

        self.__calculate_profit_schedule()

    def __set_reward_tracking(self) -> None:
        self.reward_records = []
        self.reward_amount, self.total_reward_amount = (0, 0)

    def __set_daily_reward_rate(self) -> None:
        self.daily_reward_rate = (self.stake_reward_prc) / 365 * self.eth_stake_amount

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
        if self.active_date.month == 12:
            year += 1
            month = 1
        # Days till next month on same year
        elif not self.active_date.day < self.reward_payment_day:
            month += 1

        reward_upcoming_date = date(year, month, self.reward_payment_day)
        
        self.days_to_next_reward_payment = (reward_upcoming_date - self.active_date).days
    
    def __adjust_reward_payment_days(self) -> None:
        # Adjust next reward days when start date day is not on reward day
        # Because we'd run past staking end day
        # e.g. start date day is higher/lower than reward day 
        self.days_to_next_reward_payment = (self.end_date - self.active_date).days


    def __is_final_staking_period(self) -> bool:
        # Days till reward payment day is less than a month = final staking period
        return (self.end_date - self.active_date).days < 28

    def __get_reward_record(self, current_line: int, reward_amount: Number) -> dict:
        # Create dict for each reward payout
        # To avoid key/value count misallignment if we stored keys and values in separate lists
        return {
                "Line #": current_line,
                "Reward Date": self.active_date, 
                "Investment Amount": round(self.eth_stake_amount, 6),
                "Current Month Reward Amount": round(reward_amount, 6),
                "Total Reward Amount To Date": round(self.total_reward_amount, 6),
                "Staking Reward Rate": f"{self.stake_reward_prc:.2f}%"
            }

    def __calculate_profit_schedule(self) -> None:
        current_line = 1
        while True:
            self.__set_days_to_next_reward_payment()
            
            if self.active_date == self.end_date:
                break

            if self.__is_final_staking_period():
                self.__adjust_reward_payment_days()

            reward_amount = self.daily_reward_rate * self.days_to_next_reward_payment

            self.total_reward_amount += reward_amount

            # Change active date to upcoming reward date 
            # Because we already calculated rewards for current date
            self.active_date += timedelta(days=self.days_to_next_reward_payment)

            reward = self.__get_reward_record(current_line, reward_amount)

            # Save records which later will be written to CSV
            self.reward_records.append(reward)
            
            if self.reinvest_reward:
                self.eth_stake_amount += reward_amount
                
                # Update daily reward rate on each iteration
                # Because it changes when reinvesting the reward
                self.__set_daily_reward_rate()
            
            current_line += 1
    
    def get_staking_log(self) -> list[dict]:
        return self.reward_records

ETH_INVESTED = 10
STAKING_REWARD = 7 # %
START_DATE = date.fromisoformat('2020-11-20')
DURATION_MONTHS = 24
REWARD_DAY = 15
TO_REINVEST = True

staker = EthereumStakingCalculator(ETH_INVESTED, STAKING_REWARD, START_DATE, DURATION_MONTHS, REWARD_DAY, TO_REINVEST)
rewards_list = staker.get_staking_log()


file_path = "data.csv"

with open(file_path, "w", newline="", encoding="utf-8") as output_file:
    csv_separator = ","

    header = rewards_list[0].keys()
    
    writer = csv.writer(output_file, delimiter=csv_separator)
    # Write separator to properly display data
    writer.writerow([f"sep={csv_separator}"])

    writer.writerow(header)

    # Loop through records to get their values associated with keys
    for i in range(len(rewards_list)):
        writer.writerow(rewards_list[i].values())



## TODO ###
# Finish MAIN TASK
# Add bonus task 1
    # The input data from is the same, but starting from 2025-04-15 cryptocurrency exchange decided that yearly rewardTask 1 rates will be lowered to 8% from initial 10%
# Add tests
# Write a program that allows entering input data described above;
# Add documentation on how to use it
# Try on different OS'es
