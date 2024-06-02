def clean_data(datafile, newfile):
    with open(newfile, "w") as f:
        for line in datafile.open():
            cleaned_line = line[1:-2] + "\n"
            f.write(cleaned_line)
