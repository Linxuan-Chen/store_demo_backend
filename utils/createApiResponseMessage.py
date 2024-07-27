def createApiResponseMessage(message: str):
    """Create api response message
    
    This method converts a pure literal to a dict which contains the message literal as a key value pair.

    Args:
        message (str): message content

    Returns:
        { 'details': message }
    """
    return { 'details': message }