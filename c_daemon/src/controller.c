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

void stop(char *s) {
    perror(s);
    exit(EXIT_FAILURE);
}

char * gethostIP() {
    
    char hostbuffer[256];
    char *hostIP;
    struct hostent *host_entry;

    // To retrieve hostname
    if((gethostname(hostbuffer, sizeof(hostbuffer))) == -1) {
        stop("gethostname");
    } 
    
    // To retrieve host information
    if((host_entry = gethostbyname(hostbuffer)) == -1) {
        stop("gethostbyname");
    }

    // To convert an Internet network
    // address into ASCII string
    hostIP = inet_ntoa(*((struct in_addr*)
                           host_entry->h_addr_list[0]));
 
    printf("Host IP: %s\n", hostIP);
}

// get ip address from client connected using socket ?