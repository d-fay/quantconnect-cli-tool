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

**arguments:**
----

  `-h`, `--help`        
 - show this help message and exit
  
  `-cp <project-name> <language>`, `--create_project <project-name> <language>`     
 - Create a project with the specified name and language

  `-lp`, `--list_projects`

 - List all projects

  `-af <project-id> <file-name> <local-file-path>`, `--add_file <project-id> <file-name> <local-file-path>`

 - Add a file to a project

  `-ufn <project-id> <old-file-name> <new-file-name>`, `--update_file_name <project-id> <old-file-name> <new-file-name>`

 - Update the name of a file

  `-lpf <project-id>`, `--list_project_files <project-id>`

 - List all files in a project

  `-dpf <project-id> <file-name>`, `--download_project_file <project-id> <file-name>`

 - Download a single file file in a project

  `-upf <project-id> <file-name> <local-file-path>`, `--update_project_file <project-id> <file-name> <local-file-path>`

 - Update the contents of a file

  `-dapf <project-id>`, `--download_all_project_files <project-id>`

 - Download all files in a project

  `-uapf <project-id>`, -`-update_all_project_files <project-id>`

 - Update the contents of all project files

  `-deletef <project-id> <file-name>`, `--delete_file <project-id> <file-name>`

 - Delete a file in a project

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
python algolab.py --add_file 1880611 Main.py code/qc/algolab/proj/Main.py
{'files': [{'name': 'Main.py', 'content': 'this is a ...', 'modified': '2018-10-07 06:02:01'}], 'success': True}
```

After making changes to file locally push your updates to the exiting/hosted project and file:
```
$ python algolab.py --update_project_file 1880611 Main.py code/qc/algolab/proj/Main.py
{'files': [{'name': 'Main.py', 'content': 'this is a ...', 'modified': '2018-10-07 06:07:27', 'open': False}], 'success': True}
```