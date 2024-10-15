import socket
import sys

def evaluate_expression(expression):
    try:
        # Evaluate the expression (e.g., "9 + 8")
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

def start_server(ip, port):
    
    try:
        # Create a TCP/IP socket for server
        #AF_INET refers to the address-family ipv4
        #SOCK_STREAM means connection-oriented TCP protocol
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the IP and port provided
        server_socket.bind((ip, port))
        print(f"Server started at {ip}:{port}")

        # Listen for incoming connections
        server_socket.listen(1)  # Only 1 connection at a time
        print("Waiting for a client to connect...")

        occupied = False  # To track if the server is occupied

        while True:
            try:
                # Accept a connection request from a client
                client_socket, client_address = server_socket.accept()

                if occupied:
                    # Server is busy, send message to the client and close connection
                    client_socket.send("Server is busy. Try again later.".encode())
                    client_socket.close()
                else:
                    # Server is available, serve the client
                    print(f"Client connected from {client_address}")
                    occupied = True
                    
                    while True:
                        # Receive data from the client
                        data = client_socket.recv(1024).decode()
                        if not data:
                            # Break if no more data is received from the client
                            break
                        print(f"Expression Received from client: {data}")
                        
                        # Evaluate the arithmetic expression
                        result = evaluate_expression(data)
                        print(f"Sending reply: {result}")

                        # Send the result back to the client
                        client_socket.send(result.encode())
                
            except Exception as e:
                print(f"Error during connection: {e}")
            
            finally:
                # Mark server as free after the client disconnects
                occupied = False
                # Close the connection after the client terminates
                client_socket.close()
                print("Client disconnected, waiting for another client...")

    except KeyboardInterrupt:
        #Handling keyboard interrupt (Ctrl+C)
        print("\nServer terminated.")
    
    except socket.error as e:
        #Handling socket errors
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        # Close the server socket before exiting
        server_socket.close()
        print("Server socket closed. Exiting...")

if __name__ == "__main__":
    #checks if there are correct number of command line arguments
    if len(sys.argv) != 3:
        print("Usage: python server1.py <IP> <PORT>")
        sys.exit(1)
    
    # Getting server IP and Port number from the command line and storing them in variables
    ip = sys.argv[1]
    port = int(sys.argv[2])

    #calling start_server function with server IP and Port number as parameters
    start_server(ip, port)
