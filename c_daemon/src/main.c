#include "TCP_protocols.h"
#include "global_var.h"

const int BUFSIZE = 1024;
uint16_t PORT = 1234;

int maxfd;
int res;
int listenfd = 0;
int connected_player = 0;
int existed_player = 0;
int player_socket[PLAYER_MAX] = {0};
char *existed_player_IP[PLAYER_MAX] = {NULL};

fd_set readfds;
struct sockaddr_in master_addr = {};

int main(int argc, char **argv) {
    // get own IP address
    // create another socket, addr_in for listenfd
    // and bind and listen on listenfd
    char *ip_host = gethostIP();
    if ((res = create_master_socket(ip_host))) {
        fprintf(stderr, "Error number %d creating listening socket\n", res);
        return (EXIT_FAILURE);
    }

    if (argc > 1) {
        // connect to starting IP
        existed_player_IP[0] = argv[1];
        PORT = ((argc > 2) ? (uint16_t)atoi(argv[2]) : PORT);
        existed_player++;
        // printf("%d %s\n", PORT, existed_player_IP[0]);
        if ((res = connect_existed_players(0))) {
            fprintf(stderr, "Error number %d connecting to player #0\n", res);
        }

        // get list of other IP addresses
        
        // for each connected IP, create socket, initialise addr_in
        // and connect to them and save their socket
        for (int index = 1; index < existed_player; index++) {
            if ((res = connect_existed_players(index))) {
                fprintf(stderr, "Error number %d connecting to player #%d\n", res, index);
            }
        }
    }

    // while loop
    while (1) {
        
        // get all socket into fd set
        FD_ZERO(&readfds);
        FD_SET(listenfd, &readfds);
        maxfd = listenfd;
        FD_SET(STDIN_FILENO, &readfds);
        maxfd = max(maxfd, STDIN_FILENO);

        for (int index = 0; index < PLAYER_MAX; index++) {
            if (player_socket[index]) {
                FD_SET(player_socket[index], &readfds);
                maxfd = max(maxfd, player_socket[index]);
            }
        }

        // select
        if ((res = select(maxfd + 1, &readfds, NULL, NULL, NULL)) < 0 && errno != EINTR) {
            stop("Select error");
        }

        // new player connecting
        if (FD_ISSET(listenfd, &readfds)) {
            // out of slot
            if (connected_player >= PLAYER_MAX) {
                continue;
            }

            // accept connection with new player
            int len = sizeof(master_addr);
            if ((res = accept(listenfd, (struct sockaddr *)&master_addr, &len)) < 0) {
                stop("Error accepting new player");
            }
            printf("A new player has joined\n");

            // save their socket fd
            for (int index = 0; index < PLAYER_MAX; index++) {
                if (player_socket[index] == 0) {
                    player_socket[index] = res;
                    connected_player++;
                    break;
                }
            }
        } else if (FD_ISSET(STDIN_FILENO, &readfds)) {
            char buffer[BUFSIZE];
            bzero(buffer, BUFSIZE);
            int charcnt;
            if ((charcnt = read(STDIN_FILENO, buffer, BUFSIZE - 1)) < 0) {
                stop("Standard input error");
            }
            buffer[charcnt - 1] = '\0';
            // we are deconnecting
            if (!strcmp(buffer, "quit")) {
                // kill all socket of connection
                for (int index = 0; index < PLAYER_MAX; index++) {
                    if (player_socket[index]) {
                        const char *disconnectMsg = "A player has disconnected!\n";
                        if (write(player_socket[index], disconnectMsg, strlen(disconnectMsg) + 1) < 0) {
                            fprintf(stderr, "Cannot send disconnecting message to player #%d\n", index);
                        }
                        close(player_socket[index]);
                        player_socket[index] = 0;
                    }
                }
                break;
            }
        }
        // incoming from other players
        else {
            for (int index = 0; index < PLAYER_MAX; index++) {
                if (FD_ISSET(player_socket[index], &readfds)) {
                    char buffer[BUFSIZE];
                    int charcnt;
                    bzero(buffer, BUFSIZE);
                    // this player has disconnected
                    if ((charcnt = read(player_socket[index], buffer, BUFSIZE)) == 0) {
                        close(player_socket[index]);
                        player_socket[index] = 0;
                        printf("A player has disconnected\n");
                    } else if (charcnt < 0) {
                        stop("Error reading message");
                    }
                    // receive data from other
                    else {
                    }
                }
            }
        }
    }

    close(listenfd);
    perror("Execution");
    return (EXIT_SUCCESS);
}