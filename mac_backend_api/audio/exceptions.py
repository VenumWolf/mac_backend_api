class UserAlreadyLikesException(Exception):
    """Raised when adding a like to an audio the user has already liked"""

    def __init__(self):
        super(Exception, self).__init__("User already likes the audio")
