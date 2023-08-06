import os
from dotenv import load_dotenv
import requests
import click
import sys
import json
import pathlib
from datetime import datetime, date
import re
import logging
import base64
from time import sleep

load_dotenv()

vams_backend = os.getenv("VAMS_BACKEND")
credentials_path = pathlib.Path(__file__).parent.resolve()

class LoginParamsError(Exception):
    """Exception raised for errors in the input salary.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Input params error"):
        self.message = message
        super().__init__(self.message)


def get_current_time():
    now = datetime.now()

    dt_string = now.strftime("%Y-%m-%dT%H:%M")

    print("date and time =", dt_string)
    return dt_string


def authenticate(username, password):
    try:        
        credentials = read_credentials()

        username = username
        password = password

        is_valid = validate_params(username, password)
        headers={'tokens': json.dumps(credentials)}

        if(is_valid):
            res = requests.post(f"{vams_backend}/login", data={"username":username, "password":password}, headers=headers)
            if(res.status_code >= 400):
                print(res.json())
            elif("userStatus" in res.json() and res.json()["userStatus"] == "FORCE_CHANGE_PASSWORD"):
                change_password(username)
                return 
            else:
                json_object = json.dumps(res.json(), indent=4)
                write_credentials(json_object)
                print('You have successfully logged in')
                return 
    except Exception as e:
        print('Fail')
        print("Error ", e)
        return e


def validate_params(username, password):
    if(username == None or len(username.strip()) == 0):
        raise LoginParamsError("Username is empty")
    
    if(password == None or len(password.strip()) == 0):
        raise LoginParamsError("Password is empty")

    if(len(username) < 4):
        raise LoginParamsError("Username is too short")
    
    if(len(password) < 8):
        raise LoginParamsError("Password is too short")

    return True

def change_password(username):
    print("You need change password. Please, enter new password")
    new_password = sys.stdin.readline().strip()
    username = username
    res = requests.post(f"{vams_backend}/change_password", data={"username": username, "new_password":new_password})

    if(res.json()['result'] == 'ok'):
        print('Now you can login with new password')
    
    return

def read_credentials():
    try: 
        if(os.path.exists(f'{credentials_path}/.credentials')):
            with open(f'{credentials_path}/.credentials', 'r') as openfile:
                credentials = json.load(openfile)    
                return credentials
    except Exception as e:
        print("Error ", e)


def write_credentials(credentials):
    try:
        with open(f"{credentials_path}/.credentials", "w") as outfile:
            outfile.write(credentials)
    except Exception as e:
        print("Error ", e)

def download_data(count, tag, start_time, end_time, batch, output, printt):

    if printt == 'True':
        printt = True

            
    if(batch == None):
        start_time = "2022-11-01T00:00"
        end_time = get_current_time()

    form = re.compile('\d{4}-\d{2}-\d{2}T\d{2}:\d{2}')


    logs_file = ''

    if output:
        if not os.path.exists(os.path.join(output, f'test-logs.txt')):
            logs_file = open(os.path.join(output, f'test-logs.txt'), 'w')
        else:
            logs_file = open(os.path.join(output, f'test-logs.txt'), 'a')
    else:
        if not os.path.exists(os.path.join(os.getcwd(), f'test-logs.txt')):
            logs_file = open(os.path.join(os.getcwd(), f'test-logs.txt'), 'w')
        else:
            logs_file = open(os.path.join(os.getcwd(), f'test-logs.txt'), 'a')


    tokens = json.dumps(read_credentials())

    header = {'tokens':f'{tokens}'}

    url = f'{vams_backend}/api/download_data?tag={tag}&start_time={start_time}&end_time={end_time}&count={count}&batch={batch}'

    logs_file.write(f'Making request to {url}\n')

    response = requests.request(method="GET", url=url, headers=header)

    logs_file.write('Auth succeed\n')

    if(response.status_code == 401):
        print('Auth failed, try login')
        return

    res = response.json()

    print(res) if printt else None
    logs_file.write(f"keys: {res['keys']}\n")
    keys_len = len(res['keys'])

    print(keys_len) if printt else None
    logs_file.write(f'Total keys {keys_len}\n')

    key_url = f'{vams_backend}/api/download_data?'

    for key in res['keys']:
    
        new_url = key_url + f"key={key}"

        logs_file.write(f"Making request to {new_url}\n")

        response = requests.request(method="GET", url=new_url, headers=header)

        logs_file.write(f'Request succed\n')

        print(f'working on {key}') if printt else None
        logs_file.write(f'Working on {key}\n')

        try:
            json_object = json.loads(response.json())

        except Exception as e:
            print(e) if printt else None
            logs_file.write(f'no annotated sessions left or server error, status code is {response.status_code}\n')
            logs_file.write(f'Error: {e}\n')
            logging.warning(f'no annotated sessions left or server error, status code is {response.status_code}') if printt else None
            continue

        logs_file.write("Initing directory\n")

        if not output:
            main_file = os.getcwd().replace('\\', '/')
        else:
            if os.path.isdir(output):
                main_file = output
            else:
                os.makedirs(output)
                main_file = output
        
        ses_id = key.split('/')[-1]

        logs_file.write(f'Writing directory is {main_file}{ses_id}\n')

        for obj in json_object:
            prefix = obj['key']
            print(prefix)
            key = prefix.replace('\\', '/').split('/')[-1]

            if not os.path.isdir(os.path.join(main_file, key)):
                os.makedirs(os.path.join(main_file, key))
                os.chdir(os.path.join(main_file, key))
            else:
                os.chdir(os.path.join(main_file, key))
                #current_dir = os.getcwd().replace('\\', '/')

            number = 0

            try:

                for img in obj['frames']:
                    file = os.path.join(os.getcwd(), f"{key}__{number}.txt").replace('\\', '/')

                    if os.path.exists(f'{file.split(".")[0]}.png'):
                        logs_file.write(f"such file exist {file.split('.')[0]}.png, skipping\n")
                        print(f"such file exist {file.split('.')[0]}.png, skipping")
                        break
                        
                    open(file, 'w').write(img)

                    img_byte = base64.b64decode(img)

                    open(file, 'wb').write(img_byte)

                    f, ext = os.path.splitext(file)

                    os.rename(file, f + ".png")
                    logs_file.write(f'Wrote {f}.png\n')

                    number+=1

                if number != 0:
                    logging.info(f'there is passives for {prefix}') if printt else None
                    logs_file.write(f'there is passives for {prefix}\n')
            
            except:
                logs_file.write(f'no passives for {prefix}\n')
                logging.warning(f'no passives for {prefix}') if printt else None

            json_obj = json.dumps(obj['annotations'])

            with open(f'{key}.json', 'w') as out:
                out.write(json_obj)

            os.chdir(main_file)

            count-=1

            sleep(2)



@click.group(help="VAMS CLI")
def main():
    """vams cli"""

@main.command('ping', help='service health check')
def ping():
    res = requests.get(f"{vams_backend}/health-check")
    print(res.json())

@main.command('login', help='login to vams')
@click.option('-u', '--user', required=True, help='Username')
@click.option("-p", "--password", prompt=True, hide_input=True)
def login(user, password):
    authenticate(user, password)

@main.command('download', help='download annotated data')
@click.option('--count', default=0, help='Number of session to be downloaded(if 0 provided all sessions will be loaded)')
@click.option('--tag', default=None, help='Tag of session')
@click.option('--start_time', default=None, help='From which date start dowloading')
@click.option('--end_time', default=None, help='Till which date to load')
@click.option('--batch', default=None, help='batch name')
@click.option('--output', default=None, help='output file') #need create output folder before use, add autho create output folder
@click.option('--printt', default=False, help='want to see or not prints')
def download(count, tag, start_time, end_time, batch, output, printt):
    download_data(count, tag, start_time, end_time, batch, output, printt)
