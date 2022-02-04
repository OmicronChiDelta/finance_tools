# finance_tools

End product will be a Bokeh-server hosted app, running within a Docker container to allow reproducible deployment on foreign machines.

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
- dockerfile

## Notes:
Interest rate information obtained from publicly available datasets curated by the Bank of England
https://www.bankofengland.co.uk/boeapps/database/fromshowcolumns.asp?Travel=NIxSTxTIxSUx&FromSeries=1&ToSeries=50&DAT=ALL&FNY=&CSVF=TT&html.x=146&html.y=37&C=EOF&C=NB2&C=EP6&Filter=N
