
import colemen_utils as c
objUtils = c.obj


def get_input(prompt='',**kwargs):
    '''
        Get the user's input.
        This method can be escaped if the user presses ctrl+c

        ----------

        Arguments
        -------------------------
        `prompt` {string} The prompt to show before the input


        Return {any}
        ----------------------
        The value entered by the user or False if they press ctrl+c

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03-10-2022 09:09:01
        `memberOf`: inputs
        `version`: 1.0
        `method_name`: get_input
        # xxx [03\10\2022 09:10:16]: documentation for get_input
    '''
    
    # required = objUtils.get_kwarg(['required'], False, (bool), **kwargs)
    # clear_line_after = objUtils.get_kwarg(['clear line after','clear after'], True, (bool), **kwargs)
    default = objUtils.get_kwarg(['default'], None, None, **kwargs)
    options = objUtils.get_kwarg(['options'], None, (list), **kwargs)
    try:
        iv = input(prompt)
        if len(iv) == 0:
            return default
        if options is not None:
            option_result = _is_valid_option(iv,options)
            if option_result is False:
                print(f"Must be one of these options: {options}")
                return get_input(prompt,default=default,options=options)
            else:
                return option_result

        return iv
    except KeyboardInterrupt:
        return "__ESCAPE_KEY__"

def _is_valid_option(iv,options):
    for opt in options:
        if isinstance(opt,(str)):
            if iv == opt:
                return opt
            
        if isinstance(opt,(int)):
            if int(iv) == opt:
                return opt
            
        if isinstance(opt,(float)):
            if float(iv) == opt:
                return opt
    return False

def getuser_confirmation(prompt):
    '''
        Get a confirmation from the user.

        ----------

        Arguments
        -------------------------
        `prompt` {string} The prompt to show before the input

        Return {boolean}
        ----------------------
        True if the user enters a synonym of yes, False otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03-10-2022 09:10:25
        `memberOf`: inputs
        `version`: 1.0
        `method_name`: getuser_confirmation
        # xxx [03\10\2022 09:11:54]: documentation for getuser_confirmation.
    '''
    result = get_input(prompt)
    if result in ['y','yes','ye','yup','yep','correct','indeed','affirmative','true','sure']:
        return True
    return False

def required_cycle(prompt='',options=None):
    ready = False
    while ready is False:
        iv = get_input(prompt)
        if iv is False:
            return False
        if len(iv) > 0:
            if options is not None:
                if iv in options:
                    ready = True
                    return iv
                else:
                    print(f"Must be one of these options: {options}")
            else:
                ready = True
                return iv
        else:
            print("This is required.\n")




