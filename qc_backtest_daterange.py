# -*- coding: utf-8 -*-
import argparse
import logging.handlers
import os
import time
import datetime as dt
import urllib.request

from dotenv import load_dotenv

from code.qc.algolab import models
from code.qc.api.wrapper import QCApi

dir_script = os.path.dirname(os.path.realpath(__file__))
dotenv_path = os.path.join(os.getcwd(), '.env')
load_dotenv(dotenv_path)

uid = os.environ['QC_USER_ID'],
token = os.environ['QC_ACCESS_TOKEN']
pid = os.environ['QC_BACKTEST_DATERANGE_PID']


class QCHelper(QCApi):
    """ Toolkit for the QuantConnect CommandLine AlgorithmLab API Interactor Tool """

    def __init__(self):
        self.dir_qc_proj = os.path.dirname(os.path.realpath(models.__file__))
        super(QCHelper, self).__init__(userId=uid, token=token)

    def get_project_directory(self):

        project_response = self.read_project(pid)
        project_details = project_response['projects'][0]
        filename = os.path.join(self.dir_qc_proj, 'project_files/{}_{}'.format(
            project_details['projectId'],
            project_details['name']))
        return filename

    def update_config_params(self, config_file_txt):
        self.update_project_file_content(projectId=pid,
                                         fileName='conf.py',
                                         newFileContents=config_file_txt)


def setup_logging():
    log_dir = os.path.join(dir_script, 'log')
    if not os.path.isdir(log_dir):
        os.mkdir(os.path.join(dir_script, 'log'))
    log_filename = 'log/qc_backtest_daterange.log'
    log = logging.getLogger('qc_backtest_daterange_logger')
    log.setLevel(logging.DEBUG)

    # Add handler to create new log file every 10MB
    file_handler = logging.handlers.RotatingFileHandler(
        log_filename, maxBytes=10*1024*1024, backupCount=5)
    log.addHandler(file_handler)


def update_project_params(start_date,
                          end_date):
    config_file_txt = 'START_DATE = \'{}\'\n' \
                      'END_DATE = \'{}\'\n'.format(start_date[0], end_date[0])
    qc = QCHelper()
    cur_proj_dir = qc.get_project_directory()
    config_filepath = os.path.join(cur_proj_dir, 'conf.py')
    # save file locally
    with open(config_filepath, 'w') as f:
        f.write(config_file_txt)
    # update remotely
    qc.update_config_params(config_file_txt)


def compile_project():
    qc = QCHelper()
    print('Compiling project...')
    compile_results = qc.create_compile(pid)
    compile_id = compile_results['compileId']
    print('Checking compilation results')
    while True:
        compile_read_status_results = qc.read_compile(pid, compile_id)

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
        pid, str(dt.datetime.now())[:19].replace(' ', '_').replace(':', ''))
    backtest_results = qc.create_backtest(pid, compile_id, backtest_name)
    backtest_id = backtest_results['backtestId']
    backtest_read_results = qc.read_backtest(pid, backtest_id)
    while backtest_read_results['progress'] < 1:
        print('Waiting for backtest to complete...')
        time.sleep(15)
        backtest_read_results = qc.read_backtest(pid, backtest_id)
    if backtest_read_results['completed'] is True:
        print(backtest_read_results['result'])
        print('Successful backtest! Downloading log file...')

        log_url = 'https://www.quantconnect.com/backtests/{}/{}/{}-log.txt'.format(
            uid, pid, backtest_id)

        filename = '{}_{}-log.txt'.format(backtest_name, backtest_id)
        backtest_log_dir = os.path.join(qc.get_project_directory(), 'backtest_logs')
        if not os.path.exists(backtest_log_dir):
            os.makedirs(backtest_log_dir)
        file_path = os.path.join(backtest_log_dir, filename)
        urllib.request.urlretrieve(log_url, file_path)
        return file_path


if __name__ == '__main__':
    setup_logging()

    """ Parse arguments from CLI """
    parser = argparse.ArgumentParser(description='Backtest date param passing demo')
    parser.add_argument('-s', '--start_date', nargs=1, metavar=('<start-date>',), default=None, help="First date to run algo on")
    parser.add_argument('-e', '--end_date', nargs=1, metavar=('<end-date>',), default=None, help="Last date to run algo on")

    args = parser.parse_args()

    update_project_params(args.start_date,
                          args.end_date)
    compile_id = compile_project()
    backtest_compiled_project(compile_id)
    print('Done.')
