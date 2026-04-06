# Enterprise Software Development 2025 - 2026 Assignment 1  .md

## Install and run

#### Preparation
Please decompress and extract from the zip file submitted, or by cloning from
GitHub.com by the following command ( if git is installed ) :-
git clone https://github.com/cochan2526/esdassg1.git
Application is stored in the directory "esdassg1"
By changing the directory into the "esdassg1" , the file "manage.py" can be found.

#### Create the environment
Create virtual environment by the following command :-
python3 -m venv .venv
( or python -m venv .venv )

#### Activate the environment
Activate the virtual environment by :-
source .venv/bin/activate
( or .venv\Scripts\activate.bat in Windows )

#### Install packages required
Install packages ( Django ) required
pip install -r requirements.txt

#### Start the application
Application can now be run by the following command :-
python manage.py runserver [any port number free for use]

#### Accessing the application
And now the program is now can be accessed by browser at the address "localhost[:port number entered]"

## Deployment
Application is also deployed to pythonanywhere.com at the following address:
"https://nitorishuuichi.pythonanywhere.com/"

## Usage of the application
When the website is accessed, user can search the fare between stations by selecting
the departing and destination station and click on "Get fare" button.  Users can then
click on the name of station to get the list of barrier free facilities available in
the station.

User can also register by simply provide a username and password, after register,
user can access the account page and select their preferred departing and destination
stations, and also the barrier free facilities in concern, by doing so, everytime
they login, their prefered stations will be automatically selected in homepage,
and the barrier free facilities in concern will be automatically filtered out and
displayed if it is available in the departing and destination stations of the 
journey user selected, in the fare displaying page, without the need of entering
the barrier free facilities listing page.

### Correctness of data
As the data is real and updated, the result can be also check in the websit of the
MTR as the following address.

#### MTR Fare enquiry page
"https://www.mtr.com.hk/en/customer/tickets/index.php"

#### MTR Barrier free facilities
"https://www.mtr.com.hk/en/customer/services/free_search.php?query_type=search&station=1&disable_search=#searchResult"

## Reference
## user authentication System using django
On 2026-03-22
referencing https://www.geeksforgeeks.org/python/user-authentication-system-using-django/
logout referencing https://docs.djangoproject.com/en/6.0/topics/auth/default/

## for use of "import *"
Referencing "https://stackoverflow.com/a/6761908"

## get checkbox values in django application as a list
Referencing "https://stackoverflow.com/questions/48735726/how-to-get-checkbox-values-in-django-application"

### helper.py
Sub functions used in views.py
In order to make views.py more clear and easy to read.

## Data used in this project is obtained from data.gov.hk,
## provided by MTR Corporation Limited of Hong Kong

Open data is download from "http://https://data.gov.hk/en-data/dataset/mtr-data-routes-fares-barrier-free-facilities/" , 
data used are "MTR Lines (except Light Rail) & Stations" , "Barrier Free Access 
Category" , "Barrier Free Access in MTR stations" and "MTR Lines (except 
Airport Express & Light Rail) Fares".

MTR is the subway system in Hong Kong which is started to be built from the
1970s.

As there is 96 stations in the data and thus the total number of fare record 
is square of 96 = 9,216, in otder to make the size of the data small enough and
keep the application simple, I trimmed down to the earliest stage of the system 
which is the first 2 lines ( Kwun Tong Line and Tsuen Wan Line ) , 25 stations
in total, with station number ranged from 1 to 25. I further remove records of
same stations and half of the records as the fare is the same for opposite
direction, and final number of records is down to 25*24/2 = 300.

For the barrier free facilities dataset, in order to trim down the size of 
data, facilities that are not available is removed.


Below is extract of T & C of using data from data.gov.hk

On 2026-04-04

https://data.gov.hk/en/terms-and-conditions

Use of Data on DATA.GOV.HK

You are allowed to browse, download, distribute, reproduce, hyperlink to, and print the Data for both commercial and non-commercial purposes on a free-of-charge basis on condition that:-

    you shall comply with the Terms of Use;
    you shall identify clearly the source of the Data and acknowledge the Government and the Relevant Organisations’ ownership of the intellectual property rights in the Data and in all copies thereof including but not limited to paper copies, digital copies and copies placed on other websites;
    you shall indemnify the Government and the Relevant Organisations against any allegations or claims of infringement of the rights of any person and all costs, losses, damages and liabilities incurred by the Government and the Relevant Organisations, which in any case arise directly or indirectly in relation to your use, reproduction and/or distribution of the Data;
    you shall also give proper attribution to the Government, the Relevant Organisations and DATA.GOV.HK.

In paragraph 3, “commercial purposes” includes without limitation the following:

    an offer to supply goods, services, facilities, land or an interest in land;
    an offer to provide a business opportunity or an investment opportunity;
    an advertisement or promotion of goods, services, facilities, land or an interest in land;
    an advertisement or promotion of a business opportunity or an investment opportunity;
    an advertisement or promotion of a supplier, or a prospective supplier, of goods, services, facilities, land or an interest in land; and
    an advertisement or promotion of a provider, or a prospective provider, of a business opportunity or an investment opportunity,

in the course of or in the furtherance of any business.




