FROM python:3.11-slim

WORKDIR /adguard-vpn-helper

COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python3", "-m", "src.app"]