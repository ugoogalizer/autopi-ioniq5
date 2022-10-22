# References: https://community.autopi.io/t/copying-txt-pid-file-from-torque-pro/1031/2

import csv 



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

with open('example.csv', mode='r') as csv_file:
    #csv_reader = csv.DictReader(csv_file)
    csv_reader = csv.DictReader(filter(lambda row: row[0]!='~', csv_file))
    



    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            # Column names are Name, ShortName, ModeAndPID, Equation, Min Value, Max Value, Units, Header
            line_count += 1
         #print(f'\t{row["name"]} works in the {row["department"]} department, and was born in {row["birthday month"]}.')
        print(f'\t{row["Name"]}\trow["Equation"]')
        
        #Drop any rows with the string "val" in them
        if "val" in row["Equation"]:
            del csv_reader[row]

        # Iterate over all key-value pairs in dictionary 
        for key, value in char_to_replace.items():
            # Replace key character with value character in string
            row["Name"] = row["Name"].replace(key, value)

        print(f'\t{row["Name"]}\trow["Equation"]')
        line_count += 1
    print(f'Processed {line_count} lines.')


    print(colNameToNum('aaa'))

    #Now start to substitute


    #for row in csv_reader:
       # line_count += 1
    #print(f'Processed {line_count} lines.')