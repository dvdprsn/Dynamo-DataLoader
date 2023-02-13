# CIS\*4010 Assignment 2 (DynamoDB)

David Pearson

1050197

dpears04@uoguelph.ca

## Module Structure

### File Tree

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

- `add_data/` directory -> This contains the csv files for bulk appending NEW data to the tables. Included in the submission is two files to serve as an example for how this works and for format. This is explained further below
- Changes to input CSV files - The only change was adding the header to the un_shortlist.csv file

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

**Note** This section will outline how to run the 3 programs outlined in step 4 of the Assignment 2 description. As mentioned above, the 7 modules above were not designed to be directly interfaced with.

**aws.conf file with default profile is required**

### Creating and loading initial table data

1. execute `python3 create_load.py`

- This will create the two tables, `dpears04_NonEconomic` and `dpears04_Economic`
- It will also initialize the key values (country names) from the un_shortlist file
- Once the two tables have been created, assuming neither of the tables existed already, the program will populate the tables with data from the csv files in the `data/` directory
- The program will notify the user at each step of this process and it may take some time to populate the tables.
- If this program is ran again once the tables exist, it will not try to repopulate the tables

### Manipulating/Adding Data to existing tables

1. execute `python3 modify_data.py`

- This program will initiate an interactive terminal guide that steps the user through providing all the necessary info for the functions
- The user will have the option of loading from formatted csv files or from prompts
  **Loading from File** This is also covered in the How to Make Edits section below
- If the user selects `Load data from add_data folder` the program will try to add data from all CSV files located in that directory.
  Included in the submission are examples files for how the program expects the data to be formatted. **File Format** Generally speaking, the program expects the
  files to have the same names and headers as the original, provided csv files found in the `data/` folder.
- The user can also just select prompts and the program will step by step collect information to be added to the table - much more intuitive

**More information on table modifications is outlined below**

### Creating Reports

1. execute `python3 create_reports.py`

- This program will start an interactive command line tool to build the reports. It will ask the user for a couple pieces of information needed and then a PDF will be output to the project directory

## How to generate reports

## How to make edits to the table

**Execute `python3 modify_data.py` and follow the prompts**

- There's two options for adding new data to the tables

1. Through prompts (Easiest and recommended)
2. Through csv files in `add_data/` directory

The prompts will only allow adding a single data point at a time, so adding multiple years of population data would require multiple executions. The csv option works well for bulk loading new data, but requires a special format described below.

Generally, this special format is identical to the files in `data/` but modified with any data you wish added

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

- **tl;dr:** Create a copy of the csv from the data directory that includes the data you would like to add in the add_data directory. Either add the new data to an existing row for the country it should be added to or, create a new row at the bottom for a new country.
- Upon telling the `modify_data.py` program to use the add_data directory you will likely recieve many errors indicating the data already exists - this can be avoided by removing the rows with existing data. Despite this, the new data will still be added to the table.

- Notably, this is not nearly as intuitive as following the prompts but it allows bulk adding information to the table if for example the user wished to add a new country

#### Through prompts (Easiest)

- The program will prompt the user for various info to help build the data to be added.
- If the user tries to add data that already exists in the table it will notify the user this is not possible.
- If the user attempts to add a country that does not exist it will create that country in the indicated table.
- The prompts only allow adding a single data point at a time, to add multiple, rerun this program
- The program will ask the following

1. (1) Add or (2) delete data -> For these prompts enter 1 to add data
2. Load data from (1) Prompts (2) add_data folder -> enter 1
3. Select table (1) Non Economic (2) Economic -> enter 1 or 2
4. Enter the country name or ISO3 value
5. Enter attribute name -> This is a value such as the year for GDPPC or Pop depending on table, or Languages, Currency etc. (The heading value)
6. Enter the data point to be added under the attribute value specified above

### Deleting Data

- This is handled through the `modify_data.py` program as well and it will prompt the user for deletion options.
- The following prompts will appear

1. (1) Add or (2) Delete data -> Enter 2
2. (1) Economic or (2) Non Economic -> Enter 1 or 2 depending on the table
3. Enter the country name or ISO3 the data is stored at
4. You are now given the option to delete the entire country or just the single data point in the country -> select 1 or 2
5. For single data point -> Enter attribute name where the data contained within should be deleted. For example 2019 for GDPPC or pop or languages, currency etc

## Limitations/Assumptions

- Creating single country reports is limited to countries that have sufficient data to create the report. Sufficient means: Name, Official Name, Area, Languages, currency, and capital. The tables will be empty if there is no Population or Economic data.
- Limited input validation for the interactive programs (1) or (2) selections. If it doesnt get a value it expects it will default to one of the options.
- Limited output for success or failure on modify the table functions.
- Blank rows will still be included in the GDPPC for all countries table in the global report. I have elected to handle it this way as not including am empty row
  tells the exact same information as it being there, that is, no data exists for this timeframe. But, for an analyst it enables seeing at a glance that for a given decade
  which countries do not have data.
- If in a given decade no country has a data point for a single year, this year is not included in the table. This means if a data point is added for Canada in 2020, this would create a new decade table,
  but would only have a 2020 column.
- The interactive programs are not looped, meaning to continue changing data in the table it should be rerun
- It is assumed an file with the name `aws.conf` will be provided by the grader, this file should have the same structure from assignment 1, just renamed since we were not working with S3 anymore.
- The reports will be output in a PDF format using the reportlab library, this is included in the requirements.txt file and should be downloaded ahead of execution for the reports
- Tested on Mac and WSL Debian - reportlab failed to install on the VirtualBox SoCS image with a string of system errors that couldnt be resolved.
- The program to modify data and build the reports assumes that the tables exist and are populated with the provided data and will through errors if the tables with expected names do no exists. In other words, `python3 create_load.py` should be run first.
- Tables created by `create_load.py` will have the following names `dpears04_Economic` and `dpears04_NonEconomic` - for the size of the data it was easier just to have two tables.
- These tables will use 'CountryName' as the primary key for each data entry. This can be challenging for countries with more complex names, as such the interactive programs will assume three letter inputs for the country is the ISO3 value and will be accepted.
