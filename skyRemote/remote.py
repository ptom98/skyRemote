import time, math, socket, struct, time
from array import array

#sky q port 5900

class remote:
    commands={"power": 0, "select": 1, "backup": 2, "dismiss": 2, "channelup": 6, "channeldown": 7, "interactive": 8, "sidebar": 8, "help": 9, "services": 10, "search": 10, "tvguide": 11, "home": 11, "i": 14, "text": 15,  "up": 16, "down": 17, "left": 18, "right": 19, "red": 32, "green": 33, "yellow": 34, "blue": 35, 0: 48, 1: 49, 2: 50, 3: 51, 4: 52, 5: 53, 6: 54, 7: 55, 8: 56, 9: 57, "play": 64, "pause": 65, "stop": 66, "record": 67, "fastforward": 69, "rewind": 71, "boxoffice": 240, "sky": 241}
    connectTimeout = 1000;
    
    def __init__(self, ip, port=49160):
        self.ip=ip
        self.port=port
        
    def showCommands(self):
        for command, value in self.commands.iteritems():
            print str(command)+ " : "+str(value) 
            
    def getCommand(self, code):
        try:
            return self.commands[code]
        except:
            print "Error: command '"+code+"' is not valid"
            return False
          
    def press (self, sequence):
        if isinstance(sequence, list):
            for item in sequence:
                toSend=self.getCommand(item)
                if toSend:
                    self.sendCommand(toSend)
                    time.sleep(0.5)
                    
        else:
            toSend=self.getCommand(sequence)
            if toSend:
                self.sendCommand(toSend)    
    
    def sendCommand(self, code):
        commandBytes = array('l', [4,1,0,0,0,0, int(math.floor(224 + (code/16))), code % 16])
        
        try:
            client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, msg:
            print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
            return
            
        try:
            client.connect((self.ip, self.port))
        except:
            print "Failed to connect to client"
            return
        
        l=12
        timeout=time.time()+self.connectTimeout
        
        while 1:
            data=client.recv(24)
            data=data
            
            if len(data)<24:
                client.sendall(data[0:l])
                l=1
            else:
                client.sendall(buffer(commandBytes))
                commandBytes[1]=0
                client.sendall(buffer(commandBytes))
                client.close()
                break

            if time.time() > timeout:
                print "timeout error"
                break