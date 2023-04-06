#ifndef GLOBAL_VAR_H
#define GLOBAL_VAR_H

#include <arpa/inet.h>
#include <errno.h>
#include <netdb.h>
#include <netinet/in.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/select.h>
#include <unistd.h>

#define max(a, b) ((a > b) ? a : b)
#define PLAYER_MAX 10

extern const int BUFSIZE;
extern uint16_t PORT;

extern int listenfd;
// extern int player_socket[PLAYER_MAX];

typedef struct {
    int used;
    int socket;
    char *IP;
} network_info;

extern network_info connection[PLAYER_MAX];

extern int existed_player;

extern struct sockaddr_in master_addr;

#endif