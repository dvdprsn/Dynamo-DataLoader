# DynamoDB Data Loader

David Pearson

## File Tree

```
.
├── add_data
│   ├── shortlist_area.csv
│   └── un_shortlist.csv
├── aws.conf
├── create_load.py
├── create_reports.py
├── data
│   ├── shortlist_area.csv
│   ├── shortlist_capitals.csv
│   ├── shortlist_curpop.csv
│   ├── shortlist_gdppc.csv
│   ├── shortlist_languages.csv
│   └── un_shortlist.csv
├── modify_data.py
├── modules
│   ├── aws_client.py
│   ├── loaddata.py
│   ├── reports.py
│   └── table.py
├── readme.md
└── requirements.txt
```

- Python version 3.9.6
- Requires reportlab for PDF report output
- Requires Boto3
- See requirements.txt
- Developed and tested on OSX and WSL Debian

## Module Structure

- All of the modules are contained within the `modules/` directory
- Modules were broken up into various files to keep everything more organized and usable
  - `aws_client.py` -> Contains code required init the aws connection to DynamoDB
  - `loaddata.py` -> Contains code for manipulating the data including, loading, adding, deleting as well as the interactive programs
  - `reports.py` -> Contains code for generating the two report types along with helper functions to parse the returned data
  - `table.py` -> Contains code for creating and deleting the tables

### Changes to CSV Input files

- un_shortlist.csv has an added header row as this was originally missing

## How to use the modules

**For each entry below, the required import statement is listed, how to call the function, and any other relevant information such as arguments or return values to expect**

**`aws.conf` is required in the project root with the authentication keys -> same file and structure as A1 just renamed since we are not working with S3 anymore**

- In all instances where an interactive program asks from an attribute name this refers to the column name in the given table
  - Examples: 1974, Currency, Area, Languages, ISO3, 2010
  - Years will contain the values for either population of GDPPC for that given year for the respective tables
  - Refer to the DynamoDB 'explore items' feature to see more options but it is generally straightforward and no changes have been made from the header values in the original CSV inputs

1. Create a table
   - `from modules import aws_client, table`
   - `table.create(client, dict_config)`
     - Create the client `client = aws_client.create_client()`
     - `dict_config` is the params dict from the boto3 docs. An example of this can be found in `modules/table.py` in the function `create_noneconomic()`
2. Delete a table
   - `from modules import aws_client, table`
   - `table.delete(client, table_name)`
     - Create the client `client = aws_client.create_client()`
     - `table_name` is a string
3. Load records into the table
   - `from modules import aws_client, loaddata`
   - `loaddata.load(client, dir)`
     - Create the client `client = aws_client.create_client()`
     - `dir` is a string for the directory containing all the csv files to load - should be `data`
     - This function will scan all csv files in the `data` directory that match the names as they were given, calling a different function for each file to handle loading the various data formats
4. Add individual record
   - `from modules import aws_client, loaddata`
   - `loaddata.load_single(client)`
     - Create the client `client = aws_client.create_client()`
     - This function will start an interactive program asking the user to enter the data to be loaded to the table
5. Delete Individual Record
   - `from modules import aws_client, loaddata`
   - `loaddata.delete_data(client)`
     - Create the client `client = aws_client.create_client()`
     - Starts an interactive program finding which data to delete from the table
     - Allows the user to choose between deleting an individual attribute from a country or the entire country
6. Dump data from table
   - `from modules import aws_client, loaddata`
   - `loaddata.dump_all(client, table)`
     - Create the client `client = aws_client.create_client()`
     - Table is the table name
     - Will return the raw data from the boto3 scan() function for a given table
7. Query Module
   - `from modules import aws_client, table`
   - `table.query_data(client, table_name, key)` OR `table.query_from_iso3(client, key)`
     - Create the client `client = aws_client.create_client()`
     - `key` is the country name or ISO3 value depending on which function above is used
     - `query_data()` will return the dictionary for all data at the given key
     - `query_from_iso3()` will return the country name

## Create and load provided data to the tables

