#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <errno.h>

#define INVALID_SOCKET -1
#define SOCKET_ERROR -1
#define TRUE 1
#define BUFLEN 1024	    //Buffer length
#define PORT 1234
#define max(a, b) ((a > b) ? a : b)

void stop(char *s)
{
	perror(s);
	exit(EXIT_FAILURE);
}

int main(int argc,char *argv[])
{
	int sock, maxfd, connfd, nready;
	char buff[BUFLEN];
	struct sockaddr_in other_player_addr, my_addr;
    const int number_player = 2;
	char playerIP[][100] = {};
    int player_socket[number_player];
  
    // connect to all players connected
    for(int i=0;i<number_player;i++){	

         // create socket
        sock = socket(AF_INET,SOCK_STREAM,0);
        if(sock == INVALID_SOCKET)
            stop("socket invalide !\n");

        other_player_addr.sin_family = AF_INET;
        other_player_addr.sin_port = htons(PORT);
        other_player_addr.sin_addr.s_addr = playerIP[i];

        if(other_player_addr.sin_addr.s_addr == INADDR_NONE)
            stop("error inaddr\n");
        else
            printf("Trying %s...\n", inet_ntoa(other_player_addr.sin_addr));

		if(connect(sock,(struct sockaddr*)&other_player_addr, sizeof(other_player_addr)) != 0)
        {
            stop("connect() : Unable to connect to the remote host");
            close(sock);
        }

        // Accept the connection
	    memset(&other_player_addr, 0, sizeof(other_player_addr));
	}

    
    //set of socket descriptors
	int listenfd = socket(AF_INET,SOCK_STREAM,0);
    if(listenfd == INVALID_SOCKET)
        stop("socket invalide !\n");

    my_addr.sin_family = AF_INET;
    my_addr.sin_port = htons(PORT);
    my_addr.sin_addr.s_addr = inet_addr("127.0.0.1");

    int *len;
    *len = sizeof(my_addr);

    fd_set readfds;
    if (bind(listenfd, (struct sockaddr *)&my_addr, sizeof(my_addr))<0)
		stop("bind failed");

	// Ready to listen	
	if (listen(listenfd, 5) != 0)
		stop("listen failed. Error");
    
    while (1) {

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

        if (((nready = select(maxfd + 1, &readfds, NULL, NULL, NULL)) < 0) && errno != EINTR) {
            stop("Select Error\n");
        }

        if (FD_ISSET(listenfd, &readfds)) {
            if ((connfd = accept(listenfd, (struct sockaddr *)&my_addr, &len)) < 0) {
                stop("Cannot connect to this client!");
            }

            int clientID;
            for (int index = 0; index < number_player; index++) {
                if (player_socket[index] == 0) {
                    player_socket[index] = connfd;
                    break;
                }
            }
		}
	}

	close(sock);
	return 0;
}