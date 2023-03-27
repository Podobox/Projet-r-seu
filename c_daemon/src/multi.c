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

int main(int argc, char *argv[]) {
    
    const int number_player = 1;
    int sock, maxfd, listenfd, connfd, nready, player_socket[number_player];
    char buff[BUFLEN], playerIP[][100] = { "192.168.68.17" };
    struct sockaddr_in other_player_addr, my_addr;

    // get the IP of the host
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

        if (connect(sock, (struct sockaddr *)&other_player_addr, sizeof(other_player_addr)) != 0) {
            stop("connect() : Unable to connect to the remote host");
            close(sock);
            continue;
        }
        else{
            player_socket[i] = sock;
        }

    }

    // set of socket descriptors
    if ((listenfd = socket(AF_INET, SOCK_STREAM, 0))== -1)
        stop("socket invalide !\n");

    my_addr.sin_family = AF_INET;
    my_addr.sin_port = htons(PORT);
    my_addr.sin_addr.s_addr = inet_addr(hostIP);

    int *len = (int *)malloc(sizeof(int));
    (*len) = sizeof(my_addr);

    fd_set readfds;
    if (bind(listenfd, (struct sockaddr *)&my_addr, sizeof(my_addr)) < 0)
        stop("bind failed");

    // Ready to listen
    if (listen(listenfd, 5) != 0)
        stop("listen failed. Error");

    perror("after listen");


    while (1) {

        // Wait for activity on any socket
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
            
            // Print the IP address of the new client
            char newClientIP[INET_ADDRSTRLEN];
            if (inet_ntop(AF_INET, &my_addr.sin_addr, newClientIP, sizeof(newClientIP)) != NULL) {
                printf("New client connected from %s\n", newClientIP);
            } else {
                printf("Unable to retrieve the IP address of the new client\n");
            }

            int clientID;
            for (int index = 0; index < number_player; index++) {
                if (player_socket[index] == 0) {
                    player_socket[index] = connfd;
                    break;
                }
            }

            printf("after recv new player");
        }   

    }

    close(listenfd);
    return 0;
}