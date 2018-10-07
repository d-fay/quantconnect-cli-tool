# -*- coding: utf-8 -*-
import os
import errno

from dotenv import load_dotenv

from ..api.wrapper import QCApi


class AlgorithmLabToolkit(QCApi):
    """ Toolkit for the QuantConnect CommandLine AlgorithmLab API Interactor Tool """

    def __init__(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.dotenv_path = os.path.join(os.getcwd(), '.env')
        load_dotenv(self.dotenv_path)
        super(AlgorithmLabToolkit, self).__init__(
            userId=os.environ['QC_USER_ID'],
            token=os.environ['QC_ACCESS_TOKEN']
        )

    def _download_files(self, project_response, files_response):
        project_details = project_response['projects'][0]
        for file_data in files_response['files']:
            filename = os.path.join(self.dir_path, 'project_files/{}_{}/{}'.format(
                project_details['projectId'],
                project_details['name'],
                file_data['name']))
            if not os.path.exists(os.path.dirname(filename)):
                try:
                    os.makedirs(os.path.dirname(filename))
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            with open(filename, 'w') as f:
                f.write(str(file_data['content']))
            print(' |- {}'.format(file_data['name']))

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
        with open(file_location, 'r') as f:
            file_contents = f.read()
            add_file_response = self.add_project_file(project_id, file_name, file_contents)
            print(add_file_response)

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

    def dpf__download_project_file(self, project_id, file_name):
        project_response = self.read_project(project_id)
        if not project_response['success']:
            return None
        file_response = self.read_project_file(project_id, file_name)
        if not file_response['success']:
            return None
        self._download_files(project_response, file_response)

    def upf__update_project_file(self, project_id, file_name, local_file_path):
        with open(local_file_path, 'r') as f:
            file_contents = f.read()
            update_file_response = self.update_project_file_content(project_id, file_name, file_contents)
            print(update_file_response)

    def dapf__download_all_project_files(self, project_id):
        project_response = self.read_project(project_id)
        if not project_response['success']:
            return None
        files_response = self.read_project_files(projectId=project_id)
        if not files_response['success']:
            return None
        self._download_files(project_response, files_response)

    def uapf__update_all_project_files(self, project_id):
        project_response = self.read_project(project_id)
        if not project_response['success']:
            return None
        files_response = self.read_project_files(project_id)
        if not files_response['success']:
            return None
        project_details = project_response['projects'][0]
        project_dir = os.path.join(self.dir_path, 'project_files/{}_{}'.format(
            project_details['projectId'],
            project_details['name']))
        local_project_files = os.listdir(project_dir)
        for file_name in local_project_files:
            file_path = os.path.join(project_dir, file_name)
            with open(file_path, 'r') as f:
                file_contents = f.read()
                update_file_response = self.update_project_file_content(project_id, file_name, file_contents)
                print(update_file_response)

    def deletef__delete_file(self, project_id, file_name):
        delete_file_response = self.delete_project_file(project_id, file_name)
        print(delete_file_response)
