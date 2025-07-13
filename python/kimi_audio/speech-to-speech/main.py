def client_send_handshake(audio_connection):
    print("client -sending handhsake")
    audio_connection = {"client_connection":"true"}
    return audio_connection

def server_receive_handshake(audio_connection):
    print("server-receive_handhsake")
    audio_connection_new = {"server_connection":"true"}

    audio_connection |= audio_connection_new
    return audio_connection


def client_send_audio_chunk(audio_connection):
    print("cleint send audio chunk")
    audio_connection_new = {"client_send_audio_chunk=1":"true"}

    audio_connection |= audio_connection_new
    return audio_connection



def server_receive_audio_chunk(audio_connection):
    print("server receive audio chunk")
    audio_connection_new = {"server_receive_audio_chunk=1":"true"}

    audio_connection |= audio_connection_new
    return audio_connection


def server_send_vad_commit_message(audio_connection):
    print("server_send_vad_commit_message")
    audio_connection_new = {"server_send_vad_commit_message":"true"}

    audio_connection |= audio_connection_new
    return audio_connection


def client_receive_vad_message(audio_connection):
    print("client_receive_vad_message")

    audio_connection_new = {"client_receive_vad_message":"true"}

    audio_connection |= audio_connection_new
    return audio_connection

def server_send_audio_chunk(audio_connection):
    print("server_send_audio_chunk")
    audio_connection_new = {"server_send_audio_chunk=1":"true"}

    audio_connection |= audio_connection_new
    return audio_connection

def client_receive_audio_chunk(audio_connection):
    print("client_receive_audio_chunk")

    audio_connection_new = {"client_receive_audio_chunk=1":"true"}

    audio_connection |= audio_connection_new
    return audio_connection

def server_send_finish(audio_connection):
    print("server_send_finish")
    audio_connection_new = {"server_send_finish":"true"}

    audio_connection |= audio_connection_new
    return audio_connection

def client_receive_finish(audio_connection):
    print("client_receive_finish")
    audio_connection_new = {"client_receive_finish":"true"}

    audio_connection |= audio_connection_new
    return audio_connection


def client_end_connection(audio_connection):
    print("client_end_connection")
    audio_connection_new = {"client_end_connection":"true"}

    audio_connection |= audio_connection_new
    return audio_connection

def server_end_connection(audio_connection):
    print("server_end_connection")
    audio_connection_new = {"server_end_connection":"true"}

    audio_connection |= audio_connection_new
    return audio_connection



def main():
    print("hwllo_wolrd")

    audio_connection={}

    audio_connection=client_send_handshake(audio_connection)

    print(audio_connection)
    server_receive_handshake(audio_connection)

    print(audio_connection)

    client_send_audio_chunk(audio_connection)


    print(audio_connection)

    server_receive_audio_chunk(audio_connection)

    print(audio_connection)

    client_send_audio_chunk(audio_connection)

    print(audio_connection)

    server_receive_audio_chunk(audio_connection)

    print(audio_connection)

    server_send_vad_commit_message(audio_connection)
    print(audio_connection)



    client_receive_vad_message(audio_connection)

    print(audio_connection)

    server_send_audio_chunk(audio_connection)

    print(audio_connection)

    client_receive_audio_chunk(audio_connection)

    print(audio_connection)

    server_send_audio_chunk(audio_connection)

    print(audio_connection)
    client_receive_audio_chunk(audio_connection)
    print(audio_connection)
    server_send_audio_chunk(audio_connection)
    print(audio_connection)
    client_receive_audio_chunk(audio_connection)
    print(audio_connection)

    server_send_finish(audio_connection)
    print(audio_connection)
    client_receive_finish(audio_connection)
    print(audio_connection)

    client_end_connection(audio_connection)
    print(audio_connection)

    server_end_connection(audio_connection)
    
if __name__ == "__main__":
    main()
