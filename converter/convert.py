# References: https://community.autopi.io/t/copying-txt-pid-file-from-torque-pro/1031/2

import csv, copy, re

# Function to convert the letter conventions used in Torque Pro (and Excel columns to numbers)
# Attribution to: https://code-examples.net/en/q/16c19b0
def colNameToNum(name):
    pow = 1
    colNum = 0
    for letter in name[::-1]:
            colNum += (int(letter, 36) -9) * pow
            pow *= 26
    return colNum


#List of all the string replacements to be done
char_to_replace = {
    'Tire': '2', 
    'Temp': 'TEMP54', 
    'Right': 'RIIIIIIGHT'
    }

csv_file = open('example.csv', mode='r') 
#pid_list = csv.DictReader(csv_file)
dict_reader = csv.DictReader(filter(lambda row: row[0]!='~', csv_file))

#ordered_dict_from_csv = list(dict_reader)

# Get a list of dictionaries
pid_list_raw = list(dict_reader)

# Filter out anything with the string "val" in it, asI don't know how/if autopi can use other PIDs in an equation
pid_list = [d for d in pid_list_raw if "val" not in d['Equation']]


#iterate over the list of pids
line_count = 0
for row in pid_list:
    if line_count == 0:
        print(f'Column names are {", ".join(row)}')
        # Column names are Name, ShortName, ModeAndPID, Equation, Min Value, Max Value, Units, Header
        line_count += 1
        #print(f'\t{row["name"]} works in the {row["department"]} department, and was born in {row["birthday month"]}.')
    #print(f'\t{row["Name"]}\t{row["Equation"]}')
    
    
    row['Converted'] = "test"
    #regex1 = re.compile('SIGNED\(', re.IGNORECASE)
    row['Converted'] = re.sub(r'(?i)(SIGNED)\(',r'\1twos_comp',row["Equation"])

    
    #“SIGNED(singlebyte)” -> “twos_comp(singlebyte,8)”
    #“SIGNED(doublebyte)” -> “twos_comp(doublebyte,16)”


    # Iterate over all key-value pairs in dictionary 
    for key, value in char_to_replace.items():
        # Replace key character with value character in string
        row["Name"] = row["Name"].replace(key, value)



    print(f'\t{row["Name"]}\t{row["Equation"]}\t{row["Converted"]}')
    line_count += 1
print(f'Processed {line_count} lines.')


print(colNameToNum('aaa'))

#Now start to substitute


#for row in pid_list:
    # line_count += 1
#print(f'Processed {line_count} lines.')