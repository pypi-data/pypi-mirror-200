# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

from dataclasses import dataclass
from datetime import datetime
import os
import re
import time
from typing import Iterable

import colemen_utils as c

import ramanager.settings.types as _t
import ramanager.settings as _settings
from ramanager.Year import Year as _Year
from ramanager.inputs import inputs


@dataclass
class ProjectManager:
    alice = None
    '''A reference to the ALICE instance used for adding CLI arguments.'''

    _years:Iterable[_t.year_type] = None
    '''A dictionry of Year instances within the root directory'''
    projects:Iterable[_t.project_type] = None
    cur_year_project_count:int = 0
    '''How many project directories are in the current year directory.'''




    def __init__(
        self,
        alice=None,
        root_directory:str=None,
        user_name:str=None,
        user_email:str=None,
        pypi_user_name:str=None,
        pypi_password:str=None,
        ):

        if alice is not None:
            self.alice = alice

        if isinstance(root_directory,(str)):
            _settings.control.root_directory = root_directory
            _settings.control.user_name = user_name
            _settings.control.user_email = user_email
            _settings.control.pypi_user_name = pypi_user_name
            _settings.control.pypi_password = pypi_password

        self.apply_alice_args()



    def apply_alice_args(self):
        if self.alice is None:
            return None
        self.alice.add_auto_replace(r"ra[0-9\s]","ra9",regex=True)
        self.alice.add_auto_replace(r"(ra9(\s|_)?new|new(\s|_)?ra9)(\s|_)?project","ra9 new_ra9_project",regex=True)
        self.settings_path = f'{os.getcwd()}/alice/ra9_project/ra9_project.settings.json'
        self.settings = c.file.import_project_settings(self.settings_path)

        parser_new = self.alice.subparsers.add_parser('ra9',help="Manage Ra9 Projects")
        ra9_sub_parsers = parser_new.add_subparsers()

        new_ra9_project_parser = ra9_sub_parsers.add_parser('new_ra9_project',help="Create a new Ra9 Project",aliases=['new ra9 project'])
        new_ra9_project_parser.add_argument('-title','-t',nargs=1,type=str,default=None, help='The name of the new project')
        new_ra9_project_parser.add_argument('-description','-d',nargs=1,type=str,default=None, help='The new project description')
        new_ra9_project_parser.add_argument('-type','-ty',nargs=1,type=str,default=None, help='The new project type',choices=self.settings['types'])
        # new_ra9_project_parser.add_argument('-package','-pkg',default=False,action='store_true', help='True if this is a pypi package')
        new_ra9_project_parser.set_defaults(func=self.new_project)

        # index_parser = ra9_sub_parsers.add_parser('index',help="Index the current projects")
        # index_parser.add_argument('-path','-p',nargs=1,type=str,default=None, help='The directory to treat as the projects root.')
        # index_parser.set_defaults(func=self.index_current_projects)

        # ra_compress = ra9_sub_parsers.add_parser('compress',help="compress older projects")
        # ra_compress.add_argument('-archive','-a',default=False,action='store_true', help='Only zip projects with the archive attribute')
        # ra_compress.add_argument('-max_age','-m',nargs=1,type=int,default=365, help='How many days since the last modification before zipping.')
        # ra_compress.set_defaults(func=self.compress_old)


    def _arg_new_project(self,args):
        '''used for CLI argument parsing prior to calling new_project'''
        title = c.obj.get_arg(args,['title'],None,(str,list))
        if isinstance(title,(list)):
            title = title[0]
        description = c.obj.get_arg(args,['description'],None,(str,list))
        if isinstance(description,(list)):
            description = description[0]
        project_type = c.obj.get_arg(args,['type'],None,(str,list))
        if isinstance(project_type,(list)):
            project_type = project_type[0]
        data = {
            "title":title,
            "description":description,
            "project_type":project_type,
        }
        data = self.get_project_title(data)
        data = self.get_project_type(data)
        data = self.get_project_description(data)
        self.new_project(**data)


    def get_project_title(self,data):
        if 'title' in data:
            if data['title'] is None:
                data['title'] = inputs.required_cycle("Enter the project title: ")
            else:
                data['title'] = data['title']

        if data['title'] is False:
            return False
        if data['title'] == "rand":
            data['title'] = c.string.to_snake_case(c.rand.abstract_name())
        return data

    def get_project_type(self,data):
        if data is False:
            return False
        if data['project_type'] is None:
            data['project_type'] = 'general'
            print("")
            self.list_project_types()
            print("Leave blank to create a general project.")
            ptyp = inputs.get_input("Enter the project type: ")
            if ptyp is False:
                return False

            if len(ptyp) == 0:
                data['project_type'] = 'general'
            else:
                data['project_type'] = ptyp
        return data

    def get_project_sub_type(self,data):
        if data is False:
            return False
        sub_type = c.obj.get_arg(data,['sub_type'],None,(str))

        if data['project_type'] == "python":
            if sub_type not in ['package','program']:
                data['sub_type'] = 'program'
                result = inputs.getuser_confirmation("Is this a library package? (Y/N)")
                if result is True:
                    # print(f"generate a python package project")
                    data['sub_type'] = 'package'

        return data
    def get_project_description(self,data):
        if data is False:
            return False
        if data['description'] is None:
            data['description'] = inputs.get_input("Enter the project description: ")
            # data['description'] = inputs.required_cycle("Enter the project description: ")

        return data



    def new_project(
        self,
        title:str=None,
        description:str=None,
        project_type:str="general"
        ):
        
        yr = self.current_year
        yr.new_project(
            title=title,
            description=description,
            project_type=project_type
        )
        # TODO []: Instantiate the new project
        # TODO []: register a project with the year.
        # # print("new_ra9_project")
        # self.index_current_projects()
        # title = c.obj.get_arg(args,['title'],None,(str,list))
        # if isinstance(title,(list)):
        #     title = title[0]
        # description = c.obj.get_arg(args,['description'],None,(str,list))
        # if isinstance(description,(list)):
        #     description = description[0]
        # project_type = c.obj.get_arg(args,['type'],None,(str,list))
        # if isinstance(project_type,(list)):
        #     project_type = project_type[0]


        # package = c.obj.get_arg(args,['package'],None,None)
        # sub_type = None
        # if project_type == "python":
        #     package = c.types.to_bool(package)
        #     if package:
        #         sub_type = "package"
        #     else:
        #         sub_type = "program"

        # # print(f"sub_type:{sub_type}")
        # data = {
        #     "id":self.data['total_projects'] + 1,
        #     "created":datetime.now().strftime('%m-%d-%Y %H:%M:%S'),
        #     "title":title,
        #     "description":description,
        #     "type":project_type,
        #     "sub_type":sub_type,
        #     "dir_path":"",
        #     "user_name":f"{self.alice.user_data['first_name']} {self.alice.user_data['last_name']}",
        #     "user_email":f"{self.alice.user_data['email']}"
        # }
        # data = self.get_project_title(data)
        # data = self.get_project_type(data)
        # data = self.get_project_sub_type(data)
        # data = self.get_project_description(data)
        # if data is False:
        #     return False
        # data = self.gen_project_title(data)
        # c.file.writer.to_json("delete.temp.json",data)
        # self.determine_generator(data)
        # c.file.writer.to_json("ra9.project_summary.json",data)


    @property
    def years(self):
        '''
            Get this ProjectManager's years

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 03-30-2023 09:29:11
            `@memberOf`: ProjectManager
            `@property`: years
        '''
        value = self._years
        if value is None:
            dirs = c.dirs.get_folders_obj(_settings.control.root_directory,recursive=False)
            if len(dirs) == 0:
                c.con.log(f"Creating current year directory: {self.cur_year_dir_path}","info")
                c.dirs.create(self.cur_year_dir_path)

                dirs = c.dirs.get_folders_obj(_settings.control.root_directory,recursive=False)
            value = {}
            for d in dirs:
                y = _Year(self,d)

                value[d.name] = y
            self._years = value
        return value

    @property
    def current_year(self)->_t.year_type:
        '''
            Get this ProjectManager's current_year

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 03-30-2023 09:44:08
            `@memberOf`: ProjectManager
            `@property`: current_year
        '''
        y = self.years
        value = None
        if self.cur_year_four in y:
            value = y[self.cur_year_four]
        return value

    @property
    def cur_year_four(self):
        '''
            Get the current year formatted to four digits, this is just a convenience method for
            datetime.now().strftime('%Y')

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 03-30-2023 09:07:22
            `@memberOf`: ProjectManager
            `@property`: cur_year_four
        '''
        return datetime.now().strftime('%Y')

    @property
    def cur_year_two(self):
        '''
            Get the current year formatted to two digits, this is just a convenience method for
            datetime.now().strftime('%y')

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 03-30-2023 09:07:22
            `@memberOf`: ProjectManager
            `@property`: cur_year_two
        '''
        return str(datetime.now().strftime('%y'))

    @property
    def cur_year_dir_path(self):
        '''
            Get the current year's directory path:

            A:\some\folder\RA\2023

            {root_directory}/{year}

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 03-30-2023 09:08:42
            `@memberOf`: ProjectManager
            `@property`: cur_year_dir_path
        '''
        return f"{_settings.control.root_directory}/{self.cur_year_four}"

    def index_current_projects(self,args=None):
        '''
            Index the projects in the current years directory or index a specific directory
            ----------

            Arguments
            -------------------------
            `args` {dict}
                A dictionary of arguments

                If `path` is found in this dict, that directory will be indexed instead of the current years

            # Return {type}
            # ----------------------
            # return_description

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 03-30-2023 09:15:36
            `memberOf`: ProjectManager
            `version`: 1.0
            `method_name`: index_current_projects
            * @TODO []: documentation for index_current_projects
        '''
        c.con.log("Indexing Projects")
        path = c.obj.get_arg(args,['path'],None)

        if isinstance(path,(list)):
            path = path[0]
        if path is None:
            path = self.cur_year_dir_path

        directories = c.dirs.get_folders_obj(path,recursive=False)
        pjs = []
        for p in directories:
            if re.match(r"[0-9]{2}-[0-9]{4}",p.name) is not None:
                pjs
            



        self.data['total_projects'] = len(directories)


    # def _generate_dirs(self):



    # @property
    # def summary(self):
    #     '''
    #         Get this ProjectBase's summary

    #         `default`:None


    #         Meta
    #         ----------
    #         `@author`: Colemen Atwood
    #         `@created`: 11-14-2022 12:38:55
    #         `@memberOf`: ProjectBase
    #         `@property`: summary
    #     '''
    #     sum_data = {
    #         "project_id":self.project_id,
    #         "project_type":self.project_type,
    #         "dir_path":self.dir_path,
    #         "file_path":self.file_path,
    #         "title":self.title,
    #         "description":self.description,
    #         "timestamp":self.timestamp,
    #     }


    #     return sum_data


    # @property
    # def file_path(self):
    #     '''
    #         Get this ProjectBase's file_path

    #         `default`:None


    #         Meta
    #         ----------
    #         `@author`: Colemen Atwood
    #         `@created`: 11-14-2022 12:35:07
    #         `@memberOf`: ProjectBase
    #         `@property`: file_path
    #     '''
    #     value = c.obj.get_arg(self.data,['file_path'],None,(str))
    #     # @Mstep [IF] if the property is not currenty set
    #     if value is None:
    #         value = None
    #         self.data['file_path'] = value
    #     return value

    # @property
    # def project_id(self):
    #     '''
    #         Get this ProjectBase's project_id

    #         `default`:None


    #         Meta
    #         ----------
    #         `@author`: Colemen Atwood
    #         `@created`: 11-14-2022 12:36:30
    #         `@memberOf`: ProjectBase
    #         `@property`: project_id
    #     '''
    #     value = c.obj.get_arg(self.data,['project_id'],None,(str))
    #     # @Mstep [IF] if the property is not currenty set
    #     if value is None:
    #         value = True
    #         self.data['project_id'] = value
    #     return value

    # @property
    # def project_type(self):
    #     '''
    #         Get this ProjectBase's type

    #         `default`:None


    #         Meta
    #         ----------
    #         `@author`: Colemen Atwood
    #         `@created`: 11-14-2022 12:36:41
    #         `@memberOf`: ProjectBase
    #         `@property`: type
    #     '''
    #     value = c.obj.get_arg(self.data,['type'],None,(str))
    #     # @Mstep [IF] if the property is not currenty set
    #     if value is None:
    #         value = "general"
    #         self.data['project_type'] = value
    #     return value

    # @property
    # def dir_path(self):
    #     '''
    #         Get this ProjectBase's dir_path

    #         `default`:None


    #         Meta
    #         ----------
    #         `@author`: Colemen Atwood
    #         `@created`: 11-14-2022 12:37:22
    #         `@memberOf`: ProjectBase
    #         `@property`: dir_path
    #     '''
    #     value = c.obj.get_arg(self.data,['dir_path'],None,(str))
    #     # @Mstep [IF] if the property is not currenty set
    #     if value is None:
    #         value = True
    #         self.data['dir_path'] = value
    #     return value

    # @property
    # def title(self):
    #     '''
    #         Get this ProjectBase's title

    #         `default`:None


    #         Meta
    #         ----------
    #         `@author`: Colemen Atwood
    #         `@created`: 11-14-2022 12:37:46
    #         `@memberOf`: ProjectBase
    #         `@property`: title
    #     '''
    #     value = c.obj.get_arg(self.data,['title'],None,(str))
    #     # @Mstep [IF] if the property is not currenty set
    #     if value is None:
    #         value = True
    #         self.data['title'] = value
    #     return value

    # @property
    # def description(self):
    #     '''
    #         Get this ProjectBase's description

    #         `default`:None


    #         Meta
    #         ----------
    #         `@author`: Colemen Atwood
    #         `@created`: 11-14-2022 12:38:03
    #         `@memberOf`: ProjectBase
    #         `@property`: description
    #     '''
    #     value = c.obj.get_arg(self.data,['description'],None,(str))
    #     # @Mstep [IF] if the property is not currenty set
    #     if value is None:
    #         value = True
    #         self.data['description'] = value
    #     return value

    # @property
    # def timestamp(self):
    #     '''
    #         Get this ProjectBase's timestamp

    #         `default`:None


    #         Meta
    #         ----------
    #         `@author`: Colemen Atwood
    #         `@created`: 11-14-2022 12:38:25
    #         `@memberOf`: ProjectBase
    #         `@property`: timestamp
    #     '''
    #     value = c.obj.get_arg(self.data,['timestamp'],None,(int,float))
    #     # @Mstep [IF] if the property is not currenty set
    #     if value is None:
    #         value = time.time()
    #         self.data['timestamp'] = value
    #     return value









