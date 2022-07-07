import socket as DNS
import sys 
import time

def domain_access():
        inputs = open("PROJI-HNS.txt", "r")
        queries = inputs.read().splitlines()
        inputs.close()
	outputs = open("RESOLVED.txt", "w+")
	
	socket = DNS.socket(DNS.AF_INET, DNS.SOCK_STREAM)
        print "[CLIENT]: Establishing RS Connection!"
	socket.connect((DNS.gethostbyname(sys.argv[1]) , int(sys.argv[2])))
        ts_hostname = socket.recv(4096).decode("utf-8")
        print "[CLIENT]: Top-Level Backup Hostname is: " + ts_hostname
	for query in queries:
                time.sleep(1.5) # Helps slow down the access process, avoids bugs.
                print "\n"
                print "[CLIENT]: Current Query: " + query
		socket.send(query.encode("utf-8"))
		response = socket.recv(4096).decode("utf-8")
		response_parsed = response.split()
		flag = response_parsed[2]

		if flag == "A":
                    print "[CLIENT]: Query Found in RS. Server response: " + str(response)
		    outputs.write(response + str("\n"))
		elif flag == "NS":
                    new_socket = DNS.socket(DNS.AF_INET, DNS.SOCK_STREAM)
                    print "[CLIENT]: Not found in RS. Looking in TS!"
                    new_socket.connect((DNS.gethostbyname(ts_hostname), int(sys.argv[3])))
                    new_socket.send(query.encode('utf-8'))
                    new_response = new_socket.recv(4096).decode('utf-8')
                    new_response_parsed = new_response.split()
                    new_flag = new_response_parsed[2]
                    if new_flag == "A":
                        print "[CLIENT]: Query Found in TS. Server response: " + str(new_response)
                    elif new_flag == "Error:HOST":
                        print "[CLIENT]: Query Not Found in TS. Server error response: " + str(new_response)
                    new_socket.close()
                    outputs.write(new_response + str("\n"))

	socket.send("close".encode('utf-8'))
	socket.close()	
	outputs.close()
	exit()
	return

domain_access()
