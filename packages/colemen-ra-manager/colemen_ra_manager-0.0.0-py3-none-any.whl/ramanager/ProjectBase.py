# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

from dataclasses import dataclass
from datetime import datetime
import re
import time

import colemen_utils as c

import ramanager.settings.types as _t
import ramanager.settings as _settings




@dataclass
class ProjectBase:
    main:_t.main_type = None

    '''A reference to the project manager.'''

    year:_t.year_type = None
    '''The year instance that this project belongs to'''

    directory:c.conf._dir_type = None
    '''The directory instance for this project'''



    project_id:int = None
    title:str = None
    description:str = None
    project_type:str = None
    user_name:str = None
    user_email:str = None
    padded_project_count:str = None
    '''The project id with leading zeros'''

    dir_name:str = None
    '''The name of the projects directory'''

    dir_path:str = None
    '''The file path to the project folder

    .../ra9/23-1234 - project name
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
        self.main = main
        self.year = year
        self.directory = directory

        if directory is not None:
            # c.con.log("directory provided","yellow")
            dn = directory.name
            match = re.findall(r"^([0-9]{2})-([0-9]{4})\s*-?\s*(.*)",dn)
            if len(match) > 0:
                # print(f"match: {match}")
                match = match[0]
                self.padded_project_count = match[1]
                # print(f"int(match[1]):{int(match[1])}   {type(int(match[1]))}")
                self.project_id = int(match[1])
                self.title = match[2]

        if directory is None:
            self.project_id = project_id
            # @Mstep [] generate the padded project id "0046"
            self.padded_project_count = c.string.leftPad(self.project_id,4,"0")
            self.dir_name = f"{year.project_prefix}-{self.padded_project_count} - {title}"
            # c.con.log(self.dir_path,"yellow")
            self.dir_path = f"{year.dir_path}/{self.dir_name}"
            self.title = title
            self.description = description
            self.project_type = project_type




    def create_master(self):
        c.dirs.create(self.dir_path)
        self.directory = c.dirs.get_folder(self.dir_path)



    @property
    def summary(self):
        '''
            Get this ProjectBase's summary

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 11-14-2022 12:38:55
            `@memberOf`: ProjectBase
            `@property`: summary
        '''
        sum_data = {
            "project_id":self.project_id,
            "project_type":self.project_type,
            "dir_path":self.dir_path,
            "file_path":self.file_path,
            "title":self.title,
            "description":self.description,
            "timestamp":self.timestamp,
        }


        return sum_data


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
    #         self.data['type'] = value
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









