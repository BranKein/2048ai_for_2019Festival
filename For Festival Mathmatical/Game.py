import puzzle
import socket

def Upload(School, Name, Score, ifWin):
    print("ChiHo will upload the datas")
    HOST='jinsanplus.net'
    PORT=1636
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    # 지정한 HOST와 PORT를 사용하여 서버에 접속합니다. 
    client_socket.connect((HOST, PORT))
    temp=School+" "+Name+" "+str(Score)+" "
    # 메시지를 전송합니다. 
    client_socket.sendall(temp.encode())

    # 메시지를 수신합니다. 
    data = client_socket.recv(1024)
    print('Received', repr(data.decode()))

    # 소켓을 닫습니다.
    client_socket.close()


def main():
    School = "None"
    Name = "None"
    Score = 0
    ifWin = False

    School = input("Please enter your school name : ")
    Name = input("Please enter your name : ")
    print("Let's play 2048!")
    
    gamegrid = puzzle.puzzle()

    done = True

    while done:
        if(gamegrid.ifgameset()):
            Score = gamegrid.GetScore()
            ifWin = gamegrid.ifwintoai()
            Upload(School, Name, Score, ifWin)
            done = False


if __name__ == "__main__":
    main()
