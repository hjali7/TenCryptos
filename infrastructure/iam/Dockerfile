FROM python:3.11-slim

WORKDIR /app

COPY ./requirements.txt ./requirements.txt
COPY setup_iam.py .
COPY setup_cw_role.py .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "setup_iam.py"]