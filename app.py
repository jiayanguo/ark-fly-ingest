import requests
from datetime import date, datetime
from pytz import timezone
import csv
import io
import boto3

ARKK_HOLDINGS="https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_INNOVATION_ETF_ARKK_HOLDINGS.csv"
ARKQ_HOLDINGS="https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_AUTONOMOUS_TECHNOLOGY_&_ROBOTICS_ETF_ARKQ_HOLDINGS.csv"
ARKW_HOLDINGS="https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_NEXT_GENERATION_INTERNET_ETF_ARKW_HOLDINGS.csv"
ARKG_HOLDINGS="https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_GENOMIC_REVOLUTION_MULTISECTOR_ETF_ARKG_HOLDINGS.csv"
ARKF_HOLDINGS="https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_FINTECH_INNOVATION_ETF_ARKF_HOLDINGS.csv"
PRNT_HOLDINGS="https://ark-funds.com/wp-content/fundsiteliterature/csv/THE_3D_PRINTING_ETF_PRNT_HOLDINGS.csv"
IZRL_HOLDINGS="https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_ISRAEL_INNOVATIVE_TECHNOLOGY_ETF_IZRL_HOLDINGS.csv"
ARKX_HOLDINGS="https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_SPACE_EXPLORATION_&_INNOVATION_ETF_ARKX_HOLDINGS.csv"

arkholding = {
    "arkk": ARKK_HOLDINGS,
    "arkq": ARKQ_HOLDINGS,
    "arkw": ARKW_HOLDINGS,
    "arkg": ARKG_HOLDINGS,
    "arkf": ARKF_HOLDINGS,
    "prnt": PRNT_HOLDINGS,
    "izrl": IZRL_HOLDINGS,
    "arkx": ARKX_HOLDINGS
}

OBJECT_KEY_PATTERN="holdings/{today}_{etf}_holdings.csv"
S3_BUCKET ="ark-fly"

# If the holding date is not today, return false
def get_etf_holdings(etf, date):
    response = requests.get(arkholding[etf])
    holding_date = get_holding_date(io.StringIO(response.text))
    if (holding_date == date):
        # fileName = today + "_" + etf + "_holdings.csv"
        # with open(fileName, 'wb') as temp_file: 
        #     temp_file.write(response.content)
        upload_to_s3(io.BytesIO(response.content), OBJECT_KEY_PATTERN.format(today=date, etf=etf))
        return True
    else:
        print("no need to ingest! holding_date {holding_date} today {today}".format(holding_date=holding_date, today=date))
        return False

def upload_to_s3(content, object_name):
    client = boto3.client('s3')
    try:
        response = client.upload_fileobj(content, S3_BUCKET, object_name)
    except Exception as error:
        raise Exception("faile to upload to s3! " + str(error))

def get_date():
    tz = timezone('EST')
    today = datetime.now(tz).strftime("%Y-%m-%d")
    return today

def main():
    today = get_date()
    for etf in arkholding:
        if not get_etf_holdings(etf, today):
            return

def get_holding_date(csv_bin):
    reader = csv.DictReader(csv_bin)
    for row in reader:
        if row["date"]:
            return datetime.strptime(row["date"], '%m/%d/%Y').strftime('%Y-%m-%d')

if __name__ == '__main__':
    main()

def lambda_handler(event, context):
    main()
    return {
        "status":200
    }