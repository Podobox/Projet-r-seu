#include "IPC.h"
#include "TCP_protocols.h"
#include "global_var.h"

// functions to work with the structure

// Function to add a new player info to the list of connected player
void add_connection(int socket, char *IP) {
    int i = 0;

    while (i < PLAYER_MAX && connection[i].used) {
        i++;
    }

    if (i < PLAYER_MAX) {
        connection[i].used   = 1;
        connection[i].socket = socket;
        connection[i].IP     = strdup(IP);
        existed_player++;
    } else {
        // The array is full, handle the error as needed.
    }
}

void close_connection(int index) {
    close(connection[index].socket);
    connection[index].socket = 0;
    connection[index].used   = 0;
}

void print_connections() {
    for (int i = 0; i < PLAYER_MAX; i++) {
        if (connection[i].used) {
            printf("Connection %d:\n", i);
            printf("\tSocket: %d\n", connection[i].socket);
            printf("\tIP: %s\n", connection[i].IP);
        }
    }
}

void send_file_by_socket(int sockfd) {
    FILE *fp;
    char buffer[BUFSIZE];
    long file_size;

    // ask python to save the game
    send_from_c(3, 0, 0, 0, 0);
    recv_from_python_mt(10);

    // get the name of the file
    char cwd[BUFSIZE];
    getcwd(cwd, sizeof(cwd));

    strcat(cwd, "/Save/online_game");
    printf("\t$PWD: %s\n", cwd);

    fp = fopen(cwd, "r");
    if (fp == NULL) {
        stop("File not found.\n");
    }

    // Determine the size of the file
    fseek(fp, 0, SEEK_END);
    file_size = ftell(fp);
    rewind(fp);

    // send the file size
    sprintf(buffer, "/file_size %ld", file_size);
    printf("\tsent = %s\n", buffer);
    send_message message;
    message.mesg_type = file_size;
    if (write(sockfd, &message, sizeof(send_message)) < 0) {
        stop("cannot send file_size info");
    }

    // read in the file and send
    int size;
    while ((size = fread(buffer, 1, BUFSIZE - 1, fp)) == BUFSIZE - 1) {
        buffer[size] = '\0';
        // printf("\tsent buffer %d: %s\n", size ,buffer);
        if (write(sockfd, buffer, size) < 0) {
            stop("\terror in sending file");
        }
    }
    buffer[size] = '\0';
    if (write(sockfd, buffer, size) < 0) {
        stop("send");
    }

    fclose(fp);

    printf("File sent succesfully\n");
}

void recv_file(int sockfd) {
    /* start of recv_file */
    printf("IN RECV FILE\n");

    char buffer[BUFSIZE];
    bzero(buffer, BUFSIZE);
    long file_size       = -1;  // not initialised yet
    int total_bytes_read = 0;

    // create a new file in the save directory
    char cwd[BUFSIZE];
    getcwd(cwd, sizeof(cwd));
    strcat(cwd, "/Save/online_game");
    printf("\t$PWD received file: %s\n", cwd);

    FILE *fp = fopen(cwd, "w");
    if (fp == NULL) {
        printf("Error creating file.\n");
        return;
    }

    // printf("\tstart recv_file()\n");
    int valread;

    send_message message;
    valread   = read(sockfd, &message, sizeof(send_message));
    file_size = message.mesg_type;

    /*valread = read(sockfd, buffer, BUFSIZE - 1);*/
    /*char *cmd = strtok(buffer, " ");*/

    /*// get the file size to verify the file is sent correctly*/
    /*file_size = atoi(strtok(NULL, " "));*/
    printf("\tcmd in recv_file, file size = %ld\n", file_size);
    // printf("\tin recv_file, total bytes read = %d\n", total_bytes_read);

    // verify if the file is received successfully before do other thing
    while (total_bytes_read < file_size) {
        /*printf("%i\n", total_bytes_read);*/
        while ((valread = recv(sockfd, buffer, BUFSIZE - 1, MSG_DONTWAIT)) == BUFSIZE - 1) {
            /*while ((valread = read(sockfd, buffer, BUFSIZE - 1)) == BUFSIZE - 1 ||
             * total_bytes_read < file_size - BUFSIZE + 1) {*/

            buffer[valread] = '\0';
            // printf("\trecv buffer %d: %s\n", valread,  buffer);
            fwrite(buffer, 1, valread, fp);
            total_bytes_read += valread;
        }

        if (valread < 0) {
            continue;
        }

        /*printf("valread : %d\n", valread);*/
        if (valread != 0) {
            buffer[valread] = '\0';
            fwrite(buffer, 1, valread, fp);
            total_bytes_read += valread;
        }

        /*if(total_bytes_read < file_size ) {*/
        /*printf("\tReceived file of %ld unsuccessfully (%d)\n", file_size,
         * total_bytes_read);*/
        /*stop("not received the file to start the game successfully");*/
        /*exit(EXIT_FAILURE);*/
        /*}*/
    }

    // printf("\tend recv_file()\n");
    fclose(fp);

    printf("\tin recv_file out while, total bytes read = %d\n", total_bytes_read);
    if (total_bytes_read >= file_size) {
        printf("\tReceived file of %ld successfully (%d)\n", file_size, total_bytes_read);
    } else {
        printf("\tReceived file of %ld unsuccessfully\n", file_size);
        stop("not received the file to start the game successfully");
    }
    send_from_c_mt(0, 0, 0, 0, 0, 11);
    /* end of recv_file */
}
