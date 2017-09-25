import skyRemote

ip=raw_input("Please enter ip address: ")
test=skyRemote.remote(ip)
typed=""
while 1:
    typed=raw_input("Please enter something: ")
    test.press(typed)