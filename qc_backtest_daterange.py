# -*- coding: utf-8 -*-
import argparse
import datetime as dt
import os
import time
import urllib.request

from dotenv import load_dotenv

from code.qc.algolab import models
from code.qc.algolab.models import AlgorithmLabToolkit

params_filename = 'params.py'


class QCHelper(AlgorithmLabToolkit):
    """ Toolkit for the QuantConnect CommandLine AlgorithmLab API Interactor Tool """

    def __init__(self):
        self.dir_qc_proj = os.path.dirname(os.path.realpath(models.__file__))
        self.dir_script = os.path.dirname(os.path.realpath(__file__))
        self.dotenv_path = os.path.join(os.getcwd(), '.env')
        load_dotenv(self.dotenv_path)
        self.pid = os.environ['QC_BACKTEST_DATERANGE_PID']
        self.uid = os.environ['QC_USER_ID']
        super(QCHelper, self).__init__()

    def get_project_directory(self):
        project_response = self.read_project(self.pid)
        project_details = project_response['projects'][0]
        filename = os.path.join(self.dir_qc_proj, 'project_files/{}_{}'.format(
            project_details['projectId'],
            project_details['name']))
        return filename

    def update_config_params(self, config_file_txt):
        self.update_project_file_content(projectId=self.pid,
                                         fileName=params_filename,
                                         newFileContents=config_file_txt)

#
# def setup_logging():
#     import logging.handlers
#     qc = QCHelper()
#     log_dir = os.path.join(qc.dir_script, 'log')
#     if not os.path.isdir(log_dir):
#         os.mkdir(os.path.join(qc.dir_script, 'log'))
#     log_filename = 'log/algolab.log'
#     log = logging.getLogger('algolab_logger')
#     log.setLevel(logging.DEBUG)
#     # Add handler to create new log file every 10MB
#     file_handler = logging.handlers.RotatingFileHandler(
#         log_filename, maxBytes=10*1024*1024, backupCount=5)
#     log.addHandler(file_handler)


def update_project_params(start_date,
                          end_date):
    # config_file_txt = 'START_DATE = \'{}\'\n' \
    #                   'END_DATE = \'{}\'\n'.format(start_date, end_date)
    daterange = {'start_date': start_date, 'end_date': end_date}
    params_file_contents = 'daterange = {}\n'.format(daterange)
    qc = QCHelper()
    cur_proj_dir = qc.get_project_directory()
    params_filepath = os.path.join(cur_proj_dir, params_filename)
    with open(params_filepath, 'w') as f:
        f.write(params_file_contents)                       # save file locally
    qc.uapf__update_all_project_files(project_id=qc.pid)    # update all remote project files


def compile_project():
    qc = QCHelper()
    print('Compiling project...')
    compile_results = qc.create_compile(qc.pid)
    compile_id = compile_results['compileId']
    print('Checking compilation results')
    while True:
        compile_read_status_results = qc.read_compile(qc.pid, compile_id)

        if compile_read_status_results['state'] == 'InQueue':
            time.sleep(15)  # seconds
            print('Compilation still in queue: waiting.')
        elif compile_read_status_results['state'] == 'BuildError':
            print(compile_read_status_results['logs'])
            exit(0)
        elif compile_read_status_results['state'] == 'BuildSuccess':
            print(compile_read_status_results['logs'])
            return compile_id
        else:
            print(compile_read_status_results)
            print('Error')
            exit(0)


def backtest_compiled_project(compile_id):
    qc = QCHelper()
    print('Triggering project backtest...')
    backtest_name = '{}_{}'.format(
        qc.pid, str(dt.datetime.now())[:19].replace(' ', '_').replace(':', ''))
    backtest_results = qc.create_backtest(qc.pid, compile_id, backtest_name)
    backtest_id = backtest_results['backtestId']
    while True:
        backtest_read_results = qc.read_backtest(qc.pid, backtest_id)
        if backtest_read_results['completed'] is True and backtest_read_results['progress'] == 1:
            print(backtest_read_results['result'])
            print('Successful backtest! Downloading log file...')
            log_url = 'https://www.quantconnect.com/backtests/{}/{}/{}-log.txt'.format(
                qc.uid, qc.pid, backtest_id)
            filename = '{}_{}-log.txt'.format(backtest_name, backtest_id)
            backtest_log_dir = os.path.join(qc.get_project_directory(), '../{}_backtest_logs'.format(qc.pid))
            if not os.path.exists(backtest_log_dir):
                os.makedirs(backtest_log_dir)
            file_path = os.path.join(backtest_log_dir, filename)
            urllib.request.urlretrieve(log_url, file_path)
            print('Backtest log file saved to: {}'.format(file_path))
            return file_path
        print('Waiting for backtest to complete...')
        time.sleep(15)


def read_file_to_log(file_path):
    print(' ===================== Contents of file: ===================== ')
    with open(file_path, 'r') as f:
        lines = f.read().splitlines()
        log_txt = '\n'
        for line in lines:
            log_txt += '{}\n'.format(line)
        print(log_txt)
    print(' ============================ EOF ============================ ')


if __name__ == '__main__':
    # Parse arguments from CLI
    parser = argparse.ArgumentParser(description='Backtest date param passing demo')
    parser.add_argument('-s', '--start_date', metavar=('<start-date>',),
                        default=None, help="First date to run algo on")
    parser.add_argument('-e', '--end_date', metavar=('<end-date>',),
                        default=None, help="Last date to run algo on")
    args = parser.parse_args()
    update_project_params(args.start_date,
                          args.end_date)
    compilation_id = compile_project()
    backtest_log_filepath = backtest_compiled_project(compilation_id)

    read_file_to_log(backtest_log_filepath)
    print('Done.')
