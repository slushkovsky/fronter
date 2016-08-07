def ask_yes_no(question, default=None):
    '''
      Ask a yes/no question via raw_input() and return their answer.

      @param  question  <str>         is a string that is presented to the user.
      @param  default   <bool, None>  Is the presumed answer if the user just hits <Enter>.
                                      It must be None for '[y/n]' (the default), 
                                      True for '[Y/n]' or 'no' for '[y/N]'

      @return <bool> True for 'yes' answer or False for 'no'
    '''

    assert(isinstance(question, str))
    assert(isinstance(default,  bool) or default is None)


    ANSWERS = {
        True:  ['yes', 'y', 'ye'],
        False: ['no', 'n']
    }

    yesno = {
        None:  'y/n', 
        True:  'Y/n',
        False: 'y/N'
    }[default]

    if not question.endswith('?'): 
        question += '?'

    while True:
        print('{question} [{yesno}]'.format(question=question, yesno=yesno))

        choice = input().lower().strip()

        if len(choice) == 0: 
            if default is not None: 
                return default
        else:
            if choice in ANSWERS[True]: 
                return True
            elif choice in ANSWERS[False]: 
                return False

        print('Please respond with:', ', '.join(ANSWERS[True] + ANSWERS[False]))
