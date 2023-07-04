import socket

s = socket.socket()

try:
    host = input("Enter Server IP: ")
    port = input("Enter Server Port: ")
    sock_addr = (host, int(port))

    try:
        s.connect(sock_addr)
    except socket.error as e:
        print("Couldn't connect to the socket:", e)
        exit(1)
    c=1
    while True:
        try:
            data = s.recv(1024).decode()
            if len(data) < 1 or data == 'done':
                break
            print(data)

            u_input = input('>>>>')
            
            while True:
                if c==1 and u_input.isdigit():
                    break
                if c==2 and not u_input.isdigit():
                    break
                if  c>2 and u_input in ['a', 'b', 'c', 'd', 'done']:
                    break
                else:
                    u_input = input('>>>>')
            c+=1   
            s.send(u_input.encode())
        except socket.error as e:
            print('An error occurred while receiving/sending data:', e)
            break

except KeyboardInterrupt:
    print("Client is terminated by the user.")

finally:
    s.close()
