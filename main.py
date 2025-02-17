import socket
import threading


def handle_client(client_socket, address):
    print(f"[+] 연결됨: {address}")
    # Telnet 클라이언트에 환영 메시지 전송 (CRLF 사용)
    client_socket.send(b"Welcome to the Echo Telnet Server!\r\n")
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break  # 클라이언트 연결 종료
            print(f"[{address}] 받은 데이터: {data.decode('utf-8', 'ignore').strip()}")
            # 받은 데이터를 그대로 echo
            client_socket.sendall(data)
    except ConnectionResetError:
        print(f"[-] 연결 끊김: {address}")
    finally:
        client_socket.close()
        print(f"[*] 연결 종료: {address}")


def main():
    host = "0.0.0.0"
    port = 2323  # 일반 사용자 권한에서 실행하기 위해 비권한 포트 사용 (Telnet 기본 포트는 23)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"[*] 서버가 {host}:{port} 에서 대기 중...")

    try:
        while True:
            client_socket, addr = server.accept()
            client_thread = threading.Thread(
                target=handle_client, args=(client_socket, addr)
            )
            client_thread.daemon = True  # 메인 스레드 종료 시 함께 종료
            client_thread.start()
    except KeyboardInterrupt:
        print("\n[!] 서버 종료")
    finally:
        server.close()


if __name__ == "__main__":
    main()
