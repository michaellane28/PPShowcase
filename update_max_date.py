import re
from datetime import datetime, timedelta

# Path to the script.js file
script_path = 'script.js'

# Read the existing script.js file
with open(script_path, 'r') as file:
    script_content = file.read()

# Define a pattern to find and update the maxDate
pattern = r'const maxDate = new Date\(Date\.UTC\((\d+), (\d+), (\d+)\)\);'
match = re.search(pattern, script_content)

if match:
    year, month, day = map(int, match.groups())
    # Create a datetime object and increment by one day
    current_date = datetime(year, month + 1, day)  # Months are zero-indexed
    new_date = current_date + timedelta(days=1)
    
    # Adjust month and year if necessary
    new_month = new_date.month - 1  # Months are zero-indexed
    new_year = new_date.year
    new_day = new_date.day

    # Format the new maxDate value
    new_max_date_str = f'const maxDate = new Date(Date.UTC({new_year}, {new_month}, {new_day}));'
    
    # Replace the old maxDate with the new one
    updated_script_content = re.sub(pattern, new_max_date_str, script_content)

    # Write the updated content back to script.js
    with open(script_path, 'w') as file:
        file.write(updated_script_content)

    print(f'Updated maxDate to {new_max_date_str}')
else:
    print('maxDate not found in script.js')