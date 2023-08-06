# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

import colemen_utils as c
import ra_manager.settings as _settings



class Main:
    def __init__(self):
        self.settings = {}
        self.data = {}
        # self.set_defaults()

    # def set_defaults(self):
    #     self.settings = c.file.import_project_settings("ra_manager.settings.json")

    def master(self):
        print("master")


if __name__ == '__main__':
    m = Main()
    m.master()

