import csv

def save_csv(file_path: str, reward_log: list[dict], separator:str):
    
    try:
        with open(file_path, "w", newline="", encoding="utf-8") as output_file:

            header = reward_log[0].keys()
            
            writer = csv.writer(output_file, delimiter=separator)
            # Write separator to properly display data
            writer.writerow([f"sep={separator}"])

            writer.writerow(header)

            # Loop through records to get their values associated with keys
            for i in range(len(reward_log)):
                writer.writerow(reward_log[i].values())
    except PermissionError as e:
        raise PermissionError("Close file before creating a new one or check if directory exists")    
    
