import struct

#   Networking setup

SERVER_IP = "127.0.0.1"
SERVER_PORT = 7831

#   Header length (bytes)

HEADER_MESSAGE_LENGTH = 4
HEADER_SENDER_LENGTH = 10
HEADER_LENGTH = HEADER_SENDER_LENGTH + HEADER_MESSAGE_LENGTH

#   Header contents:
#       Message length          -> 4 bytes
#       Sender                  -> 10 bytes


#   Message handling

def getMessage(client):
    #   Get header
    header = client.recv(HEADER_LENGTH)

    #   Extract message length and flag
    message_length_bytes, sender = struct.unpack(f'I{HEADER_SENDER_LENGTH}s', header)

    sender_decoded = sender.rstrip(b'\x00').decode('ascii')

    #   Get message
    message = client.recv(message_length_bytes).decode('ascii')
    
    

    return message, sender_decoded

def sendMessage(client, message, sender = "NULL"):
    #   Build header
    
    header = struct.pack(f'I{HEADER_SENDER_LENGTH}s', len(message), sender.encode('ascii'))

    #   Send header
    client.send(header)
    
    #   Send message
    client.send(message.encode('ascii'))

    
    

