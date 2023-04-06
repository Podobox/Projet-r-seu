#ifndef GLOBAL_VAR_H
#define GLOBAL_VAR_H

#define _GNU_SOURCE     /* To get defns of NI_MAXSERV and NI_MAXHOST */

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
#include <ifaddrs.h>
#include <arpa/inet.h>
#include <linux/if_link.h>

#define max(a, b) ((a > b) ? a : b)
#define PLAYER_MAX 10
#define MAX_FILENAME_LENGTH 15

// define the save directory
#define SAVE_DIR "../Save"

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