from dateutil.relativedelta import relativedelta
from datetime import date, timedelta
import csv

# DEFINITIONS
ETH_INVESTED = 10
STAKING_REWARD = 7 # %
START_DATE = date.fromisoformat('2024-10-15')
DURATION_MONTHS = 24
REWARD_DAY = 15
TO_REINVEST = True

RATE_CHANGE_DATE = date(2024, 4, 15)
RATE_CHANGE_TO = 7 # %

###### DONE
END_DATE = START_DATE + relativedelta(months=DURATION_MONTHS) 

###### DONE
reward_amount = 0
total_reward_amount = 0
curr_date = START_DATE



###### DONE
rewards_list = []


def get_month_day_diff(curr_date, end_date, reward_day):
    # When reward day is on the same month as start date
    # By default will create next date in same month
    year = curr_date.year
    month = curr_date.month
    # Days till reward when reward is following year
    if curr_date.month == 12:
        year += 1
        month = 1
    # Days till next month on same year
    elif not curr_date.day < reward_day:
        # next_date = date(curr_date.year, curr_date.month, reward_day)
        month += 1

    
    next_date = date(year, month, reward_day)
    # Set reward date to end date when start date day is not on reward day
    # Because we'd run past staking end day
    if (end_date - curr_date).days < 28:
        return (end_date - curr_date).days
    
    return (next_date - curr_date).days



i = 0
while True:
    if curr_date == END_DATE:
        break
    
    days_till_reward = get_month_day_diff(curr_date,END_DATE, REWARD_DAY)
    
    ###### DONE
    reward_amount = (STAKING_REWARD / 100) / 365 * 1 * ETH_INVESTED
    reward_amount *= days_till_reward

    if 0 <= (RATE_CHANGE_DATE - curr_date).days < 28:
        print("old rate times ", (RATE_CHANGE_DATE - curr_date).days)
        print("new rate days: ", days_till_reward - (RATE_CHANGE_DATE - curr_date).days)
        # Calculate reward amount for days that old rate still applies
        reward_amount = (STAKING_REWARD / 100) / 365 * 1 * ETH_INVESTED * (RATE_CHANGE_DATE - curr_date).days # times old rate days
        # Change rate to a new one and apply reward with new rate till reward payment day
        STAKING_REWARD = RATE_CHANGE_TO 
        reward_amount += (STAKING_REWARD / 100) / 365 * 1 * ETH_INVESTED * (days_till_reward - (RATE_CHANGE_DATE - curr_date).days)
        

    print((STAKING_REWARD / 100) / 365 * 1 * ETH_INVESTED, days_till_reward, reward_amount)

    total_reward_amount += reward_amount

    curr_date += timedelta(days=days_till_reward)

    reward = {
        "Line #": i+1,
        "Reward Date": curr_date,
        "Investment Amount": round(ETH_INVESTED, 6),
        "Current Month Reward Amount": round(reward_amount, 6),
        "Total Reward Amount To Date": round(total_reward_amount, 6),
        "Staking Reward Rate": f"{STAKING_REWARD:.2f}%"
    }

    rewards_list.append(reward)
    
    if TO_REINVEST:
        ETH_INVESTED += reward_amount
    


    i+= 1


# write to csv

file_path = "record_files/data_not_obj.csv"

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




