#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

#define SERVER_IP "192.168.213.129"  // 如果是容器间通信，这里填写服务器容器对应的IP地址
#define PORT 8888
#define MESSAGE "Hello, Server!"
#define MAX_BUFFER_SIZE 1024

int main() {
    // 1. 创建套接字
    int client_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (client_socket == -1) {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }

    // 2. 初始化服务器地址结构体
    struct sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    server_addr.sin_addr.s_addr = inet_addr(SERVER_IP);
    memset(server_addr.sin_zero, '\0', sizeof(server_addr.sin_zero));

    // 3. 连接服务器
    if (connect(client_socket, (struct sockaddr *)&server_addr, sizeof(server_addr)) == -1) {
        perror("Connect failed");
        close(client_socket);
        exit(EXIT_FAILURE);
    }

    // 4. 发送数据给服务器
    ssize_t bytes_sent = send(client_socket, MESSAGE, strlen(MESSAGE), 0);
    if (bytes_sent == -1) {
        perror("Send failed");
        close(client_socket);
        exit(EXIT_FAILURE);
    }
    printf("Sent to server: %s\n", MESSAGE);

    // 5. 关闭套接字
    close(client_socket);

    return 0;
}