1. execute `python3 create_load.py` (Assuming tables have not already been created and populated)
   - This will create the two tables, `dpears04_NonEconomic` and `dpears04_Economic`
   - It will also initialize the key values (country names) from the un_shortlist file
   - Once the two tables have been created, assuming neither of the tables existed already, the program will populate the tables with data from the csv files in the `data/` directory
   - The program will notify the user at each step of this process and it may take some time to populate the tables.
   - If this program is ran again once the tables exist, it will not try to repopulate the tables

## How to generate reports

1. execute `python3 create_reports.py`
   - This will start an interative program walking the user through a series of questions necessary for building a report
   - This interactive program will expect valid inputs for what is required
   - Enter 1 for Global reports or enter 2 for a country report
   - If global reports is selected it will then ask for a year
   - If country report is selected it will ask for country name or ISO3

### About Global Reports

- The countries ranked lists will only include countries that have a valid population entry for the given year
- The GDPPC section will include empty rows for countries with no data for the given decade
  - This was done as it provides more information about what data is currently contained in the tables over just omitting those entries entirely.
- If there is no data for ALL countries in a given year within a decade, that year will not be included in the table

### About Country Reports

- If a new country is added and does not contain enough information to generate a report the program will throw an error indicating what information might be missing

## How to make edits to the DB tables

### Adding new data

- Excute `python3 modify_data.py`
- This will launch an interactive program with two options for loading new data
- This interactive program will expect valid inputs for what is required
- If the attribute name already exists in the table this program will NOT allow overwrites, instead you must delete then add the modified data - done per slack discussion

1. Prompts (Best)

   - The prompts will walk the user through a series of questions to collect the data to be added
   - For the country name prompt assuming the country has a valid ISO3 value in the Non-Economic table - ISO3 can be used instead of the entire country name (saves typing for the longer names)
   - Valid selections are expected - if a value is entered that is not one of the options it will chose a default or throw an error
   - This program will not loop, for adding multiple data entries rerun this program or see the files section below for bulk adding new data.

2. Files (Cool option for bulk loading)

   - This will scan the `add_data/` directory for csv files of the same name and structure of the ones provided (now found in the `data/` folder)
   - This program is best for bulk loading new data in the same way the provided data is bulk loaded when the tables are created.
   - Within the `add_data/` folder sample files are provided for adding 'the United States' to the tables.
     - The `add_data/shortlist_area.csv` files contains a row attempting to overwrite data that already exists in the tables, this is done to demonstrate the error handling for data overwrites.
   - This is the only functionality the `add_data` folder is used for and if not adding from files can be safely ignored.
   - If the csvs have an unrecognized name or mismatched headers within, data may not be added or unexpected behaviour may occur - prompts are the safest method for adding data.

## Deleting data from the table

- Execute `python3 modify_data.py`
- This will start an interactive program
- The user will have the option of deleting an entire country from the table and all its contained data or an individual attribute contained within the country
- Country name or ISO3 can be used for convience
- This program will expect valid inputs

## Limitations and Assumptions

- Limited output for success or failure on modify the table functions - Couldnt find a clean way to do this with boto3 return values.
- The interactive programs are not looped, meaning to continue changing data in the table it should be rerun
- It is assumed an file with the name `aws.conf` will be provided by the grader, this file should have the same structure from assignment 1, just renamed since we were not working with S3 anymore.
- The reports will be output in a PDF format using the reportlab library, this is included in the requirements.txt file and should be downloaded ahead of execution for the reports
- The program to modify data and build the reports assumes that the tables exist and are populated with the provided data and will through errors if the tables with expected names do no exists. In other words, `python3 create_load.py` should be run first.
- Tables created by `create_load.py` will have the following names `dpears04_Economic` and `dpears04_NonEconomic` - for the size of the data it was easier just to have two tables.
- These tables will use 'CountryName' as the primary key for each data entry. This can be challenging for countries with more complex names, as such the interactive programs will assume three letter inputs for the country is the ISO3 value and will be accepted.
- None of the three programs interface with the delete tables module, from an inclass question and outline this was not required - Refer to the 'how to use the modules' section for information on creating your own program that uses these functions.
