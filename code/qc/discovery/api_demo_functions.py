# -*- coding: utf-8 -*-
import os
import errno

from dotenv import load_dotenv

from ..api.wrapper import QCApi

PID = 1685011                               # Example project ID
BID = '3dcd51433200e1d3919f021dae7376bf'    # Example backtest ID

dotenv_path = os.path.join(os.getcwd(), '.env')
load_dotenv(dotenv_path)
client = QCApi(userId=os.environ['QC_USER_ID'], token=os.environ['QC_ACCESS_TOKEN'])


def print_projects_verbose():
    if client.connected():
        print('Successfully connected to Quant Connect!')
        print('Listing details of all projects for user: \n')
        projects_response = client.list_projects()

        # MAYBE THIS IS SOMETHING WE CAN USE TO CHECK FOR HTTP REQUEST SUCCESS STATUS
        print('SUCCESS: {}\n'.format(projects_response['success']))

        # Example project details:
        print('PROJECTS\n')

        # print every key and value in list of dictionaries
        for project in projects_response['projects']:
            print('===================================================')
            for proj_dict_key in project:
                if proj_dict_key == 'collaborators':
                    print('collaborators: ')
                    for collaborator in project['collaborators']:
                        for collaborator_dict_key in collaborator:
                            print('  |-- {}: {}'.format(collaborator_dict_key, collaborator[collaborator_dict_key]))
                        print('--------------------------')
                elif proj_dict_key == 'liveResults':
                    print('liveResults: ')
                    for live_result_dict_key in project['liveResults']:
                        print('    |-- {}: {}'.format(live_result_dict_key, project['liveResults'][live_result_dict_key]))
                else:
                    print('{}: {}'.format(proj_dict_key, project[proj_dict_key]))

        # THIS LOOKS LIKE RANDOM QC BACKEND STUFF
        # print('VERSION')
        # for version in projects_response['versions']:
        #     print(version)

    else:
        print('Error connecting to Quant Connect.\n'
              'Check your user credentials in .env and ensure\n'
              'you are connected to the internet')


def print_projects():
    if client.connected():
        print('Successfully connected to Quant Connect!')
        print('Listing details of all projects for user: \n')
        projects_response = client.list_projects()

        # Example project details:
        print('PROJECTS')
        # print every key and value in list of dictionaries
        for project in projects_response['projects']:
            print('  |-- {} | {}'.format(project['projectId'], project['name']))
    else:
        print('Error connecting to Quant Connect.\n'
              'Check your user credentials in .env and ensure\n'
              'you are connected to the internet')


def print_list_of_backtests_by_project():
    if client.connected():
        print('Successfully connected to Quant Connect!\n')
        print('Listing details of all backtests by project: ')
        projects_response = client.list_projects()
        if projects_response['success'] is not True:
            return None
        # Example project backtest details:
        print('PROJECTS')
        for project in projects_response['projects']:
            print('===================================================')
            print('projectId: {}'.format(project['projectId']))
            print('name: {}'.format(project['name']))
            print('---------------------------------------------------')
            backtests_response = client.list_backtests(projectId=project['projectId'])
            if backtests_response['success'] is not True:
                return None
            print('This project has {} backtests available to query.'.format(len(backtests_response['backtests'])))
            for backtest in backtests_response['backtests']:
                for backtest_dict_key in backtest:
                    print('    |-- {}: {}'.format(backtest_dict_key, backtest[backtest_dict_key]))
                print('---------------------------------------------------')
    else:
        print('Error connecting to Quant Connect.\n'
              'Check your user credentials in .env and ensure\n'
              'you are connected to the internet')


def download_example_backtest_report(project_id=PID, backtest_id=BID):
    if client.connected():
        print('Successfully connected to Quant Connect!\n')
        print('Downloading report for a hardcoded backtest ID...')
        backtest_response = client.read_backtest_report(projectId=project_id, backtestId=backtest_id)
        if not backtest_response['success']:
            return None
        filename = os.path.join(os.getcwd(), '{}.html'.format(backtest_id))
        with open(filename, 'w') as out_file:
            out_file.write(backtest_response['report'])
    else:
        print('Error connecting to Quant Connect.\n'
              'Check your user credentials in .env and ensure\n'
              'you are connected to the internet')


def print_project_files_verbose(project_id=PID):
    if client.connected():
        print('Successfully connected to Quant Connect!')
        print('Loading list of project files for project ID...')
        files_response = client.read_project_files(projectId=project_id)
        if not files_response['success']:
            return None
        for file_data in files_response['files']:
            print('===================================================')
            print('---------------- < {} > ---------------'.format(file_data['name']))
            print('===================================================')
            print(' |- {}'.format(file_data['name']))
            for file_dict_key in file_data:
                if file_dict_key == 'content':
                    print('file content: ')
                    print('---------------- < CODE BEGINS > ------------------')
                    print('{}'.format(file_data[file_dict_key]))
                    print('----------------- < CODE ENDS > -------------------')
                elif file_dict_key != 'name':
                    print('  |-- {}: {}'.format(file_dict_key, file_data[file_dict_key]))
            print('===================================================\n')
    else:
        print('Error connecting to Quant Connect.\n'
              'Check your user credentials in .env and ensure\n'
              'you are connected to the internet')


def print_project_files(project_id=PID):
    if client.connected():
        print('Successfully connected to Quant Connect!')
        print('Loading list of project files for project ID {}'.format(project_id))
        files_response = client.read_project_files(projectId=project_id)
        if not files_response['success']:
            return None
        print('FILES:')
        for file_data in files_response['files']:
            print(' |- {}'.format(file_data['name']))
    else:
        print('Error connecting to Quant Connect.\n'
              'Check your user credentials in .env and ensure\n'
              'you are connected to the internet')


def download_project_files(project_id=PID):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    if client.connected():
        print('Successfully connected to Quant Connect!')
        print('Downloading files for project ID...')
        files_response = client.read_project_files(projectId=project_id)
        if not files_response['success']:
            return None
        for file_data in files_response['files']:
            python_filename = '{}-{}'.format(project_id, file_data['name'])
            filename = os.path.join(dir_path, 'downloads/{}'.format(python_filename))
            if not os.path.exists(os.path.dirname(filename)):
                try:
                    os.makedirs(os.path.dirname(filename))
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            with open(filename, 'w') as f:
                f.write(python_filename)
            print(' |- {}'.format(file_data['name']))
    else:
        print('Error connecting to Quant Connect.\n'
              'Check your user credentials in .env and ensure\n'
              'you are connected to the internet')
