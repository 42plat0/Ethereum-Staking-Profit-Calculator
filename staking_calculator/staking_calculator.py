from dateutil.relativedelta import relativedelta
import datetime
import csv

class EthereumStakingCalculator():
    def __init__(self, eth_stake_amount, stake_reward_prc, start_date, duration_months, reward_payment_day, reinvest_reward):
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
        self.__set_staking_end_indicator(False)

    def __set_reward_tracking(self):
        self.reward_records = []
        self.reward_amount, self.total_reward_amount = (0, 0)

    def __set_daily_reward_rate(self):
        self.daily_reward_rate = (self.stake_reward_prc) / 365 * self.eth_stake_amount

    def __set_end_date(self):
        self.end_date = self.start_date + relativedelta(months=self.duration_months)
    
    def __set_active_date(self):
        self.active_date = self.start_date
    
    def __set_staking_end_indicator(self, is_end_of_staking):
        self.end_staking = is_end_of_staking

    def __set_days_to_next_reward_payment(self):
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

        reward_upcoming_date = datetime.date(year, month, self.reward_payment_day)
        
        self.days_to_next_reward_payment = (reward_upcoming_date - self.active_date).days
    
    def adjust_reward_payment_days(self):
        # Adjust next reward days when start date day is not on reward day
        # Because we'd run past staking end day
        # e.g. start date day is higher/lower than reward day 
        self.days_to_next_reward_payment = (self.end_date - self.active_date).days

        # As we have to adjust days to next reward payment
        # We have reached the end of staking
        self.__set_staking_end_indicator(True)

    def is_final_staking_period(self):
        # Days till reward payment day is less than a month = final staking period
        return (self.end_date - self.active_date).days < 28

    def calculate_profit_schedule(self):
        line = 0
        while True:
            self.__set_days_to_next_reward_payment()

            if self.is_final_staking_period():
                self.adjust_reward_payment_days()

            if self.end_staking:
                break

            reward_amount = self.daily_reward_rate * self.days_to_next_reward_payment

            self.total_reward_amount += reward_amount

            # Change active date to upcoming reward date 
            # Because we already calculated rewards for current date
            self.active_date += datetime.timedelta(days=self.days_to_next_reward_payment)

            # Create dict for each reward payout
            # To avoid key/value count misallignment if we stored keys and values in separate lists
            reward = {
                "Line #": line+1,
                "Reward Date": self.active_date, 
                "Investment Amount": round(self.eth_stake_amount, 6),
                "Current Month Reward Amount": round(reward_amount, 6),
                "Total Reward Amount To Date": round(self.total_reward_amount, 6),
                "Staking Reward Rate": f"{self.stake_reward_prc:.2f}%"
            }

            # Save records which later will be written to CSV
            self.reward_records.append(reward)
            
            if self.reinvest_reward:
                self.eth_stake_amount += reward_amount
                
                # Update daily reward rate on each iteration
                # Because it changes when reinvesting the reward
                self.__set_daily_reward_rate()
            
            line += 1
    
    def get_staking_log(self):
        self.calculate_profit_schedule()
        return self.reward_records

ETH_INVESTED = 10
STAKING_REWARD = 7 # %
START_DATE = datetime.date.fromisoformat('2020-11-20')
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