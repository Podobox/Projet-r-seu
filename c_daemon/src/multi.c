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

#define INVALID_SOCKET -1
#define SOCKET_ERROR -1
#define TRUE 1
#define BUFLEN 1024	    //Buffer length

void stop(char *s)
{
	perror(s);
	exit(EXIT_FAILURE);
}

void chatTP(int sockfd)
{
	char buff[BUFLEN], *pseudo;
	int n, rest;
	bzero(&pseudo, sizeof(pseudo));
	while (TRUE) {
        // Create a file descriptor set
		fd_set read_fds;
		FD_ZERO(&read_fds);
		bzero(buff, sizeof(buff));

		// Add the sockets to the read and write sets
        if (sockfd != 0){
            FD_SET(sockfd, &read_fds);
		}
        FD_SET(0, &read_fds);

		if (select(sockfd+1, &read_fds, NULL, NULL, NULL) < 0) {
			stop("select");
		}

		if (FD_ISSET(sockfd, &read_fds)) {

			// data is available to be read
			if (( n = recv(sockfd , buff , sizeof(buff), 0)) < 0)
				stop("recv error");
			else if (n == 0) {
				printf("\033[0mConnection closed by foreign host.\n\r");
				break;
			}

            
			// when te pseudo is used by another registered user
			else if (strcmp(buff, "Change your pseudo with /nickname <pseudo>") == 0)
			{
				n = 0;            
				// scan from the client
				int c;
				while ((c = getchar()) != '\n' && c != EOF)
					buff[n++] = c;
				buff[n] = '\0';
				
				if(strcmp(buff, "\n") != 0){
					write(sockfd, buff, sizeof(buff));
				}
				
				bzero(buff, sizeof(buff));
			}
			
			else{
				printf("\033[0m%s\033[0;35m\n", buff);
				bzero(buff, sizeof(buff));
			}
		}

        if (FD_ISSET(0, &read_fds)) {
            n = 0;            
            // scan from the client
            int c;

            while ((c = getchar()) != '\n' && c != EOF)
                buff[n++] = c;
            buff[n] = '\0';
            
            if(strcmp(buff, "\n") != 0){
                write(sockfd, buff, sizeof(buff));
            }
            
            bzero(buff, sizeof(buff));
        }

	}
}

int main(int argc,char *argv[])
{
	int n = 0, sock;
	char buff[BUFLEN], message[BUFLEN+1], pseudo[20];
	struct sockaddr_in server_addr;

	if (argc < 2 || argc > 3) {
        printf("Usage: %s address [port]\n", argv[0]);
		stop("Byeee");
    }

	int PORT = atoi(argv[2]);

	// Connect to a remote host
	server_addr.sin_family = AF_INET;
	server_addr.sin_port = htons(PORT);
	server_addr.sin_addr.s_addr = inet_addr(argv[1]);

	if(server_addr.sin_addr.s_addr == INADDR_NONE)
		stop("erreur inaddr\n");
	else
		printf("Trying %s...\n", inet_ntoa(server_addr.sin_addr));

	sock = socket(AF_INET,SOCK_STREAM,0);
	if(sock == INVALID_SOCKET)
		stop("socket invalide !\n");

	if(connect(sock,(struct sockaddr*)&server_addr, sizeof(server_addr)) != 0)
	{
		stop("connect() : Unable to connect to the remote host");
		close(sock);
	}

	printf("Connected to %s.\n", argv[1]);

	// recv
	bzero(&message,BUFLEN+1);
	if( recv(sock, message, BUFLEN, 0) < 0 ){
			stop("recv failed. Error");
	}

	//show a message from server
	printf("\033[0;31mMessage from Server : %s\033[0m", message);	

	// function for chat
	printf("\033[0;35m\n"); 
	chatTP(sock);
	close(sock);
	return 0;
}