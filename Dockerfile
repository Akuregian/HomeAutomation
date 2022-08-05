FROM python:3

WORKDIR /home/HomeAutomation

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80

CMD ["python", "./run.py"]

