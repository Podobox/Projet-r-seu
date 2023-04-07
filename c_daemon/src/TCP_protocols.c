#include "TCP_protocols.h"

#include "global_var.h"

// return 0 if no problem
// return 1 if violate number of existed players or maximum players
// return 2 if cannot create socket
// return 3 if cannot connect to player
int connect_existed_players(int index) {
    if (index >= PLAYER_MAX) {
        return 1;
    }

    // create socket
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        return 2;
    }

    // initialise socket address
    struct sockaddr_in current_player;
    bzero(&current_player, sizeof(current_player));
    current_player.sin_family = AF_INET;
    current_player.sin_port = htons(PORT);
    current_player.sin_addr.s_addr = inet_addr(connection[index].IP);

    // connect to the player
    if (connect(sock, (struct sockaddr *)&current_player, sizeof(current_player)) < 0) {
        return 3;
    }

    // save player socket
    connection[index].socket = sock;
    connection[index].used = 1;
    return 0;
}

// return 0 if no problem
// return 1 if cannot create socket
// return 2 if cannot bind socket
// return 3 if cannot listen
int create_master_socket(char *ip_host) {
    // create socket
    if ((listenfd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        return 1;
    }

    // initialise socket address
    bzero(&master_addr, sizeof(master_addr));
    master_addr.sin_family = AF_INET;
    master_addr.sin_port = htons(PORT);
    master_addr.sin_addr.s_addr = inet_addr(ip_host);

    int option = 1;
    if (setsockopt(listenfd, SOL_SOCKET, SO_REUSEPORT, &option, sizeof(option)) < 0) {
        perror("setsockopt");
    }

    // bind socket to address
    if (bind(listenfd, (struct sockaddr *)&master_addr, sizeof(master_addr)) < 0) {
        perror(strerror(errno));
        return 2;
    }

    // listen on socket
    if (listen(listenfd, PLAYER_MAX) < 0) {
        return 3;
    }

    return 0;
}

void stop(char *msg) {
    close(listenfd);
    perror(msg);
    exit(EXIT_FAILURE);
}


char *get_my_IP() {
    struct ifaddrs *addrs, *tmp;
    addrs = (struct ifaddrs *)malloc(sizeof(struct ifaddrs));
    tmp = (struct ifaddrs *)malloc(sizeof(struct ifaddrs));
    getifaddrs(&addrs);
    tmp = addrs;

    while(tmp){
        if(tmp->ifa_addr && tmp->ifa_addr->sa_family == AF_INET){
            struct sockaddr_in *pAddr = (struct sockaddr_in *) tmp->ifa_addr;
            if(strcmp(tmp->ifa_name, "lo")){
                return inet_ntoa(pAddr->sin_addr);
            }
        }
        tmp = tmp->ifa_next;
    }
    freeifaddrs(addrs);
    return NULL;
}
