FROM python:3.9

#Copy required files
ADD ./app.py .
ADD ./utils_graphics.py .
ADD ./utils_maths.py .
ADD ./requirements.txt .

#Install required libraries
RUN pip install -r ./requirements.txt

#Bokeh server used 5006 by default
EXPOSE 5006

#Use bokeh to launch the app
CMD bokeh serve \
    --show \
    ./app.py