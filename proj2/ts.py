import socket as DNS
import sys
import threading

def domain_name_system():
        dns_file = open("PROJI-DNSTS.txt", "r")
        lines = dns_file.read().splitlines()
        dns_file.close()
        ts_hashtable = {}
        for line in lines:
            line_parsed = line.split()
            hostname = line_parsed[0].strip().lower()
            flag = line_parsed[2]
            if flag == "A":
                ts_hashtable[hostname] = line.strip()

	socket = DNS.socket(DNS.AF_INET, DNS.SOCK_STREAM)
        print "[TOP LEVEL DNS]: Top Level DNS socket established successfully!"
	server_binding = ("", int(sys.argv[1]))
	socket.bind(server_binding)
	socket.listen(10)
        print "[TOP LEVEL DNS]: Listening for connections..."

        while True:
            connection, address = socket.accept()
            print "[TOP LEVEL DNS]: Establihed connection with: ", address
            thread = threading.Thread(name='thread_connect', target=thread_connect, args=(connection, ts_hashtable))
            thread.start()
	socket.close()
	return 

def thread_connect(connection, ts_hashtable):
	query = connection.recv(4096).decode('utf-8').strip().lower()
	if query in ts_hashtable:
		response = ts_hashtable[query]
                print "[TOP LEVEL DNS]: Query '" + query + "' found: " + response 
		connection.send(response.encode('utf-8'))
	else:
		error = query + " - Error:HOST NOT FOUND"
                print "[TOP LEVEL DNS]: Query '" + query + "' not found. Error response: " + error
		connection.send(error.encode('utf-8'))
	connection.close()
	exit()
	return 

domain_name_system()
