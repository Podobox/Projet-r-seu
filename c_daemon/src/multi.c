#include <arpa/inet.h>
#include <errno.h>
#include <fcntl.h>
#include <netdb.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>
#include "controller.h"

#define BUFLEN 1024  // Buffer length
#define PORT 1234
#define max(a, b) ((a > b) ? a : b)

int main(int argc, char *argv[]) {
  
    int sock, maxfd, connfd, nready;
    char buff[BUFLEN];
    struct sockaddr_in other_player_addr, my_addr;
    const int number_player = 1;
    char playerIP[][100] = { "192.168.68.17"};
    int player_socket[number_player];

    char *hostIP = gethostIP();

    // connect to all players connected
    for (int i = 0; i < number_player; i++) {
        // create socket
        sock = socket(AF_INET, SOCK_STREAM, 0);
        if (sock == -1)
            stop("socket invalide !\n");

        other_player_addr.sin_family = AF_INET;
        other_player_addr.sin_port = htons(PORT);
        other_player_addr.sin_addr.s_addr = inet_addr(playerIP[i]);
 
        printf("Trying %s...\n", inet_ntoa(other_player_addr.sin_addr));

        perror("before connect");

        if (connect(sock, (struct sockaddr *)&other_player_addr, sizeof(other_player_addr)) != 0) {
            stop("connect() : Unable to connect to the remote host");
            close(sock);
        }
           
    }

    // set of socket descriptors
    int listenfd = socket(AF_INET, SOCK_STREAM, 0);
    if (listenfd == -1)
        stop("socket invalide !\n");

    perror("ok");

    my_addr.sin_family = AF_INET;
    my_addr.sin_port = htons(PORT);
    my_addr.sin_addr.s_addr = hostIP;

    perror("ok");

    int *len = (int *)malloc(sizeof(int));
    (*len) = sizeof(my_addr);

    fd_set readfds;
    if (bind(listenfd, (struct sockaddr *)&my_addr, sizeof(my_addr)) < 0)
        stop("bind failed");

    perror("ok");

    // Ready to listen
    if (listen(listenfd, 5) != 0)
        stop("listen failed. Error");

    perror("ok");
    // printf("listen");

    while (1) {
        FD_ZERO(&readfds);
        FD_SET(STDIN_FILENO, &readfds);
        FD_SET(listenfd, &readfds);
        maxfd = listenfd;
        maxfd = max(maxfd, STDIN_FILENO);

        for (int i = 0; i < number_player; i++) {
            if (player_socket[i] > 0) {
                FD_SET(player_socket[i], &readfds);
            }
            maxfd = max(maxfd, player_socket[i]);
        }

        perror("select test");
        if (((nready = select(maxfd + 1, &readfds, NULL, NULL, NULL)) < 0) && errno != EINTR) {
            stop("Select Error\n");
        }

        // new player incoming
        if (FD_ISSET(listenfd, &readfds)) {
            if ((connfd = accept(listenfd, (struct sockaddr *)&my_addr, len)) < 0) {
                stop("Cannot connect to this client!");
            }
            perror("new player joined");
            int clientID;
            for (int index = 0; index < number_player; index++) {
                if (player_socket[index] == 0) {
                    player_socket[index] = connfd;
                    break;
                }
            }

            printf("after recv new player");
        } else {
            
        }
    }

    close(sock);
    return 0;
}