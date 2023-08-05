class InvalidImageException(Exception):
    '''
    Raised when either the magic or the load address of the
    provided image are invalid.
    '''
    pass

class NoPatchesFoundException(Exception):
    '''
    Raised when no patches are found for the provided image.
    '''
    pass

class InvalidPatchFileException(Exception):
    '''
    Raised when the provided patch file is invalid.
    '''
    pass