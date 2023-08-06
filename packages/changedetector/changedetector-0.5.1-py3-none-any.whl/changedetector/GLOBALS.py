class VARS:
    _verbose = False

    def set_verbose(value: bool):
        VARS._verbose = value

    @property
    def verbose():
        return VARS._verbose
