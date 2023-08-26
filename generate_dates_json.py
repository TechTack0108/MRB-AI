import json
from datetime import datetime, timedelta

# Define the start and end years
start_year = 2009
end_year = 2023

# Generate a list of all dates between the start and end years
all_dates = []
current_date = datetime(start_year, 1, 1)
while current_date.year <= end_year:
    all_dates.append(current_date.strftime("%d/%m/%Y"))
    current_date += timedelta(days=1)


# Function to generate all possible date formats for a given date
def generate_formats(date):
    parsed_date = datetime.strptime(date, "%d/%m/%Y")
    formats = [
        parsed_date.strftime("%d/%m/%Y"),
        parsed_date.strftime("%d-%b-%Y"),
        parsed_date.strftime("%d. %b. %Y"),
        parsed_date.strftime("%d %B %Y"),
        parsed_date.strftime("%d/%m/%y"),
        parsed_date.strftime("%m/%d/%Y"),
        parsed_date.strftime("%Y-%m-%d"),
        parsed_date.strftime("%Y/%m/%d"),
        parsed_date.strftime('%B %d" %Y'),
        # ... add more formats as needed
    ]

    return formats


new_formmatted_dates = []
# Generate all possible date formats for each date in the all_dates list
for date in all_dates:
    formats = generate_formats(date)
    new_formmatted_dates.extend(formats)

# write the dates to a json file
with open("data/trained_data/date/mrb_dates.json", "w") as f:
    json.dump(new_formmatted_dates, f, indent=4)
