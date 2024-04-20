CSV Query Server

A simple single web page portal for querying on multiple CSV files and geting the required output.

Requirements:
-python3 and above
-Flask

Setup

-Creating virtual environment
Run the following commands to create a virtual environment

python -m venv venvNameHere

To start the virtual environment run:
venvNameHere\Scripts\activate

To install all the dependencies run:
pip install -r requirements.txt

To start the application run:
python csv_server.py <csv_file1> <csv_file2> ... <csv_filen>

Note: If you dont specify any csv files, by default 'ADM.csv', 'AFA.csv' and 'GWL.csv' will be imported.

Server will launch on port http://127.0.0.1:5000/


