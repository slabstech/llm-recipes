def client_send_handshake():
    print("client -sending handhsake")

def server_receive_handshake():
    print("server-receive_handhsake")

def client_send_audio_chunk():
    print("cleint send audio chunk")

def server_receive_audio_chunk():
    print("server receive audio chunk")

def server_send_vad_commit_message():
    print("server_send_vad_commit_message")

def client_receive_vad_message():
    print("client_receive_vad_message")

def server_send_audio_chunk():
    print("server_send_audio_chunk")

def client_receive_audio_chunk():
    print("client_receive_audio_chunk")


def server_send_finish():
    print("server_send_finish")

def client_receive_finish():
    print("client_receive_finish")
    
def main():
    print("hwllo_wolrd")

    client_send_handshake()

    server_receive_handshake()


    client_send_audio_chunk()

    server_receive_audio_chunk()


    client_send_audio_chunk()

    server_receive_audio_chunk()

    server_send_vad_commit_message()

    client_receive_vad_message()


    server_send_audio_chunk()
    client_receive_audio_chunk()


    server_send_audio_chunk()
    client_receive_audio_chunk()
    server_send_audio_chunk()
    client_receive_audio_chunk()

    server_send_finish()
    client_receive_finish()
    
if __name__ == "__main__":
    main()
