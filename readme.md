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
