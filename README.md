# finance_tools
This application is designed to help users compare performance of various financial products. Currently, it's geared towards mortgages, but in future I plan to extent it to investment strategies too. The objective is to help users better understand the long term financial impact of decisions such as:
- Should I overpay my mortgage, invest, or strike a balance?
- Once my fixed-rate deal expires, how quickly am I likely to repay under the expected variable rate?

From a technical perspective, it's been an exercise in creating reusable, reproducible web-apps, and gaining practice with Docker. 

How to use:
## Running the app in a docker container
1. Ensure you have Docker installed on your local machine
2. Clone this repository to <clone_path>
3. Open a powershell prompt and run the following commands:

cd <clone_path>

docker build mortgage-assistant

4. This will take a few minutes. Once the container is ready, call

docker run -p 5006:5006 mortgage-assistant

5. Finally, navigate to localhost:5006/app in your browser to use the application.

## To do:
- Interest calculator
- Interest rate forecasting outside of fixed term

## Notes:
Interest rate information obtained from publicly available datasets curated by the Bank of England
https://www.bankofengland.co.uk/boeapps/database/fromshowcolumns.asp?Travel=NIxSTxTIxSUx&FromSeries=1&ToSeries=50&DAT=ALL&FNY=&CSVF=TT&html.x=146&html.y=37&C=EOF&C=NB2&C=EP6&Filter=N
