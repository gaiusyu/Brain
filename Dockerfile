FROM python:3.7
WORKDIR /
 
ADD . .
 
RUN pip install -r requirements.txt

CMD ["python","/Code/runBrain.py"]
 
