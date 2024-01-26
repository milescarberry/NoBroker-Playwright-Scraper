FROM python:3.11.4

WORKDIR /nobroker-mumbai-rental-scrape-playwright

COPY . .

RUN pip install pytest-playwright

RUN playwright install

RUN pip install -r requirements_.txt

CMD ['python', './rental_scrape.py']