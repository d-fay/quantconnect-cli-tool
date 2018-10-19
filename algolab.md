*QC Project Management CLI Developer Tool*
==========================================
```
usage: algolab.py [-h] [-cp <project-name> <language>] [-lp]
                  [-af <project-id> <file-name> <local-file-path>]
                  [-ufn <project-id> <old-file-name> <new-file-name>]
                  [-lpf <project-id>] [-dpf <project-id> <file-name>]
                  [-upf <project-id> <file-name> <local-file-path>]
                  [-dapf <project-id>] [-uapf <project-id>]
                  [-deletef <project-id> <file-name>]
```

## arguments:


#### Help
-   `-h`
-   `--help`        

#### Create a project with specified name and language (ie: `Py`)
-   `-cp <project-name> <language>`
-   `--create_project <project-name> <language>`     

#### List all projects
-   `-lp`
-   `--list_projects`


#### Add a file to a project 
-   `-af <project-id> <file-name> <local-file-path>`
-   `--add_file <project-id> <file-name> <local-file-path>`


#### Update the name of a file

-   `-ufn <project-id> <old-file-name> <new-file-name>`
-   `--update_file_name <project-id> <old-file-name> <new-file-name>`


#### List all files in a project

-   `-lpf <project-id>`
-   `--list_project_files <project-id>`

#### Download a single file file in a project

-   `-dpf <project-id> <file-name>`
-   `--download_project_file <project-id> <file-name>`

#### Update the contents of a file

-   `-upf <project-id> <file-name> <local-file-path>`
-   `--update_project_file <project-id> <file-name> <local-file-path>`

#### Download all files in a project

-   `-dapf <project-id>`
-   `--download_all_project_files <project-id>`

#### Update the contents of all project files

-   `-uapf <project-id>`
-   `--update_all_project_files <project-id>`

#### Delete a file in a project

-   `-deletef <project-id> <file-name>`
-   `--delete_file <project-id> <file-name>`


-----
Example usage:
-----

Create a new project:
```
$ python algolab.py --create_project test_project Py
{'projects': [{'projectId': 1880611, 'name': 'test_project', 'created': '2018-10-07 05:53:57', 'modified': '2018-10-07 05:53:57'}], 'success': True}
```

List projects to obtain `project_id`:
```
$ python algolab.py --list_projects

PROJECTS
  | ID ---- | NAME -------------------------
  | 1880611 | test_project
  | 1878550 | test_proj_1

```

Add file to QC project using `project_id`:
```
$ python algolab.py --add_file 1880611 Main.py code/qc/algolab/proj/Main.py
{'files': [{'name': 'Main.py', 'content': 'this is a ...', 'modified': '2018-10-07 06:02:01'}], 'success': True}
```

After making changes to file locally push your updates to the exiting/hosted project and file:
```
$ python algolab.py --update_project_file 1880611 Main.py code/qc/algolab/proj/Main.py
{'files': [{'name': 'Main.py', 'content': 'this is a ...', 'modified': '2018-10-07 06:07:27', 'open': False}], 'success': True}
```