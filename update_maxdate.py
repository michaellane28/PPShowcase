import re
from datetime import datetime, timezone

# Read the script file
with open('script.js', 'r') as file:
    script_content = file.read()

# Extract current maxDate
match = re.search(r'Date.UTC\((\d+), (\d+), (\d+)\)', script_content)
if match:
    year, month, day = map(int, match.groups())
    # Convert extracted date to datetime object (months are zero-based in Date.UTC)
    current_max_date = datetime(year, month + 1, day, tzinfo=timezone.utc).date()
else:
    # If no maxDate found, set to the earliest possible date
    current_max_date = datetime.min.date()

# Get today's date in UTC
today = datetime.now(timezone.utc).date()

# Compare today's date with current maxDate
if today > current_max_date:
    # Update maxDate to today's date
    updated_content = re.sub(
        r'Date.UTC\(\d+, \d+, \d+\)',
        f'Date.UTC({today.year}, {today.month - 1}, {today.day})',
        script_content
    )
    # Write the updated content back to script.js
    with open('script.js', 'w') as file:
        file.write(updated_content)
    print(f"maxDate updated to {today}")
else:
    print("No update required.")