# Ethereum Staking Profit Calculator

## A fully functional Ethereum Staking Calculator written in Python calculating Ethereum staking rewards and producing staking schedule

This project was built for internship entry task which was to write a simplified **Ethereum Staking profit calculator**.

## Features

- Create **staking reward schedule** with:
  - Reward Date
  - Investment Amount
  - Current Month Reward Amount
  - Total Reward Amount To Date
  - Staking Reward Rate
- Ouptut reward schedule in **CSV** file
- Handles **date overflow** - when reward day doesn't exist in the current month

## Installing

1. Clone the repository:

- [Get ssh key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) if there you encounter problem cloning

```bash
git clone git@github.com:42plat0/Ethereum-Staking-Profit-Calculator.git
cd Ethereum-Staking-Profit-Calculator
```

### or

- [Download project as ZIP](https://github.com/42plat0/Ethereum-Staking-Profit-Calculator/archive/refs/heads/main.zip)
- Unzip
- Cd into folder

```bash
cd Ethereum-Staking-Profit-Calculator-main
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

- Install pip if you do not have it installed

```bash
sudo apt install python3-pip
```

## Usage

```bash
    usage: main [-h] [--ratechange RATECHANGE RATECHANGE] [--filename FILENAME] Amount Rate Start_date Duration Payment {1,0}

    Ethereum Staking Profit Calculator

    positional arguments:
    Amount                initial investment amount of ETH
    Rate                  yearly staking reward rate in percentage
    Start_date            staking start date in ISO (2024-12-1)
    Duration              staking duration in months
    Payment               staking reward payment day
    {1,0}                 if reinvest staking rewards on receiving

    options:
    -h, --help            show this help message and exit
    --ratechange, -rc RATECHANGE RATECHANGE
                            CHANGED_RATE_DAY in ISO, CHANGED_RATE
    --filename, -f FILENAME
                            filename to save logs in
```

## Examples

### Generate example schedule

```bash
python example.py
```

### Generate schedule with input

#### Main task

Code

```bash
python main.py 25 10 2024-04-15 24 23 1 -f main_task
```

CSV file

```csv
"sep=,"
Line #,Reward Date,Investment Amount,Current Month Reward Amount,Total Reward Amount To Date,Staking Reward Rate
1,2024-04-23, 25.000000, 0.054795, 0.054795,10.00%
2,2024-05-23, 25.054795, 0.205930, 0.260724,10.00%
3,2024-06-23, 25.260724, 0.214543, 0.475267,10.00%
4,2024-07-23, 25.475267, 0.209386, 0.684653,10.00%
5,2024-08-23, 25.684653, 0.218144, 0.902797,10.00%
6,2024-09-23, 25.902797, 0.219996, 1.122793,10.00%
7,2024-10-23, 26.122793, 0.214708, 1.337501,10.00%
8,2024-11-23, 26.337501, 0.223688, 1.561189,10.00%
9,2024-12-23, 26.561189, 0.218311, 1.779501,10.00%
10,2025-01-23, 26.779501, 0.227442, 2.006943,10.00%
11,2025-02-23, 27.006943, 0.229374, 2.236317,10.00%
12,2025-03-23, 27.236317, 0.208936, 2.445253,10.00%
13,2025-04-23, 27.445253, 0.233097, 2.678350,10.00%
14,2025-05-23, 27.678350, 0.227493, 2.905843,10.00%
15,2025-06-23, 27.905843, 0.237009, 3.142852,10.00%
16,2025-07-23, 28.142852, 0.231311, 3.374163,10.00%
17,2025-08-23, 28.374163, 0.240986, 3.615149,10.00%
18,2025-09-23, 28.615149, 0.243033, 3.858182,10.00%
19,2025-10-23, 28.858182, 0.237191, 4.095372,10.00%
20,2025-11-23, 29.095372, 0.247111, 4.342483,10.00%
21,2025-12-23, 29.342483, 0.241171, 4.583655,10.00%
22,2026-01-23, 29.583655, 0.251258, 4.834913,10.00%
23,2026-02-23, 29.834913, 0.253392, 5.088305,10.00%
24,2026-03-23, 30.088305, 0.230814, 5.319120,10.00%
25,2026-04-15, 30.319120, 0.191052, 5.510172,10.00%
```

#### Bonus task
Code

```bash
python main.py 25 10 2024-04-15 24 23 1 -rc 2025-04-15 8 -f main_task_bonus
```

CSV

```csv
"sep=,"
Line #,Reward Date,Investment Amount,Current Month Reward Amount,Total Reward Amount To Date,Staking Reward Rate
1,2024-04-23, 25.000000, 0.054795, 0.054795,10.00%
2,2024-05-23, 25.054795, 0.205930, 0.260724,10.00%
3,2024-06-23, 25.260724, 0.214543, 0.475267,10.00%
4,2024-07-23, 25.475267, 0.209386, 0.684653,10.00%
5,2024-08-23, 25.684653, 0.218144, 0.902797,10.00%
6,2024-09-23, 25.902797, 0.219996, 1.122793,10.00%
7,2024-10-23, 26.122793, 0.214708, 1.337501,10.00%
8,2024-11-23, 26.337501, 0.223688, 1.561189,10.00%
9,2024-12-23, 26.561189, 0.218311, 1.779501,10.00%
10,2025-01-23, 26.779501, 0.227442, 2.006943,10.00%
11,2025-02-23, 27.006943, 0.229374, 2.236317,10.00%
12,2025-03-23, 27.236317, 0.208936, 2.445253,10.00%
13,2025-04-23, 27.445253, 0.221066, 2.666319,8.00%
14,2025-05-23, 27.666319, 0.181916, 2.848235,8.00%
15,2025-06-23, 27.848235, 0.189215, 3.037450,8.00%
16,2025-07-23, 28.037450, 0.184356, 3.221806,8.00%
17,2025-08-23, 28.221806, 0.191754, 3.413559,8.00%
18,2025-09-23, 28.413559, 0.193057, 3.606616,8.00%
19,2025-10-23, 28.606616, 0.188098, 3.794714,8.00%
20,2025-11-23, 28.794714, 0.195646, 3.990360,8.00%
21,2025-12-23, 28.990360, 0.190622, 4.180982,8.00%
22,2026-01-23, 29.180982, 0.198271, 4.379253,8.00%
23,2026-02-23, 29.379253, 0.199618, 4.578871,8.00%
24,2026-03-23, 29.578871, 0.181525, 4.760396,8.00%
25,2026-04-15, 29.760396, 0.150025, 4.910421,8.00%
```
