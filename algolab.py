# -*- coding: utf-8 -*-
import os
import argparse
import logging
import logging.handlers

from code.qc.algolab.models import AlgorithmLabToolkit


def main(create_project,
         list_projects,
         add_file,
         update_file_name,
         list_project_files,
         pull_file,
         push_file,
         pull_all_files,
         push_all_files,
         delete_file_name):
    alt = AlgorithmLabToolkit()

    if create_project is not None:
        create_project_args = getattr(args, 'create_project')
        alt.cp__create_project(
            project_name=create_project_args[0],
            language=create_project_args[1])

    if list_projects is True:
        alt.lp__list_projects()

    if add_file is not None:
        create_project_args = getattr(args, 'add_file')
        alt.af__add_file(
            project_id=create_project_args[0],
            file_name=create_project_args[1],
            file_location=create_project_args[2])

    if list_project_files is not None:
        list_project_files_args = getattr(args, 'list_project_files')
        alt.lpf__list_project_files(project_id=list_project_files_args[0])


if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    log_dir = os.path.join(dir_path, 'log')
    if not os.path.isdir(log_dir):
        os.mkdir(os.path.join(dir_path, 'log'))
    log_filename = 'log/algolab.log'
    log = logging.getLogger('algolab_logger')
    log.setLevel(logging.DEBUG)

    # Add handler to create new log file every 10MB
    file_handler = logging.handlers.RotatingFileHandler(
        log_filename, maxBytes=10*1024*1024, backupCount=5)
    log.addHandler(file_handler)

    """ Parse arguments from CLI """
    # python algolab.py --push_project 1231453647441324, live-algo-name, <code>
    parser = argparse.ArgumentParser(description='QC Project Management CLI Developer Tool')
    parser.add_argument('-cp', '--create_project', nargs=2, metavar=('<project-name>', '<language>'), default=None, help="Create a project with the specified name and language")
    parser.add_argument('-lp', '--list_projects', default=False, action="store_true", help="List all projects")
    parser.add_argument('-af', '--add_file', nargs=3, metavar=('<project-id>', '<file-name>', '<local-file-path>'), default=None, help="Add a file to a project")
    parser.add_argument('-ufn', '--update_file_name', nargs=3, metavar=('<project-id>', '<old-file-name>', '<new-file-name>'), default=None, help="Update the name of a file")
    parser.add_argument('-lpf', '--list_project_files', nargs=1, metavar=('<project-id>',), default=None, help="List all files in a project")
    parser.add_argument('-pullf', '--pull_file', nargs=2, metavar=('<project-id>', '<file-name>'), default=None, help="Download a single file file in a project")
    parser.add_argument('-pushf', '--push_file', nargs=3, metavar=('<project-id>', '<file-name>', '<local-file-path>'), default=None, help="Update the contents of a file")
    parser.add_argument('-pull_all', '--pull_all_files', nargs=1, metavar=('<project-id>',), default=None, help="Download all files in a project")
    parser.add_argument('-push_all', '--push_all_files', nargs=1, metavar=('<project-id>',), default=None, help="Update the contents of all project files")
    # TODO: ensure appropriate conditional logic for above arg
    # (ie: if file does not exist on QC, create file, then update contents).
    parser.add_argument('-dfn', '--delete_file_name', nargs=2, metavar=('<project-id>', '<file-name>'), default=None, help="Delete a file in a project")

    args = parser.parse_args()

    main(args.create_project,
         args.list_projects,
         args.add_file,
         args.update_file_name,
         args.list_project_files,
         args.pull_file,
         args.push_file,
         args.pull_all_files,
         args.push_all_files,
         args.delete_file_name
         )
