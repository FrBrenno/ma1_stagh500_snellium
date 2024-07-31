def analyze_usb_sniffing(csv_file):
    pair_time_in_out = []
    time_diffs = []

    with open(csv_file, "r") as file:
        lines = file.readlines()

        # Remove the first two lines
        lines = lines[1:]

        # for each URB_BULK out find the corresponding URB_BULK in  
        for i in range(0, len(lines), 1):
            if "URB_BULK out" in lines[i]:
                j = i + 1
                while j < len(lines) and "URB_BULK in" not in lines[j]:
                    j += 1
                if j < len(lines):
                    pair_time_in_out.append((lines[i], lines[j]))

        # Compute the time difference between the URB_BULK out and the URB_BULK in
        for pair in pair_time_in_out:
            time_out = float(pair[0].split(",")[1].strip('"'))
            time_in = float(pair[1].split(",")[1].strip('"'))
            time_diff = time_in - time_out
            time_diffs.append(time_diff)

    # Compute the average time difference
    avg_time_diff = sum(time_diffs) / len(time_diffs)
    
    print(f"Analyzing file {csv_file}")
    print(f"Number of pairs of URB_BULK out and URB_BULK in: {len(pair_time_in_out)}")
    print(f"Average time difference between the transmission of the command and its response: {avg_time_diff}s")
    
    nb_pairs = len(pair_time_in_out)
    
    return nb_pairs, avg_time_diff
    
    
if __name__ == "__main__":
    csv_files = ["../docs/usb_sniffing.csv",
                 "../docs/usb_sniffing_2.csv",
                 "../docs/usb_sniffing_3_random.csv",
                 "../docs/usb_sniffing_4_random.csv",
                 "../docs/usb_sniffing_5_random.csv",
                 ]
    results = []
    
    
    for csv_file in csv_files:
        nb_pairs, avg_time = analyze_usb_sniffing(csv_file)
        results.append((nb_pairs, avg_time))
        print()
  
    avg_time_diffs = sum([result[1] for result in results]) / len(results)
    print(f"Average time difference between the transmission of the command and its response: {avg_time_diffs}s")
    # write the results to a file
    with open("../docs/usb_sniffing_analysis.txt", "w") as file:
        file.write("Summary of the analysis of the USB sniffing\n\n")    
        file.write(f"Average time difference between the transmission of the command and its response: {avg_time_diffs} s\n\n")
        for i, result in enumerate(results):
            file.write(f"Analysis of file {csv_files[i]}\n")
            file.write(f"Number of pairs of URB_BULK out and URB_BULK in: {result[0]}\n")
            file.write(f"Average time difference between the transmission of the command and its response: {result[1]} s\n\n")
        