import re
from datetime import datetime, timedelta

# Path to the script.js file
script_path = 'script.js'

# Read the existing script.js file
with open(script_path, 'r') as file:
    script_content = file.read()

# Define a pattern to find and update the maxDate and currentDate
max_date_pattern = r'const maxDate = new Date\(Date\.UTC\((\d+), (\d+), (\d+)\)\);'
current_date_pattern = r'let currentDate = new Date\(Date\.UTC\((\d+), (\d+), (\d+)\)\);'

# Function to update date
def update_date(pattern, script_content):
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

        # Format the new date value
        new_date_str = f'const maxDate = new Date(Date.UTC({new_year}, {new_month}, {new_day}));' if 'maxDate' in pattern else f'let currentDate = new Date(Date.UTC({new_year}, {new_month}, {new_day}));'
        
        # Replace the old date with the new one
        updated_script_content = re.sub(pattern, new_date_str, script_content)
        return updated_script_content
    else:
        print('Date not found in script.js')
        return script_content

# Update maxDate
script_content = update_date(max_date_pattern, script_content)
# Update currentDate
script_content = update_date(current_date_pattern, script_content)

# Write the updated content back to script.js
with open(script_path, 'w') as file:
    file.write(script_content)

print('Updated dates in script.js')