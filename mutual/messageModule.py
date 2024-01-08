import struct

#   Header length (bytes)

HEADER_LENGTH = 5
HEADER_MESSAGE_LENGTH = 4
CLIENT_TO_CLIENT_FLAG = 1

#   Header contents:
#       Message length          -> 4 bytes
#       Client to client flag   -> 1 byte


#   Message handling

def getMessage(client):
    #   Get header
    header = client.recv(HEADER_LENGTH)

    #   Extract message length and flag
    message_length_bytes, client_to_client_flag = struct.unpack('I?', header)

    #   Get message
    message = client.recv(message_length_bytes).decode('ascii')

    #   Flag = True :: Message from client
    #   Flag = false :: Message from server

    if client_to_client_flag:
        return message, True
    else:
        return message, False

def sendMessage(client, message, clientToClient = False):
    #   Build header
    header = struct.pack('I?', len(message), clientToClient)

    #   Send header
    client.send(header)
    
    #   Send message
    client.send(message.encode('ascii'))

