from struct import unpack
import glob
import pandas as pd

def parse_binary( raw_data ):
	"""
	Takes a raw binary string containing data from our oscilloscope.
	Returns the corresponding float vector.
	"""
	ins =  4   # Size of int stored if the raw binary string
	cur =  0   # Cursor walking in the string and getting data
	cur += 12  # Skipping the global raw binary string header
	whs =  unpack("i", raw_data[cur:cur+ins])[0] # Storing size of the waveform header
	cur += whs # Skipping the waveform header
	dhs =  unpack("i", raw_data[cur:cur+ins])[0] # Storing size of the data header
	cur += dhs # Skipping the data header
	bfs =  unpack("i", raw_data[cur-ins:cur])[0] # Storing the data size
	sc  =  bfs/ins # Samples Count - How much samples compose the wave
	dat =  unpack("f"*int(sc), raw_data[cur:cur+bfs])
	return dat

# Path to the directory with CSV files
dataset_dir = "secmatv1_2006_04_0809/"
files = glob.glob(f"{dataset_dir}/*.bin")

trace_data = []

i = 0
for file_name in files:
	with open(file_name, mode='rb') as file: # b is important -> binary
		fileContent = file.read()
		data = parse_binary(fileContent)

		power_value = data[15749] # Paper says they used the 15750th time step

		# Extract key, plaintext, and ciphertext
		parts = file_name.split("__")
		key = parts[1].split("_m=")[0].split("k=")[1]
		plaintext = parts[1].split("_c=")[0].split("_m=")[1]
		ciphertext = parts[1].split("_c=")[1].split(".bin")[0]

		# Append to the list
		trace_data.append({
			"Filepath": file_name,
			"Key": key,
			"Plaintext": plaintext,
			"Ciphertext": ciphertext,
			"Power": power_value
		})
		i +=1
		print(f"{i}/{len(files)}: Extracted Data for {file_name}")

# Convert to DataFrame for easier handling
trace_df = pd.DataFrame(trace_data)
trace_df.to_csv("processed_trace_data.csv", index=False)
print(f"Saved data to csv")