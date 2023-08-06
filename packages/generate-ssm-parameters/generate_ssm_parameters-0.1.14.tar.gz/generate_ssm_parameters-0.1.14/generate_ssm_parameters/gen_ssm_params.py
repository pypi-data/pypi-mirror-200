import boto3
import botocore
import click
import pandas as pd
import os
from tqdm import tqdm


# enter a profile to connect a session for scripts run locally
def start_session(reg, pro):
    started = False
    # profile selection input loop, lets you type in your aws credentials profile and starts a session.
    print(f"Starting AWS session in {reg}...")
    while not started:
        if not os.getenv('AWS_DEFAULT_PROFILE'):
            print('No default profile found...')
            try:
                print("Trying environment variables...")
                ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
                SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
                SESSION_TOKEN = os.getenv('AWS_SESSION_TOKEN')
                s = boto3.Session(
                    aws_access_key_id=ACCESS_KEY,
                    aws_secret_access_key=SECRET_KEY,
                    aws_session_token=SESSION_TOKEN,
                    region_name=reg
                )
                return s
            except botocore.exceptions.ClientError as error:
                print('Invalid profile: {}'.format(pro))
                raise error
        else:
            print(f'Trying profile {pro}...')
            try:
                s = boto3.Session(profile_name=pro, region_name=reg)
                if s:
                    return s
            except (botocore.exceptions.ClientError, botocore.exceptions) as error:
                print('Invalid profile: {}'.format(pro))
                raise error


def confirm(message):
    valid = False
    while not valid:
        choice = input(f"{message} Y/N:")
        if choice == 'y' or choice == 'Y':
            print('Y confirmed.')
            return True
        elif choice == 'n' or choice == 'N':
            print('N confirmed.')
            return False
        else:
            continue


@click.command()
@click.option('--region', default='us-east-1',
              help='AWS region where the parameter(s) will be created. Defaults to "us-east-1".')
@click.option('--profile', default='default',
              help='AWS profile to use for credential generation. Defaults to "default".')
@click.argument('csv')
def cli(region, profile, csv):
    session = start_session(region, profile)

    # check for csv file
    print(f"Loading {csv}...")

    path = os.getcwd()

    files = [f for f in os.listdir(path) if os.path.isfile(f)]
    if csv not in files:
        print(f'File {csv} not found in working directory. Exiting...')
        exit()

    try:
        df = pd.read_csv(csv)
        print(f'Input file {csv} loaded')
    except pd.errors as e:
        print(e)
        exit()

    name_list = []
    param_type_list = []
    value_list = []
    description_list = []

    # iterate over the rows in the input csv and populate the lists
    for index, row in df.iterrows():
        name_list.append(row.get('Name'))
        param_type_list.append(row.get('Type'))
        value_list.append(row.get('Value'))
        description_list.append(row.get('Description'))

    print(f'Loaded {len(name_list)} parameters')

    ssm_client = session.client('ssm')
    paginator = ssm_client.get_paginator('describe_parameters')
    try:
        response_iterator = paginator.paginate()
    except botocore.exceptions.ClientError as e:
        print(e)
        exit(1)

    existing_params = []
    duplicated_params = []

    for page in response_iterator:
        for param in page.get('Parameters'):
            existing_params.append(param.get('Name'))

    for param_name in name_list:
        if param_name in existing_params:
            duplicated_params.append(param_name)

    # check for duplicates and prompt user for overwrite choice
    overwrite_flag = False
    if duplicated_params:
        print('The following parameter names already exist in the target account:')
        for x in duplicated_params:
            print(f'\t- {x}')
        if confirm('Do you want to overwrite them?'):
            overwrite_flag = True

    failed_params = []
    successful_params = []
    error_codes = []
    print('Creating ssm parameters...')
    for x in tqdm(range(len(name_list))):
        try:
            response = ssm_client.put_parameter(
                Name=name_list[x],
                Description=description_list[x],
                Value=value_list[x],
                Type=param_type_list[x],
                Overwrite=overwrite_flag,
                # Tags=[
                #     {
                #         'Key': 'string',
                #         'Value': 'string'
                #     },
                # ],
            )
            successful_params.append(name_list[x])
        except botocore.exceptions.ClientError as e:
            print(e)
            failed_params.append(name_list[x])
            error_codes.append(e)

    if failed_params:
        print(f'{len(failed_params)} parameter(s) could not be created:')
        for x in range(len(failed_params)):
            print(f'\t- {failed_params[x]}: {error_codes[x]}')

    print('Parameter creation complete.')
    print(f'{len(successful_params)} parameter(s) were created.')
