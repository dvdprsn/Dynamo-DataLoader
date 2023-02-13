# CIS\*4010 Assignment 2 (DynamoDB)

## Running Instructions

** aws.conf file with default profile is required **
** Creating and loading initial table data **

1. execute `python3 create_load.py`

## Module Structure

## How to use the modules

## How to generate reports

## How to make edits to the table

### Adding New Data

#### Through add_data folder

- This will scan all csv files in the add_data folder and so long as the files within have the correct naming conventions all data within the file will be added to the table in the correct locations.
  This will notify the user if one of these files contains an attribute that already exists in the table and will prevent data overwrites.
- csv files within this folder are expected to have the SAME name and format as the provided files. If the user wishes to add more population data for Canada they would follow these steps:

1. Create a new file called shortlist_curpop.csv in the add_data directory
2. Add the headers `Country,<currency>,<years>,...` -> Country is the only required header and there can be any number of year headers
3. Populate the table rows with data you wish to add for example: `United States,203123012` assuming the file has the following headers `Country,<year>`
4. Execute the add data program and follow the prompts to add data from folder.
5. Further, steps 1,2 could be ignored by copying the exists curpop csv from the data directory and adding a new row

#### Through prompts

## Limitations

- Creating single country reports is limited to countries that have sufficient data to create the report. This must include ...
