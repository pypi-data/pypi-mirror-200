from typing import TYPE_CHECKING,TypeVar as _TypeVar


# ---------------------------------------------------------------------------- #
#                               TYPE DECLARATIONS                              #
# ---------------------------------------------------------------------------- #

main_type = None
year_type = None
project_type = None

if TYPE_CHECKING:

    from ramanager.ProjectManager import ProjectManager as _m
    main_type = _TypeVar('main_type', bound=_m)

    from ramanager.Year import Year as _InpF
    year_type = _TypeVar('year_type', bound=_InpF)

    from ramanager.Project import Project as _THZL
    project_type = _TypeVar('project_type', bound=_THZL)
