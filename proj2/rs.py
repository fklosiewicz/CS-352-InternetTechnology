
import socket as DNS
import sys
import threading


def domain_name_system():
        dns_file = open("PROJI-DNSRS.txt", "r")
        lines = dns_file.read().splitlines()
        dns_file.close()
        rs_hashtable = {}
        ts_flag = ""
        for line in lines:
            line_parsed = line.split()
            hostname = line_parsed[0].strip().lower()
            flag = line_parsed[2]
            if flag == "A":
                rs_hashtable[hostname] = line.strip()
            elif flag == "NS":
                ts_flag = line.strip()

	socket = DNS.socket(DNS.AF_INET, DNS.SOCK_STREAM)
        print "[ROOT DNS]: Root DNS socket established successfully!"
        hostname = DNS.gethostname()
        ip = DNS.gethostbyname(hostname)
        print "[ROOT DNS]: Hostname: " + hostname + "  IP: " + ip
        print "[ROOT DNS]: TS Hostname (above RS): " + str(sys.argv[2])
	server_binding = ("", int(sys.argv[1]))
	socket.bind(server_binding)
	socket.listen(10)
        print "[ROOT DNS]: Listening for connections..."
        while True:
            connection, address = socket.accept()
            print "[ROOT DNS]: Established connection with: ", address
            ts_host = str(sys.argv[2])
            connection.send(ts_host.encode('utf-8'))
            thread = threading.Thread(name='thread_connect', target=thread_connect, args=(connection, rs_hashtable, ts_flag))
            thread.start()
	socket.close()
	return 


def thread_connect(connection, rs_hashtable, ts_flag):
	while True:
		query = connection.recv(4096).decode('utf-8').strip().lower()
		if query in rs_hashtable:
			response = rs_hashtable[query]
                        print "[ROOT DNS]: Query '"+ query +"' found: " + response 
			connection.send(response.encode('utf-8'))
		elif query == "close":
			break
		else:
                        print "[ROOT DNS]: Query '" + query +"' not found. Attempting TS!"
			connection.send(ts_flag.encode('utf-8'))
	connection.close()
	return 

domain_name_system()
