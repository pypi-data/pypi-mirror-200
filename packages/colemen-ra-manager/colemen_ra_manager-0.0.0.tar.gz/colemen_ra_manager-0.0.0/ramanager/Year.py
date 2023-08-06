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
from ramanager.Project import Project as _project
from ramanager.Project import new_project as _new_project


@dataclass
class Year:
    main:_t.main_type = None
    '''A reference to the project manager.'''

    highest_id:int = 0
    directory:c.conf._dir_type = None
    '''The directory instance for this year'''
    _projects:Iterable[_t.project_type] = None
    '''A list of project instances associated to this year'''

    # dir_path:str = None
    # '''The file path to this years directory'''




    def __init__(
        self,
        main:_t.main_type,
        directory:c.conf._dir_type=None,
        ):

        self.main = main
        self.directory = directory
        if directory is None:
            _settings.control.root_directory


    @property
    def dir_path(self):
        '''
            The file path to this years directory

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 03-30-2023 09:38:24
            `@memberOf`: Year
            `@property`: dir_path
        '''
        if self.directory is not None:
            return self.directory.file_path
        else:
            c.dirs.create()
        return value


    @property
    def projects(self):
        '''
            Get this Year's projects

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 03-30-2023 09:47:04
            `@memberOf`: Year
            `@property`: projects
        '''
        value = self._projects
        if value is None:
            value = []
            dirs = c.dirs.get_folders_obj(self.dir_path,recursive=False)
            for pj in dirs:
                proj = _project(self.main,self,pj)
                if proj.project_id is None:
                    continue
                if proj.project_id > self.highest_id:
                    self.highest_id = proj.project_id
                value.append(proj)
            self._projects = value
        return value

    @property
    def next_project_id(self):
        '''
            Get this Year's next_project_id

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 03-30-2023 09:58:54
            `@memberOf`: Year
            `@property`: next_project_id
        '''
        pjs = self.projects
        if len(pjs) == 0:
            return 1
        else:
            return self.highest_id + 1


    def new_project(
        self,
        title:str,
        description:str,
        project_type:str,
        ):
        data = {
            "main":self.main,
            "year":self,
            "directory":None,
            "project_id":self.next_project_id,
            "title":title,
            "description":description,
        }
        pj = _new_project(project_type,**data)
        pj.create_master()
        # project = _project(
        #     self.main,
        #     self,
        #     None,
        #     project_id=self.next_project_id,
        #     title=title,
        #     description=description,
        #     project_type=project_type
        #     )
        # project.create_master()

    # def new_project(self,args):
    #     # print("new_ra9_project")
    #     self.index_current_projects()
    #     title = c.obj.get_arg(args,['title'],None,(str,list))
    #     if isinstance(title,(list)):
    #         title = title[0]
    #     description = c.obj.get_arg(args,['description'],None,(str,list))
    #     if isinstance(description,(list)):
    #         description = description[0]
    #     p_type = c.obj.get_arg(args,['type'],None,(str,list))
    #     if isinstance(p_type,(list)):
    #         p_type = p_type[0]


    #     package = c.obj.get_arg(args,['package'],None,None)
    #     sub_type = None
    #     if p_type == "python":
    #         package = c.types.to_bool(package)
    #         if package:
    #             sub_type = "package"
    #         else:
    #             sub_type = "program"

    #     # print(f"sub_type:{sub_type}")
    #     data = {
    #         "id":self.data['total_projects'] + 1,
    #         "created":datetime.now().strftime('%m-%d-%Y %H:%M:%S'),
    #         "title":title,
    #         "description":description,
    #         "type":p_type,
    #         "sub_type":sub_type,
    #         "dir_path":"",
    #         "user_name":f"{self.main.user_data['first_name']} {self.main.user_data['last_name']}",
    #         "user_email":f"{self.main.user_data['email']}"
    #     }
    #     data = self.get_project_title(data)
    #     data = self.get_project_type(data)
    #     data = self.get_project_sub_type(data)
    #     data = self.get_project_description(data)
    #     if data is False:
    #         return False
    #     data = self.gen_project_title(data)
    #     c.file.writer.to_json("delete.temp.json",data)
    #     self.determine_generator(data)
    #     c.file.writer.to_json("ra9.project_summary.json",data)

    @property
    def is_current(self):
        '''
            Get this Year's is_current

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 03-30-2023 09:26:08
            `@memberOf`: Year
            `@property`: is_current
        '''
        value = self.is_current
        if value is None:
            value = somethingGoesHere
            self.is_current = value
        return value

    @property
    def project_prefix(self):
        '''
            Get this Year's project_prefix
            
            This is the two digit year

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 03-30-2023 10:09:21
            `@memberOf`: Year
            `@property`: project_prefix
        '''
        return datetime.now().strftime('%y')


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
            `@property`: cur_year
        '''
        return datetime.now().strftime('%Y')

    # @property
    # def cur_year_two(self):
    #     '''
    #         Get the current year formatted to two digits, this is just a convenience method for
    #         datetime.now().strftime('%y')

    #         `default`:None


    #         Meta
    #         ----------
    #         `@author`: Colemen Atwood
    #         `@created`: 03-30-2023 09:07:22
    #         `@memberOf`: ProjectManager
    #         `@property`: cur_year
    #     '''
    #     return str(datetime.now().strftime('%y'))

    # @property
    # def cur_year_dir_path(self):
    #     '''
    #         Get the current year's directory path:

    #         A:\some\folder\RA\2023

    #         {root_directory}/{year}

    #         `default`:None


    #         Meta
    #         ----------
    #         `@author`: Colemen Atwood
    #         `@created`: 03-30-2023 09:08:42
    #         `@memberOf`: ProjectManager
    #         `@property`: cur_year_dir_path
    #     '''
    #     return f"{_settings.control.root_directory}/{self.cur_year}"

    # def index_current_projects(self,args=None):
    #     '''
    #         Index the projects in the current years directory or index a specific directory
    #         ----------

    #         Arguments
    #         -------------------------
    #         `args` {dict}
    #             A dictionary of arguments

    #             If `path` is found in this dict, that directory will be indexed instead of the current years

    #         # Return {type}
    #         # ----------------------
    #         # return_description

    #         Meta
    #         ----------
    #         `author`: Colemen Atwood
    #         `created`: 03-30-2023 09:15:36
    #         `memberOf`: ProjectManager
    #         `version`: 1.0
    #         `method_name`: index_current_projects
    #         * @TODO []: documentation for index_current_projects
    #     '''
    #     c.con.log("Indexing Projects")
    #     path = c.obj.get_arg(args,['path'],None)

    #     if isinstance(path,(list)):
    #         path = path[0]
    #     if path is None:
    #         path = self.cur_year_dir_path

    #     directories = c.dirs.get_folders_obj(path,recursive=False)
    #     pjs = []
    #     for p in directories:
    #         if re.match(r"[0-9]{2}-[0-9]{4}",p.name) is not None:
    #             pjs
            



    #     self.data['total_projects'] = len(directories)


    # # def _generate_dirs(self):



    # # @property
    # # def summary(self):
    # #     '''
    # #         Get this ProjectBase's summary

    # #         `default`:None


    # #         Meta
    # #         ----------
    # #         `@author`: Colemen Atwood
    # #         `@created`: 11-14-2022 12:38:55
    # #         `@memberOf`: ProjectBase
    # #         `@property`: summary
    # #     '''
    # #     sum_data = {
    # #         "project_id":self.project_id,
    # #         "project_type":self.project_type,
    # #         "dir_path":self.dir_path,
    # #         "file_path":self.file_path,
    # #         "title":self.title,
    # #         "description":self.description,
    # #         "timestamp":self.timestamp,
    # #     }


    # #     return sum_data


    # # @property
    # # def file_path(self):
    # #     '''
    # #         Get this ProjectBase's file_path

    # #         `default`:None


    # #         Meta
    # #         ----------
    # #         `@author`: Colemen Atwood
    # #         `@created`: 11-14-2022 12:35:07
    # #         `@memberOf`: ProjectBase
    # #         `@property`: file_path
    # #     '''
    # #     value = c.obj.get_arg(self.data,['file_path'],None,(str))
    # #     # @Mstep [IF] if the property is not currenty set
    # #     if value is None:
    # #         value = None
    # #         self.data['file_path'] = value
    # #     return value

    # # @property
    # # def project_id(self):
    # #     '''
    # #         Get this ProjectBase's project_id

    # #         `default`:None


    # #         Meta
    # #         ----------
    # #         `@author`: Colemen Atwood
    # #         `@created`: 11-14-2022 12:36:30
    # #         `@memberOf`: ProjectBase
    # #         `@property`: project_id
    # #     '''
    # #     value = c.obj.get_arg(self.data,['project_id'],None,(str))
    # #     # @Mstep [IF] if the property is not currenty set
    # #     if value is None:
    # #         value = True
    # #         self.data['project_id'] = value
    # #     return value

    # # @property
    # # def project_type(self):
    # #     '''
    # #         Get this ProjectBase's type

    # #         `default`:None


    # #         Meta
    # #         ----------
    # #         `@author`: Colemen Atwood
    # #         `@created`: 11-14-2022 12:36:41
    # #         `@memberOf`: ProjectBase
    # #         `@property`: type
    # #     '''
    # #     value = c.obj.get_arg(self.data,['type'],None,(str))
    # #     # @Mstep [IF] if the property is not currenty set
    # #     if value is None:
    # #         value = "general"
    # #         self.data['type'] = value
    # #     return value

    # # @property
    # # def dir_path(self):
    # #     '''
    # #         Get this ProjectBase's dir_path

    # #         `default`:None


    # #         Meta
    # #         ----------
    # #         `@author`: Colemen Atwood
    # #         `@created`: 11-14-2022 12:37:22
    # #         `@memberOf`: ProjectBase
    # #         `@property`: dir_path
    # #     '''
    # #     value = c.obj.get_arg(self.data,['dir_path'],None,(str))
    # #     # @Mstep [IF] if the property is not currenty set
    # #     if value is None:
    # #         value = True
    # #         self.data['dir_path'] = value
    # #     return value

    # # @property
    # # def title(self):
    # #     '''
    # #         Get this ProjectBase's title

    # #         `default`:None


    # #         Meta
    # #         ----------
    # #         `@author`: Colemen Atwood
    # #         `@created`: 11-14-2022 12:37:46
    # #         `@memberOf`: ProjectBase
    # #         `@property`: title
    # #     '''
    # #     value = c.obj.get_arg(self.data,['title'],None,(str))
    # #     # @Mstep [IF] if the property is not currenty set
    # #     if value is None:
    # #         value = True
    # #         self.data['title'] = value
    # #     return value

    # # @property
    # # def description(self):
    # #     '''
    # #         Get this ProjectBase's description

    # #         `default`:None


    # #         Meta
    # #         ----------
    # #         `@author`: Colemen Atwood
    # #         `@created`: 11-14-2022 12:38:03
    # #         `@memberOf`: ProjectBase
    # #         `@property`: description
    # #     '''
    # #     value = c.obj.get_arg(self.data,['description'],None,(str))
    # #     # @Mstep [IF] if the property is not currenty set
    # #     if value is None:
    # #         value = True
    # #         self.data['description'] = value
    # #     return value

    # # @property
    # # def timestamp(self):
    # #     '''
    # #         Get this ProjectBase's timestamp

    # #         `default`:None


    # #         Meta
    # #         ----------
    # #         `@author`: Colemen Atwood
    # #         `@created`: 11-14-2022 12:38:25
    # #         `@memberOf`: ProjectBase
    # #         `@property`: timestamp
    # #     '''
    # #     value = c.obj.get_arg(self.data,['timestamp'],None,(int,float))
    # #     # @Mstep [IF] if the property is not currenty set
    # #     if value is None:
    # #         value = time.time()
    # #         self.data['timestamp'] = value
    # #     return value









