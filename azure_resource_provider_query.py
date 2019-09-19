import sys
import json
import requests
import logging
import msal
import csv

from argparse import ArgumentParser

# Fixed variables
scope = ['https://management.azure.com//.default']

# Reusable function to create a logging mechanism
def create_logger(logfile=None):

    # Create a logging handler that will write to stdout and optionally to a log file
    stdout_handler = logging.StreamHandler(sys.stdout)
    if logfile != None:
        file_handler = logging.FileHandler(filename=logfile)
        handlers = [file_handler, stdout_handler]
    else:
        handlers = [stdout_handler]

    # Configure logging mechanism
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers = handlers
    )

# Obtain access token using client credentials flow
def obtain_access_token(tenantname,scope,client_id, client_secret):
    logging.info("Attempting to obtain an access token...")
    result = None
    app = msal.ConfidentialClientApplication(
        client_id = client_id,
        client_credential = client_secret,
        authority='https://login.microsoftonline.com/' + tenantname
    )
    result = app.acquire_token_for_client(scope)

    if "access_token" in result:
        logging.info("Access token successfully acquired")
        return result['access_token']
    else:
        logging.error("Authentication failure")
        logging.error("Error was: %s",result['error'])
        logging.error("Error description was: %s",result['error_description'])
        logging.error("Error correlation_id was: %s",result['correlation_id'])
        raise Exception("Unable obtaining access token")

# Main function
def main():
    try:
        # Create logger
        create_logger()

        # Process parameters passed
        parser = ArgumentParser()
        parser.add_argument('--tenantname', type=str, help='Azure AD tenant name')
        parser.add_argument('--clientid', type=str, help='Client ID of application')
        parser.add_argument('--clientsecret', type=str, help='Client secret of application')
        parser.add_argument('--subscriptionid', type=str, help='Subscription ID to run policy assessment')
        parser.add_argument('--resourceprovider', type=str, help='Resource Provider namespace such as Microsoft.Web')
        parser.add_argument('--exportfile', type=str, help='Full path of the export file')
        args = parser.parse_args()

        # Obtain access token
        access_token = obtain_access_token(tenantname=args.tenantname,scope=scope,client_id=args.clientid,client_secret=args.clientsecret)
        
        # Start query
        logging.info('Querying for resource provider information...')
        headers = {'Content-Type':'application/json', \
        'Authorization':'Bearer {0}'.format(access_token)}
        params = {
            '$expand':'resourceTypes/aliases',
            'api-version':'2019-05-10'
        }
        endpoint = f"https://management.azure.com/subscriptions/{args.subscriptionid}/providers/{args.resourceprovider}"
        response = requests.get(url=endpoint,headers=headers,params=params,verify=False)
        data = json.loads(response.text)

        # Process response
        resourcealiases = []
        if response.status_code == 200:
            for resource in data['resourceTypes']:
                for alias in resource['aliases']:
                    resourcealias = {}
                    resourcealias['name'] = alias['name']
                    resourcealias['defaultPath'] = alias['defaultPath']
                    resourcealiases.append(resourcealias)

            # Create CSV export file
            csv_columns = ['name','defaultPath']
            with open(args.exportfile, 'w', newline='') as exportfile:
                writer = csv.DictWriter(exportfile, fieldnames=csv_columns)
                writer.writeheader()
                for data in resourcealiases:
                    writer.writerow(data)
        else:
            logging.error("Failed resource provider query")
            logging.error("Error was: %s",data['error']['code'])
            logging.error("Error description was: %s",data['error']['message'])
            raise Exception('Failed resource provider query')   
    except Exception:
        logging.error('Execution error',exc_info=True)

if __name__ == "__main__":
    main()
