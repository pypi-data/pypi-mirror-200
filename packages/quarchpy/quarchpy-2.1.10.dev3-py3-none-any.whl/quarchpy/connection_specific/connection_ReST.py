import logging

try:
    import httplib as httplib
except ImportError:
    import http.client as httplib

class ReSTConn:
    def __init__(self, ConnTarget):
        self.ConnTarget = ConnTarget

        self.Connection = httplib.HTTPConnection(self.ConnTarget, 80, timeout=10)
        self.Connection.close()
        
    def close(self):
        return True

    def sendCommand(self, Command, expectedResponse = True):
        Command = "/" + Command.replace(" ", "%20")
        self.Connection.request("GET", Command)
        if expectedResponse == True:
            R2 = self.Connection.getresponse()
            if R2.status == 200:
                Result = R2.read()
                Result = Result.decode()

                # Debugging to check for empty responses.
                before_flag = False
                if not Result or Result == "":
                    logging.ERROR(f"RESt response to : {Command} returned empty response prior to strip")
                    before_flag = True

                Result = Result.strip('> \t\n\r')

                # Debugging to check for empty responses
                if Result == "":
                    if not before_flag:
                        logging.ERROR(f"RESt response to : {Command} was empty after string strip ")

                self.Connection.close()
                return Result
            else:
                print ("FAIL - Please power cycle the module!")
                self.Connection.close()
                return "FAIL: ", R1.status, R1.reason
        else:
            return None