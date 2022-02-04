# finance_tools

End product will be a Bokeh-server hosted app, running within a Docker container to allow reproducible deployment on foreign machines.

How to use:
## Running the app in a docker container
- Ensure you have Docker installed on your local machine
- Clone this repository to <clone_path>
- Open a powershell prompt and run the following commands:

<span style="font-family: 'courier modern';">
cd <clone_path>
docker build mortgage-assistant
</span>

- This will take a few minutes. Once the container is ready, call
docker run -p 5006:5006 mortgage-assistant
- Navigate to localhost:5006/app in your browser to use the application.

## To do:
- Interest calculator
- Interest rate forecasting outside of fixed term
- dockerfile

## Notes:
Interest rate information obtained from publicly available datasets curated by the Bank of England
https://www.bankofengland.co.uk/boeapps/database/fromshowcolumns.asp?Travel=NIxSTxTIxSUx&FromSeries=1&ToSeries=50&DAT=ALL&FNY=&CSVF=TT&html.x=146&html.y=37&C=EOF&C=NB2&C=EP6&Filter=N
