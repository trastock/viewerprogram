import socket
import datetime
import select
#from interruptingcow import timeout 


def data_setup():
    HOST = "localhost"
    PORT = 4000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((HOST, PORT))
        return s
    except ConnectionRefusedError:
        print("Connection refused." + 
              "Please make sure the server is " + 
              "running and listening on the specified host and port.")
         

def update_data(s : socket.socket, outdata : dict):
    data_types = ["_REAMAIN", "_SHOT", "_TOTL", "_PRST", 
                  "_STAT", "_NAME", "_SHID", "_SHPR", 
                  "_SNAT", "_GRPH", "_TEAM", "_PRCH", 
                  "_SUBT", "_DIAG"]
    
    if not outdata:
        outdata = {}
        for data_type in data_types:
            outdata[data_type] = []
    try:
        while True:
            ready_to_read, ready_to_write, in_error = select.select([s], [], [], 2)
            if ready_to_read: 
                data = repr(s.recv(1024))
                lst = data.split("\\r\\n")
                for element in lst:
                    for data_type in data_types:
                        if data_type in element:
                            outdata[data_type].append(element.split(";"))
                            break
                        else: # if for loop completes without finding data_type, append to _REAMAIN
                            outdata["_REAMAIN"].append(element.split(";"))
                return outdata
            else:
                print("Timeout")
                return None
                break
    except Exception as e:
        print(f"An error occurred while reading from socket {e}")
        
     #   print("didn't finish within 5 seconds")
    
    
    

