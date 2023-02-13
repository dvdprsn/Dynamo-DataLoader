# CIS\*4010 Assignment 2 (DynamoDB)

## Notes

## Running Instructions

**aws.conf file with default profile is required**
**Creating and loading initial table data**

1. execute `python3 create_load.py`

- This will create the two tables, `dpears04_NonEconomic` and `dpears04_Economic`
- It will also initialize the key values (country names) from the un_shortlist file
- Once the two tables have been created, assuming neither of the tables existed already, the program will populate the tables with data from the csv files in the `data/` directory
- The program will notify the user at each step of this process and it may take some time to populate the tables.

**Manipulating/Adding Data to existing tables**

1. execute `python3 modify_data.py`

- This program will initiate an interactive terminal guide that steps the user through providing all the necessary info for the functions
- The user will have the option of loading from formatted csv files or from prompts
  **Loading from File** This is also covered in the How to Make Edits section below
- If the user selects `Load data from add_data folder` the program will try to add data from all CSV files located in that directory.
  Included in the submission are examples files for how the program expects the data to be formatted. **File Format** Generally speaking, the program expects the
  files to have the same names and headers as the original, provided csv files found in the `data/` folder.
- The user can also just select prompts and the program will step by step collect information to be added to the table - much more intuitive

**Creating Reports**

1. execute `python3 create_reports.py`

- This program will start an interactive command line tool to build the reports. It will ask the user for a couple pieces of information needed and then a PDF will be output to the project directory

## Module Structure

- The main 3 functionalities we were tasked to implement have been divided into 3 seprate programs accordingly.
- The program `create_load.py` should be executed first as this will create the tables and load them with the provided csv data.
- The progam `modify_data.py` will start a command line interactive program to walk through adding/deleting both individual data entries and entire countries from the persepctive tables.
- Finally, `create_report.py` will also start a command line program to collect the necessary information to create one of either global for a set year or a single country report.

- The 7 individuals modules we were tasked with implementing are generally going to be located in the py files in the modules directory. There are 4 python files in that directory,

1. `aws_client.py` has the code to establish the connection with AWS
2. `loaddata.py` contains the code necessary to populate the tables as well as manipulating the data later on

- This file contains the modules to dump/display, add individual record, bulk load records, delete individual record

3. `reports.py` contains all the code required to generate the reports

- This file contains helper functions to grab data from the tables and organize it to make pdf creation easier.

3. `table.py` contains the code that actually creates and interfaces with the tables themselves

- This file contains the modules for creating tables, deleting tables, and two query functions for both country name and from ISO3.

**Locations for 7 required modules**

- Many of these functions are not designed to be directly interfaced with as I assumed was the intention. Since they are required however, below is file and location of the function and a shor description

1. Create a table
   - File: `modules/table.py`
   - Function: `create(client, dict_config)` line 8 -> client = AWS boto3 client, dict_config = params as outlined in the boto3 docs
     - This function will create a table based on the dict_config
   - Function: `create_nonecon(client, file)` line 24 -> client = AWS boto3 client, file = the un_shortlist csv to load country names as keys
2. Delete a table
   - File: `modules/table.py`
   - Function: `delete(client, table_name)` line 16
   - This will delete the table at the target table_name
3. Load Records into the table
   - File: `modules/loaddata.py`
   - Function: `load(client, dir)` line 121
   - This function will scan for all csv files in the `dir` directory and call a specific function for each file. Since data varied between all the files, a general function to handle this was my first approach but it became unreadable after a bit. Cleaner this way especially for the scale of data being added.
4. Add individual record
   - File: `modules/loaddata.py`
   - Functon: `load_single(client)` line 147
   - This function prompts the user for input from the terminal to collect the data that will be added to which table. Which then calls the following:
   - Function: `add_col(client, table_name, key, col_nam, col_val)` line 10
   - This function uses update_item from boto3 to check if the attribute does not exist and then adds the data.
5. Delete Individual record
   - File: `modules/loaddata.py`
   - Function: `delete_data(client)` line 229
   - This function prompts the user for input from terminal to find which item should be deleted. This function will then call the following:
   - Function: `delete_entry(client, table_name, item, country)` line 216 **or** `delete_country(client, country, table)` line 211
   - These functions will remove the provided value from the table.
6. Dump data from table
   - File: `modules/loaddata.py`
   - Function: `dump_all(client, table)` line 265
   - This function will return the raw data from the boto3 `scan()` function.
   - Not currently used in any of the main functionality although the scan() function is often used.
7. Query Module
   - File: `modules/table.py`
   - Function: `query_data(client, table_name, key)` line 82 **or** `query_from_iso3(client, key)` line 94
   - These function take in a key and the the boto3 `get()` function to get the data at the given key.
   - The from ISO3 function will use a scan and FilterExpression for ISO3 values equal to the key

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
5. Further, steps 1,2 could be ignored by copying the exists curpop csv from the data directory and adding a new row for the data the user wishs to add

- Similar steps can be followed for adding any other additional data so long as it is contained in the file with the same name
  it would have been if it was in the initial load from the `data/` folder.

- Notably, this is not nearly as intuitive as following the prompts but it allows bulk adding information to the table if for example the user wished to add a new country

#### Through prompts

## Limitations

- Creating single country reports is limited to countries that have sufficient data to create the report. This must include ...
