# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import




from dataclasses import dataclass
import os
from pathlib import Path, PurePath
from string import Template
import subprocess
import colemen_utils as c

import ramanager.settings.types as _t
import ramanager.settings as _settings

from ramanager.ProjectBase import ProjectBase

# VALID_PROJECT_TYPES = ["general","python","3dprint"]

@dataclass
class Project(ProjectBase):


    def __init__(
        self,
        main:_t.main_type,
        year:_t.year_type,
        directory:c.conf._dir_type = None,
        project_id:int=None,
        title:str=None,
        description:str=None,
        project_type:str=None,
        ):
        super().__init__(main, year, directory,project_id,title,description,project_type,)




class GeneralProject(ProjectBase):


    def create_master(self):
        print(f"GeneralProject.create_master")
        c.dirs.create(self.dir_path)
        self.directory = c.dirs.get_folder(self.dir_path)

class PrintingProject(ProjectBase):


    def __init__(
        self,
        main:_t.main_type,
        year:_t.year_type,
        directory:c.conf._dir_type = None,
        project_id:int=None,
        title:str=None,
        description:str=None,
        project_type:str=None,
        ):
        super().__init__(main, year, directory,project_id,title,description,project_type,)


    def create_master(self):
        c.con.log(f"Creating 3D Printing Project","info")
        self.dir_path = Path(PurePath(self.dir_path)).as_posix()
        c.dirs.create(self.dir_path)
        self.directory = c.dirs.get_folder(self.dir_path)

        tmp_dir_path = Path(PurePath(get_template_dir_path("3DPrinting"))).as_posix()

        # print(f"tmp_dir_path:{tmp_dir_path}")
        dir_reps = {}
        c.con.log("    Creating Project Base Directories","info")
        for d in c.dirs.get_folders_obj(tmp_dir_path):
            dst = d.file_path.replace(tmp_dir_path,self.dir_path)
            dst = c.string.dict_replace_string(dst,dir_reps)
            c.dirs.create(dst)

        c.con.log("    Creating Project Base Files","info")
        for d in c.file.get_files_obj(tmp_dir_path):

            dst = d.file_path.replace(tmp_dir_path,self.dir_path)
            dst = c.string.dict_replace_string(dst,dir_reps)

            if d.name.endswith(".ratmp"):
                name = d.name
                name = c.string.dict_replace_string(name,dir_reps)
                # c.string.replace_end(d.name,".ratmp","")
                dst = dst.replace(name,name.replace(".ratmp",""))
                s = Template(c.file.readr(d.file_path))
                val = s.substitute(
                    title=self.title,
                    package_title=self.title,
                    description=self.description,
                    title_snake_case=self.sub_dir_name,
                    modules_dir_name=self.modules_dir_name,
                    main_class_name=self.main_class_name,
                    sub_dir_name=self.sub_dir_name,
                    user_name=_settings.control.user_name,
                    user_email=_settings.control.user_email,
                    pypi_user_name=_settings.control.pypi_user_name,
                    pypi_password=_settings.control.pypi_password,
                    drive_letter=self.directory.drive,
                    venv_path=c.string.file_path(self.venv_path),
                )
                # print(f"dst: {dst}")
                c.file.write(dst,val)
            else:
                c.file.copy(d.file_path,dst)







        c.con.log(f"Successfully Created Project {self.title}","green invert")





