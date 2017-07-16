

class NetworkRequestFail(Exception):
    pass

class ZillowRequestError(Exception):
    """
    the error code and information returned by zillow api
    see: https://www.zillow.com/howto/api/GetZestimate.htm
    """
    def __init__(self,code,message):
        """
        :param code: should be a int, 0 means successful request 
        :param message: detail description from zillow
        """
        self.code = code
        self.message = message

    def __str__(self):
        return "Zillow Request Error: {}, {}".format(self.code,self.message)