# -*- coding: utf-8 -*-
import os
import errno

from dotenv import load_dotenv

from ..api.wrapper import QCApi


class AlgorithmLabToolkit(QCApi):
    """ Toolkit for the QuantConnect CommandLine AlgorithmLab API Interactor Tool """

    def __init__(self):
        self.dotenv_path = os.path.join(os.getcwd(), '.env')
        load_dotenv(self.dotenv_path)
        super(AlgorithmLabToolkit, self).__init__(
            userId=os.environ['QC_USER_ID'],
            token=os.environ['QC_ACCESS_TOKEN']
        )
        # self.user_id = os.environ['QC_USER_ID']
        # self.token = os.environ['QC_ACCESS_TOKEN']

    def cp__create_project(self, project_name, language):
        response = self.create_project(project_name, language)
        print(response)

    def lp__list_projects(self):
        projects_response = self.list_projects()
        print('\nPROJECTS')
        # print every key and value in list of dictionaries
        print('  | {} ---- | {} -------------------------'.format('ID', 'NAME'))
        for project in projects_response['projects']:
            print('  | {} | {}'.format(project['projectId'], project['name']))
        print('')

    def af__add_file(self, project_id, file_name, file_location):
        response = self.add_project_file(project_id, file_name, file_location)
        print(response)

    def ufn__update_file_name(self, project_id, old_file_name, new_file_name):
        response = self.update_project_filename(project_id, old_file_name, new_file_name)
        print(response)

    def lpf__list_project_files(self, project_id):
        files_response = self.read_project_files(project_id)
        if not files_response['success']:
            return None
        print('FILES:')
        for file_data in files_response['files']:
            print(' |- {}'.format(file_data['name']))

    def pf__pull_file(self, project_id, file_name):
        pass

    def pf__push_file(self, project_id, file_name):
        pass

    def pull_all__pull_all_files(self, project_id):
        pass

    def push_all___push_all_files(self, project_id):
        pass

    def daf__delete_file_name(self, project_id, file_name):
        pass
