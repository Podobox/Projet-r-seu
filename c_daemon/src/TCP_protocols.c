#include "TCP_protocols.h"
#include "global_var.h"

// return 0 if no problem
// return 1 if violate number of existed players or maximum players
// return 2 if cannot create socket
// return 3 if cannot connect to player
int connect_existed_players(int index) {
    if (index >= existed_player || index >= PLAYER_MAX) {
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

// char *gethostIP() {
//     char hostbuffer[256];
//     char *hostIP;
//     struct hostent *host_entry;
 
//     // To retrieve hostname
//     if ((gethostname(hostbuffer, sizeof(hostbuffer))) == -1) {
//         stop("gethostname");
//     }

//     // To retrieve host information
//     if ((host_entry = gethostbyname(hostbuffer)) == -1) {
//         stop("gethostbyname");
//     }

//     // To convert an Internet network
//     // address into ASCII string
//     hostIP = inet_ntoa(*((struct in_addr *)host_entry->h_addr_list[0]));

//     printf("Host IP: %s\n", hostIP);
//     hostIP[strlen(hostIP)] = '\0';
//     return hostIP;
// }

void stop(char *msg) {
    close(listenfd);
    perror(msg);
    exit(EXIT_FAILURE);
}


char *gethostIP() {

    struct ifaddrs *ifaddr;
    int family, s;
    char host[NI_MAXHOST];
    char *hostIP;


    if (getifaddrs(&ifaddr) == -1) {
        stop("getifaddrs");
    }

    /* Walk through linked list, maintaining head pointer so we
        can free list later */

    for (struct ifaddrs *ifa = ifaddr; ifa != NULL;
            ifa = ifa->ifa_next) {
        if (ifa->ifa_addr == NULL)
            continue;

        family = ifa->ifa_addr->sa_family;

        /* For an AF_INET* interface address, display the address */

        if (family == AF_INET) {
            s = getnameinfo(ifa->ifa_addr,
                    (family == AF_INET) ? sizeof(struct sockaddr_in) :
                                            sizeof(struct sockaddr_in6),
                    host, NI_MAXHOST,
                    NULL, 0, NI_NUMERICHOST);
            if (s != 0) {
                printf("getnameinfo() failed: %s\n", gai_strerror(s));
                exit(EXIT_FAILURE);
            }

            printf("\t\taddress: <%s>\n", host);
            hostIP = host;
        } 
    }

    freeifaddrs(ifaddr);
    return hostIP;
}