@dataclass
class PythonProject(ProjectBase):
    tests_path:str = None
    '''The path to the tests directory.

    .../ra9/23-1234 - project name/project_name/.venv/tests
    '''

    setup_path:str = None
    '''The path to the setup.py file

    .../ra9/23-1234 - project name/project_name/.venv/setup.py
    '''
    vscode_dir_path:str = None
    '''The path to the vscode settings directory.

    .../ra9/23-1234 - project name/project_name/.venv/.vscode
    '''
    vscode_settings_path:str = None
    '''The path to the vscode settings json file.

    .../ra9/23-1234 - project name/project_name/.venv/.vscode/settings.json
    '''
    settings_package_path:str = None
    '''The path to the settings package

    .../ra9/23-1234 - project name/project_name/.venv/project_name/settings
    '''



    sub_dir_name:str = None
    '''The name of the sub folder for this project (useful for git repos)

    project_name

    '''
    sub_dir_path:str = None
    '''The name of the sub folder for this project (useful for git repos)

    .../ra9/23-1234 - project name/project_name

    '''

    modules_dir_name:str = None
    '''The name of the directory that stores the programs modules.
    This is the name of the project converted to snake case.
    '''

    modules_path:str = None
    '''The path to the modules directory

    .../ra9/23-1234 - project name/project_name/.venv/project_name

    '''
    

    def __init__(
        self,
        main:_t.main_type,
        year:_t.year_type,
        directory:c.conf._dir_type = None,
        project_id:int=None,
        title:str=None,
        description:str=None,
        project_type:str=None,
        ):
        super().__init__(main, year, directory,project_id,title,description,project_type,)


    
    
    def create_master(self):
        c.con.log(f"Creating Python Project","info")
        self.dir_path = Path(PurePath(self.dir_path)).as_posix()
        c.dirs.create(self.dir_path)
        self.directory = c.dirs.get_folder(self.dir_path)
        self.pypi_info_provided = False
        if _settings.control.pypi_user_name is not None:
            self.pypi_info_provided = True
        # template = get_template("PythonPackage")
        # for d in template


        self.sub_dir_name = c.string.to_snake_case(self.title)
        self.sub_dir_path = f"{self.dir_path}/{self.sub_dir_name}"

        self.venv_path = f"{self.sub_dir_path}/.venv"
        self.scripts_path = f"{self.venv_path}/Scripts"
        self.build_setup_path = f"{self.venv_path}/BuildSetupTmp.py"
        self.main_path = f"{self.venv_path}/main.py"
        self.documentation_path = f"{self.venv_path}/documentation"

        self.settings_package_path = f"{self.modules_path}/settings"
        self.tests_path = f"{self.venv_path}/tests"
        self.setup_path = f"{self.venv_path}/setup.py"
        self.vscode_dir_path = f"{self.venv_path}/.vscode"
        self.vscode_settings_path = f"{self.vscode_dir_path}/settings.json"

        self.modules_dir_name = self.sub_dir_name
        self.modules_path = f"{self.venv_path}/{self.modules_dir_name}"
        self.main_class_name = c.string.to_pascal_case(self.title)

        tmp_dir_path = Path(PurePath(get_template_dir_path("PythonPackage"))).as_posix()




        dir_reps = {
                "$project_name_snake":self.sub_dir_name,
                "$modules_dir_name":self.modules_dir_name,
                "$main_class_name":self.main_class_name,
            }
        c.con.log("    Creating Project Base Directories","info")
        for d in c.dirs.get_folders_obj(tmp_dir_path):
            dst = d.file_path.replace(tmp_dir_path,self.dir_path)
            dst = c.string.dict_replace_string(dst,dir_reps)
            c.dirs.create(dst)

        # TODO []: temporarily commented
        self.create_python_venv()
        # TODO []: temporarily commented

        c.con.log("    Creating Project Base Files","info")
        for d in c.file.get_files_obj(tmp_dir_path):

            dst = d.file_path.replace(tmp_dir_path,self.dir_path)
            dst = c.string.dict_replace_string(dst,dir_reps)

            if d.name.endswith(".ratmp"):
                name = d.name
                name = c.string.dict_replace_string(name,dir_reps)
                # c.string.replace_end(d.name,".ratmp","")
                dst = dst.replace(name,name.replace(".ratmp",""))
                s = Template(c.file.readr(d.file_path))
                val = s.substitute(
                    title=self.title,
                    package_title=self.title,
                    description=self.description,
                    title_snake_case=self.sub_dir_name,
                    modules_dir_name=self.modules_dir_name,
                    main_class_name=self.main_class_name,
                    sub_dir_name=self.sub_dir_name,
                    user_name=_settings.control.user_name,
                    user_email=_settings.control.user_email,
                    pypi_user_name=_settings.control.pypi_user_name,
                    pypi_password=_settings.control.pypi_password,
                    drive_letter=self.directory.drive,
                    venv_path=c.string.file_path(self.venv_path),
                )
                # print(f"dst: {dst}")
                c.file.write(dst,val)
            else:
                c.file.copy(d.file_path,dst)
                # contents = c.file.readr(d.file_path)
                # creps = {
                #     "title":self.title,
                #     "description":self.description,
                #     "title_snake_case":self.sub_dir_name,
                # }
            # c.dirs.create(dst)
        self._run_build_setup()
        
        c.con.log(f"Successfully Created Project {self.title}","green invert")

    def create_python_venv(self):
        c.con.log("    Creating Python virtual environment.","info")
        subprocess.run("python -m venv .venv",cwd=self.sub_dir_path,check=True, capture_output=True, text=True)
        install_cfu = "activate.bat & pip install colemen-utils"
        install_pylint = "activate.bat & pip install pylint"
        try:
            c.con.log("        Installing colemen utilities","info")
            subprocess.run(install_cfu,cwd=f"{self.venv_path}/Scripts",check=True, capture_output=True, text=True)
            c.con.log("        Installing pylint","info")
            subprocess.run(install_pylint,cwd=f"{self.venv_path}/Scripts",check=True, capture_output=True, text=True)
            return True
        except subprocess.CalledProcessError as e:
            c.con.log("An error has occured while attempting to create the virtual environment.","red invert")
            c.con.log("This can happen if there is no internet connection.","red invert")
            print(e)
            return False

    def _run_build_setup(self):
        c.con.log("    Setting up Pypi build utilities.","info")
        venv_path = c.string.file_path(self.venv_path,url=True)
        batch_path = f"{venv_path}/executeBuildSetup.bat"
        print(f"batch_path: {batch_path}")

        subprocess.call([batch_path])
        c.file.delete(f"{venv_path}/executeBuildSetup.bat")
        c.file.delete(f"{venv_path}/BuildSetupTmp.py")


def get_template_dir_path(name:str):
    path = f"{os.getcwd()}/ramanager/templates/{name}"
    if c.dirs.exists(path):
        return path
    path = f"{os.getcwd()}/Lib/site-packages/ramanager/templates/{name}"
    if c.dirs.exists(path):
        return path


def new_project(project_type:str=None,**kwargs)->_t.project_type:
    if project_type is None:
        project_type = "general"
    type_found = False

    # creator = DynamicClassCreator()
    if project_type == "general":
        proj = GeneralProject(**kwargs)
        type_found = True
    if project_type == "python":
        proj = PythonProject(**kwargs)
        type_found = True
    if project_type in ["3dprint","print","printing"]:
        proj = PrintingProject(**kwargs)
        type_found = True
    if type_found is False:
        raise ValueError(f"Invalid Project Type: {project_type}")
    return proj



