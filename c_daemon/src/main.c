#include "TCP_protocols.h"
#include "global_var.h"

const int BUFSIZE = 1024;
uint16_t PORT = 1234;

int maxfd;
int res;
int listenfd = 0;
int existed_player = 0;
// index of self
int ind0;
// int player_socket[PLAYER_MAX] = {0};
// char *existed_player_IP[PLAYER_MAX] = {NULL};

// envoyer la connection de python vers c = struct 3

network_info connection[PLAYER_MAX] = {0};

fd_set readfds;
struct sockaddr_in master_addr = {};

int main(int argc, char **argv) {
    char buffer[BUFSIZE];
    bzero(buffer, BUFSIZE);
    int charcnt;

    // initialiser la connection
    for (int i = 0; i < PLAYER_MAX; i++) {
        connection[i].used = 0;
        connection[i].socket = 0;
        connection[i].IP = NULL;
    }

    // char *testIP = get_my_IP();
    // printf("My IP: %s\n", ((testIP == NULL) ? "nope" : testIP));
    // return 0;

    // get own IP address
    // create another socket, addr_in for listenfd
    // and bind and listen on listenfd
    char *ip_host = get_my_IP();
    if (argc > 3) {
        ip_host = argv[3];
    }
    if ((res = create_master_socket(ip_host))) {
        fprintf(stderr, "Error number %d creating listening socket\n", res);
        return (EXIT_FAILURE);
    }

    // add host master in the connection list
    add_connection(listenfd, ip_host);

    for (int i = 0; i < PLAYER_MAX; i++) {
        if (connection[i].used) {
            ind0 = i;
            break;
        }
    }

    if (argc > 1) {
        // connect to starting IP
        PORT = ((argc > 2) ? (uint16_t)atoi(argv[2]) : PORT);
        existed_player++;

        // printf("%d %s\n", PORT, existed_player_IP[0]);
        for (int index = 0; index < PLAYER_MAX; index++) {
            if (!connection[index].used) {
                connection[index].IP = argv[1];
                if ((res = connect_existed_players(index))) {
                    fprintf(stderr, "Error number %d connecting to player #%d\n", res, index);
                }

                // get file to start the game
                if (write(connection[index].socket, "/file_transfer", strlen("/file_transfer") + 1) < 0){
                    stop("cannot send message for file transfer");
                }

                // receive file as function recv_file(connection[index].socket);
                /* start of recv_file */
                printf("IN MAIN::RECV FILE\n");

                long file_size;
                char *cmd;
                int total_bytes_read = 0;

                // create a new file in the save directory
                char cwd[BUFSIZE];
                getcwd(cwd, sizeof(cwd));
                strcat(cwd, "/Save/on_game");
                printf("\t$PWD received file: %s\n", cwd);

                FILE* fp = fopen(cwd, "w");
                if (fp == NULL) {
                    printf("Error creating file.\n");
                    return;
                }

                printf("\tstart recv_file()\n");
                int valread;

                valread = read(connection[index].socket, buffer, BUFSIZE - 1);
                cmd = strtok(buffer, " ");

                // get the file size to verify the file is sent correctly
                file_size = atoi(strtok(NULL, " "));
                printf("\tcmd in recv_file, file size = %ld\n", file_size);
                printf("\tin recv_file, total bytes read = %d\n", total_bytes_read);

                // verify if the file is received successfully before do other thing*
                while (total_bytes_read != file_size) {

                    while ((valread = read(connection[index].socket, buffer, BUFSIZE - 1)) == BUFSIZE - 1) {

                        buffer[valread] = '\0';
                        printf("\trecv buffer %d: %s\n", valread,  buffer);
                        fwrite(buffer, 1, valread, fp);
                        total_bytes_read += valread; 

                    }

                    if (valread != 0) {

                        buffer[valread] = '\0';
                        fwrite(buffer, 1, valread, fp);
                        total_bytes_read += valread; 
        
                    }
                }

                printf("\tend recv_file()\n");

                fclose(fp);

                printf("\tin recv_file out while, total bytes read = %d\n", total_bytes_read);
                if(total_bytes_read == file_size) {
                    printf("\tReceived file of %ld successfully\n", file_size);
                }
                else {
                    printf("\tReceived file of %ld unsuccessfully\n", file_size);
                    stop("not received the file to start the game successfully");
                }
                /* end of recv_file */

                // get list of other IP addresses
                if (write(connection[index].socket, "/ip_demande", strlen("/ip_demande") + 1) < 0) {
                    stop("cannot demande ip table");
                }
                
                // demand the initial state of the game
                if (write(connection[index].socket, "/init_state_demand", strlen("/init_state_demand") + 1) < 0) {
                    stop("cannot demand initial state");
                }
                

               
                        
                break;
            }
        }

    }

    print_connections();

    // while loop
    while (1) {
        // get all socket into fd set
        FD_ZERO(&readfds);
        FD_SET(listenfd, &readfds);
        maxfd = listenfd;
        FD_SET(STDIN_FILENO, &readfds);
        maxfd = max(maxfd, STDIN_FILENO);

        for (int index = 0; index < PLAYER_MAX; index++) {
            if (connection[index].socket) {
                FD_SET(connection[index].socket, &readfds);
                maxfd = max(maxfd, connection[index].socket);
            }
        }

        // ajoute le timeout !!!
        // select
        if ((res = select(maxfd + 1, &readfds, NULL, NULL, NULL)) < 0 && errno != EINTR) {
            stop("Select error");
        }

        // new player connecting
        if (FD_ISSET(listenfd, &readfds)) {
            // out of slot
            if (existed_player >= PLAYER_MAX) {
                continue;
            }

            // accept connection with new player
            unsigned int len = sizeof(master_addr);
            if ((res = accept(listenfd, (struct sockaddr *)&master_addr, &len)) < 0) {
                stop("Error accepting new player");
            }

            // Print the IP address of the new client
            char newClientIP[INET_ADDRSTRLEN];
            if (inet_ntop(AF_INET, &master_addr.sin_addr, newClientIP, sizeof(newClientIP)) != NULL) {
                printf("New player connected from %s\n", newClientIP);

                // save their socket fd
                add_connection(res, newClientIP);
                print_connections();
            } else {
                printf("Unable to retrieve the IP address of the new client\n");
            }
        } else if (FD_ISSET(STDIN_FILENO, &readfds)) {
            bzero(buffer, BUFSIZE);
            if ((charcnt = read(STDIN_FILENO, buffer, BUFSIZE - 1)) < 0) {
                stop("Standard input error");
            }
            buffer[charcnt - 1] = '\0';
            // host deconnected
            if (!strcmp(buffer, "quit")) {
                // kill all socket of connection
                for (int index = 0; index < PLAYER_MAX; index++) {
                    if (connection[index].used) {
                        const char *disconnectMsg = "A player has disconnected!\n";
                        if (write(connection[index].socket, disconnectMsg, strlen(disconnectMsg) + 1) < 0) {
                            fprintf(stderr, "Cannot send disconnecting message to player #%d\n", index);
                        }
                        close_connection(index);
                    }
                }
                break;
            }
        }
        // incoming from other players
        else {
            for (int index = 0; index < PLAYER_MAX; index++) {
                if (FD_ISSET(connection[index].socket, &readfds)) {
                    bzero(buffer, BUFSIZE);

                    // this player has disconnected
                    if ((charcnt = read(connection[index].socket, buffer, BUFSIZE)) == 0) {
                        close_connection(index);
                        print_connections();
                    } else if (charcnt < 0) {
                        stop("Error reading message");
                    }

                    // receive data from other
                    else {
                        // print received message
                        printf("Received from IP:%s socket:%d buffer:%s\n", connection[index].IP, connection[index].socket, buffer);

                        char cmd[BUFSIZE];
                        for (long unsigned int i = 0; i <= strlen(buffer); i++) {
                            if (i == strlen(buffer)) {
                                cmd[i] = '\0';
                                break;
                            }
                            if (buffer[i] == ' ' || buffer[i] == '\n' || buffer[i] == '\0') {
                                cmd[i] = '\0';
                                break;
                            }
                            cmd[i] = buffer[i];
                        }

                        // new player ask the list of player in the game
                        if (!strcmp(cmd, "/ip_demande")) {
                            printf("IN IP DEMANDE\n");

                            sprintf(buffer, "/ip_response");

                            for (int ind = 0; ind < PLAYER_MAX; ind++) {
                                if (connection[ind].used && ind != ind0 && ind != index /**/) {
                                    /*sprintf(buffer, "%s %s", buffer, connection[ind].IP);*/
                                    strcat(buffer, " ");
                                    strcat(buffer, connection[ind].IP);
                                }
                            }

                            if (write(connection[index].socket, buffer, strlen(buffer) + 1) < 0) {
                                fprintf(stderr, "\tCannot send /ip_response message to player #%d\n", index);
                            }
                        }

                        // new player receive the list of player in the game, they try co connect to all of them
                        else if (!strcmp(cmd, "/ip_response")) {
                            printf("IN IP RESPONSE\n");

                            //separate the @IP from ip_response
                            char *get_ip_buffer = strtok(buffer, " ");
                            char *get_ip_player = strtok(NULL, " ");

                            while (*get_ip_player != '\0') {
                                fprintf(stderr, "\tget_ip_player NOT NULL %s\n", get_ip_player);

                                for (int ind = 0; ind < PLAYER_MAX; ind++) {
                                    if (!connection[ind].used) {
                                        connection[ind].IP = get_ip_player;
                                        if ((res = connect_existed_players(ind))) {
                                            fprintf(stderr, "\tError number %d connecting to player #%d\n", res, ind);
                                        }
                                        break;
                                    }
                                }
                                get_ip_player = strtok(NULL, " ");
                            }

                        }
                        
                        else if (!strcmp(cmd, "/file_transfer")){
                            printf("IN FILE TRANSFER\n");
                            // send file of the current game
                            send_file_by_socket(connection[index].socket);
                        }

                        // else if (!strcmp(cmd, "/file_start")){
                        //     printf("IN FILE START\n");
                        //     recv_file(connection[index].socket);
                        // } 
                         
                        
                        else if (!strcmp(cmd, "/init_state_demand")) {
                            // get file from python
                        } 
                        
                        else {
                            printf("OTHER MESSAGE\n");
                        }
                    }
                }
            }
        }
    }

    close(listenfd);
    perror("Execution");
    return (EXIT_SUCCESS);
}
