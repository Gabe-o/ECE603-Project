import pandas as pd
import glob

# Path to the directory with CSV files
dataset_dir = "secmatv1_csv"
csv_files = glob.glob(f"{dataset_dir}/*.csv")

time_point = 15750  # Target time point

# Store parsed data
trace_data = []

# Parse filenames and extract power at the 15750th time point
i=0
for file_path in csv_files:
    # Extract key, plaintext, and ciphertext
    parts = file_path.split("__")
    key = parts[1].split("_m=")[0].split("k=")[1]
    plaintext = parts[1].split("_c=")[0].split("_m=")[1]
    ciphertext = parts[1].split("_c=")[1].split(".csv")[0]
    
    # Load trace data
    trace_df = pd.read_csv(file_path, header=None)
    
    # Extract power at the target time point
    power_value = trace_df.iloc[time_point - 1, 1]
    
    # Append to the list
    trace_data.append({
        "Filepath": file_path,
        "Key": key,
        "Plaintext": plaintext,
        "Ciphertext": ciphertext,
        "Power": power_value
    })
    i +=1
    print(f"{i}/{len(csv_files)}: Extracted Data for {file_path}")

# Convert to DataFrame for easier handling
trace_df = pd.DataFrame(trace_data)
trace_df.to_csv("processed_trace_data.csv", index=False)
print(f"Saved data to csv")