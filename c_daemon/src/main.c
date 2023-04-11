#include "IPC.h"
#include "TCP_protocols.h"
#include "global_var.h"

const int BUFSIZE = 1024;
uint16_t PORT     = 1234;

int maxfd;
int res;
int listenfd       = 0;
int existed_player = 0;
// index of self
int ind0;
int child_pid = 0;
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
        connection[i].used   = 0;
        connection[i].socket = 0;
        connection[i].IP     = NULL;
    }

    // char *testIP = get_my_IP();
    // printf("My IP: %s\n", ((testIP == NULL) ? "nope" : testIP));
    // return 0;

    // get own IP address
    // create another socket, addr_in for listenfd
    // and bind and listen on listenfd
    char *ip_host = get_my_IP();
    if (argc > 3) {
        PORT = atoi(argv[3]);
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
                send_message message;
                message.mesg_type = -6;
                if (write(connection[index].socket, &message, sizeof(send_message)) < 0) {
                    stop("cannot send message for file transfer");
                }

                recv_file(connection[index].socket);


                // get list of other IP addresses
                message.mesg_type = -1;
                if (write(connection[index].socket, &message, sizeof(send_message)) < 0) {
                    stop("cannot demande ip table");
                }

                ////////////////////////////////////
                /// Copy the part of the code handling ip_response here
                ////////////////////////////////////
                /// I believe that what it did was sending the 3 messages in a row so
                /// fast that the other client only saw 1 of them and not the other 2
                /// I'm not sure about the explanation but at least it works
                // if ((charcnt = read(connection[index].socket, buffer, BUFSIZE)) < 0) {
                //     stop("Error reading message");
                // } else {
                //     printf("IN IP RESPONSE\n");

                //     char *get_ip_player = malloc(16);

                //     sprintf(get_ip_player, "%d.%lu.%lu.%lu", message.mes.message_type,
                //             message.mes.posx, message.mes.posy, message.mes.type);

                //     /*while (get_ip_player != NULL) {*/
                //     fprintf(stderr, "get_ip_player NOT NULL %s\n", get_ip_player);

                //     for (int ind = 0; ind < PLAYER_MAX; ind++) {
                //         if (!connection[ind].used) {
                //             connection[ind].IP = get_ip_player;
                //             if ((res = connect_existed_players(ind))) {
                //                 fprintf(stderr, "Error number %d connecting to player
                //                 #%d\n", res, ind);
                //             }
                //             break;
                //         }
                //     }
                // }
                // separate the                }
                ////////////////////////////////////

                // demand the initial state of the game
                /*send_message message;*/
                /*message.mesg_type = -2;*/
                /*if (write(connection[index].socket, &message, sizeof(send_message))
                 * < 0) {*/
                /*stop("cannot demand initial state");*/
                /*}*/
                /*if (write(connection[index].socket, "/incoming_change 1 2 3 4 5",*/
                /*strlen("/incoming_change 1 2 3 4 5") + 1)*/
                /*< 0) {*/
                /*stop("dumb dumb test");*/
                /*}*/
                /*// wait 50ms*/
                /*usleep(50000);*/
                /*if (write(connection[index].socket, "/outcoming_change 5 6 7 8 9",*/
                /*strlen("/outcoming_change 5 6 7 8 9") + 1)*/
                /*< 0) {*/
                /*stop("dumb test 2");*/
                /*}*/
                break;
            }
        }
    }

    print_connections();

    pid_t pid;

    /*signal(SIGTERM, handle_sigterm);*/

    /*atexit(handle_parent_exit);*/

    /*pid = fork();*/
    pid = 1;
    python_struct_t *recv_data;
    recv_data = (python_struct_t *)malloc(sizeof(python_struct_t));

    if (pid < 0) {
        stop("Fork failed");
    } else if (pid == 0) {
        // child recv from python
        /*child_pid = getpid();*/
        /*python_struct_t *recv_data;*/
        /*recv_data = (python_struct_t *)malloc(sizeof(python_struct_t));*/
        /*char change_msg[BUFSIZE];*/
        /*while (1) {*/
        /*recv_data = recv_from_python();*/
        /*sprintf(change_msg, "/outcoming_change %d %ld %ld %ld %ld",
         * recv_data->message_type,*/
        /*recv_data->posx, recv_data->posy, recv_data->type, recv_data->x);*/
        /*if (write(connection[ind0].socket, change_msg, strlen(change_msg) + 1) < 0)
         * {*/
        /*perror("Failed to send changes");*/
        /*}*/
        /*}*/
        ;
    } else {
        free(recv_data);
        // parent do TCP
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
            maxfd++;

            // ajoute le timeout !!!
            // select
            // timeval of 1ms
            struct timeval tv;
            tv.tv_sec  = 0;
            tv.tv_usec = 1000;
            if ((res = select(maxfd + 1, &readfds, NULL, NULL, &tv)) < 0 && errno != EINTR) {
                stop("select");
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
                char buffer[BUFSIZE];
                bzero(buffer, BUFSIZE);
                int charcnt;
                send_message message;
                if ((charcnt = read(STDIN_FILENO, &message, sizeof(message))) < 0) {
                    stop("Standard input error");
                }
                buffer[charcnt - 1] = '\0';
                // host deconnected
                /*if (!strcmp(buffer, "quit")) {*/
                if (message.mesg_type == -3) {
                    // kill all socket of connection
                    for (int index = 0; index < PLAYER_MAX; index++) {
                        if (connection[index].used) {
                            const char *disconnectMsg = "A player has "
                                                        "disconnected!\n";
                            if (write(connection[index].socket, disconnectMsg, strlen(disconnectMsg) + 1)
                                < 0) {
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
                        char buffer[BUFSIZE];
                        int charcnt;
                        bzero(buffer, BUFSIZE);
                        send_message message;

                        // this player has disconnected
                        if ((charcnt = recv(connection[index].socket, &message,
                                            sizeof(send_message), MSG_DONTWAIT))
                            == 0) {
                            close_connection(index);
                            print_connections();
                        } else if (charcnt < 0) {
                            break;
                        }

                        // receive data from other
                        else {
                            // print received message
                            printf("Received %li from IP:%s socket:%d buffer:%i %lu "
                                   "%lu "
                                   "%lu %lu\n",
                                   message.mesg_type, connection[index].IP,
                                   connection[index].socket, message.mes.message_type,
                                   message.mes.posx, message.mes.posy, message.mes.type,
                                   message.mes.x);

                            /*char cmd[BUFSIZE];*/
                            /*for (unsigned long int i = 0; i <= strlen(buffer); i++)
                             * {*/
                            /*if (i == strlen(buffer)) {*/
                            /*cmd[i] = '\0';*/
                            /*break;*/
                            /*}*/
                            /*if (buffer[i] == ' ' || buffer[i] == '\n' || buffer[i]
                             * == '\0') {*/
                            /*cmd[i] = '\0';*/
                            /*break;*/
                            /*}*/
                            /*cmd[i] = buffer[i];*/
                            /*}*/

                            // new player ask the list of player in the game
                            if (message.mesg_type == -1) {
                                printf("IN IP DEMANDE\n");

                                /*sprintf(buffer, "/ip_response");*/

                                for (int ind = 0; ind < PLAYER_MAX; ind++) {
                                    if (connection[ind].used && ind != ind0 && ind != index /**/) {
                                        send_message message;
                                        message.mesg_type = -4;
                                        sscanf(connection[ind].IP, "%d.%ld.%ld.%ld",
                                               &message.mes.message_type, &message.mes.posx,
                                               &message.mes.posy, &message.mes.type);
                                        printf("sending connection %s to %s\n",
                                               connection[ind].IP, connection[index].IP);
                                        /*printf("Sending:%i %lu "*/
                                        /*"%lu "*/
                                        /*"%lu %lu\n",*/
                                        /*message.mes.message_type,*/
                                        /*message.mes.posx, message.mes.posy,
                                         * message.mes.type,*/
                                        /*message.mes.x);*/
                                        if (write(connection[index].socket, &message, sizeof(send_message))
                                            < 0) {
                                            fprintf(stderr,
                                                    "Cannot send /ip_response "
                                                    "message to player #%d\n",
                                                    index);
                                        }
                                        /*sprintf(buffer, "%s %s", buffer,
                                         * connection[ind].IP);*/
                                        /*strcat(buffer, " ");*/
                                        /*strcat(buffer, connection[ind].IP);*/
                                    }
                                }
                                message.mesg_type = -100;
                                if (write(connection[index].socket, &message, sizeof(send_message)) < 0) {
                                    fprintf(stderr,
                                            "Cannot send /ip_response "
                                            "message to player #%d\n",
                                            index);
                                }

                                // new player receive the list of player in the game, they
                                // try co connect to all of them
                                else if (message.mesg_type == -4) {
                                    printf("IN IP RESPONSE\n");

                                    // separate the @IP from ip_response
                                    /*char *get_ip_buffer = strtok(buffer, " ");*/
                                    /*char *get_ip_player = strtok(NULL, " ");*/

                                    char *get_ip_player = malloc(16);

                                    sprintf(get_ip_player, "%d.%lu.%lu.%lu",
                                            message.mes.message_type, message.mes.posx,
                                            message.mes.posy, message.mes.type);

                                    /*while (get_ip_player != NULL) {*/
                                    fprintf(stderr, "get_ip_player NOT NULL %s\n", get_ip_player);

                                    for (int ind = 0; ind < PLAYER_MAX; ind++) {
                                        if (!connection[ind].used) {
                                            connection[ind].IP = get_ip_player;
                                            if ((res = connect_existed_players(ind))) {
                                                fprintf(stderr, "Error number %d connecting to player #%d\n",
                                                        res, ind);
                                            }
                                            break;
                                        }
                                    }
                                    print_connections();
                                    /*get_ip_player = strtok(NULL, " ");*/
                                    /*}*/
                                } else if (message.mesg_type == -5) {
                                    // they send us a change in game, send this to python
                                    send_from_c(message.mes.message_type,
                                                message.mes.posx, message.mes.posy,
                                                message.mes.type, message.mes.x);
                                    // perror("Freaking bruh");
                                    /*char *data;*/
                                    /*data = (buffer + strlen(cmd) + 1);*/
                                    /*int32_t msg_type;*/
                                    /*uint64_t posx, posy, type, x;*/
                                    /*if (sscanf(data, "%d %ld %ld %ld %ld", &msg_type,*/
                                    /*&posx, &posy, &type, &x)) {*/
                                    /*printf("Receiving: %d %ld %ld %ld %ld\n",*/
                                    /*msg_type, posx, posy, type, x);*/
                                    /*send_from_c(msg_type, posx, posy, type, x);*/
                                    /*} else {*/
                                    /*perror("Invalid input or something wrong");*/
                                    /*}*/
                                } /* else if (!strcmp(cmd, "/outcoming_change")) {
                                     // we are sending a change
                                     char msg[BUFSIZE];
                                     sprintf(msg, "/incoming_change ");
                                     char *data;
                                     data = (buffer + strlen(cmd) + 1);
                                     strcat(msg, data);
                                     // send msg to all others
                                     for (int ind = 0; ind < PLAYER_MAX; ind++) {
                                         if (ind != ind0 && connection[ind].used) {
                                             if (write(connection[ind].socket, msg,
                                 strlen(msg) + 1) < 0) { stop("Cannot send changes to
                                 other " "players");
                                             }
                                         }
                                     }
                                 }*/
                                else if (message.mesg_type == -6) {
                                    printf("IN FILE TRANSFER\n");
                                    // send file of the current game
                                    send_file_by_socket(connection[index].socket);
                                } else {
                                    printf("OTHER MESSAGE\n");
                                }
                            }
                        }
                    }
                }
                char change_msg[BUFSIZE];
                recv_data = recv_from_python();
                /*printf("recv_from_python: %p\n", recv_data);*/
                if (recv_data == NULL)
                    continue;
                sprintf(change_msg, "/outcoming_change %d %ld %ld %ld %ld", recv_data->message_type,
                        recv_data->posx, recv_data->posy, recv_data->type, recv_data->x);
                printf("%s\n", change_msg);
                send_message message;
                message.mesg_type        = -5;
                message.mes.message_type = recv_data->message_type;
                message.mes.posx         = recv_data->posx;
                message.mes.posy         = recv_data->posy;
                message.mes.x            = recv_data->x;
                message.mes.type         = recv_data->type;
                for (int ind = 0; ind < PLAYER_MAX; ind++) {
                    if (connection[ind].used && ind != ind0) {
                        printf("sending to %i\n", connection[ind].socket);
                        // send_message message;
                        // message.mesg_type        = C_TO_PY;
                        // message.mes.message_type = recv_data->message_type;
                        // message.mes.posx         = recv_data->posx;
                        // message.mes.posy         = recv_data->posy;
                        // message.mes.type         = recv_data->type;
                        // message.mes.x            = recv_data->x;
                        if (write(connection[ind].socket, &message, sizeof(send_message)) < 0) {
                            stop("Cannot forward message");
                        }
                    }
                }
                /*if (write(connection[ind0].socket, change_msg, strlen(change_msg) + 1) <
                 * 0) {*/
                /*perror("Failed to send changes");*/
                /*}*/
            }
            close(listenfd);
            perror("Execution");
            exit(EXIT_SUCCESS);
        }
        close(listenfd);
        perror("Execution");
        exit(EXIT_SUCCESS);
    }
