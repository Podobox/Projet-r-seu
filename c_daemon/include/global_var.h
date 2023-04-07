#ifndef GLOBAL_VAR_H
#define GLOBAL_VAR_H

#include <arpa/inet.h>
#include <errno.h>
#include <ifaddrs.h>
#include <netdb.h>
#include <netinet/in.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <sys/select.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

#define max(a, b) ((a > b) ? a : b)
#define PLAYER_MAX 10
#define MESG_KEY 1234
#define False 0
#define True 1
#define C_TO_PY 2
#define PY_TO_C 3

extern const int BUFSIZE;
extern uint16_t PORT;

extern int listenfd;
// extern int player_socket[PLAYER_MAX];

typedef struct {
    int used;
    int socket;
    char *IP;
} network_info;

typedef struct {
    int32_t message_type;
    uint64_t posx;
    uint64_t posy;
    uint64_t type;
    uint64_t x;
} python_struct_t;

typedef struct {
    long mesg_type;
    python_struct_t mes;
} send_message;

typedef struct {
    long mesg_type;
    char mesg_text[100];
} recv_message;

extern network_info connection[PLAYER_MAX];

extern int existed_player;

extern struct sockaddr_in master_addr;

#endif