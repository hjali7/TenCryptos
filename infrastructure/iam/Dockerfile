FROM python:3.11-slim

WORKDIR /app

COPY infrastructure/iam/requirements.txt ./requirements.txt
COPY infrastructure/iam/setup_iam.py .
COPY infrastructure/iam/setup_cw_role.py .
COPY scripts/bootstrap_iam.sh ./bootstrap_iam.sh

RUN chmod +x bootstrap_iam.sh && \
    pip install --no-cache-dir -r requirements.txt

CMD ["sh","./bootstrap_iam.sh"]