# Open the input file
with open('output_file.csv', 'r') as file:
    lines = file.readlines()

# Open a new output file to write the modified data
with open('output_file.txt', 'w') as file:
    # Iterate through each line
    for line in lines:
        # Split the line by commas
        values = line.strip().split(',')
        # Iterate through each value and add single quotes
        modified_values = [f"'{value.strip()}'" if value.strip() != 'NULL' else 'NULL' for value in values]
        # Join the modified values with commas and write to the output file
        file.write(', '.join(modified_values) + '\n')
