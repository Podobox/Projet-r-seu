#include "TCP_protocols.h"
#include "global_var.h"

// functions to work with the structure

// Function to add a new player info to the list of connected player
void add_connection(int socket, char* IP) {
    int i = 0;

    while (i < PLAYER_MAX && connection[i].used) {
        i++;
    }

    if (i < PLAYER_MAX) {
        connection[i].used = 1;
        connection[i].socket = socket;
        connection[i].IP = strdup(IP);
        existed_player++;
    } else {
        // The array is full, handle the error as needed.
    }
}

void close_connection(int index) {
    close(connection[index].socket);
    connection[index].socket = 0;
    connection[index].used = 0;
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

    fp = fopen("/home/dini/Documents/S6/Projet reseaux/Projet-r-seu/Save/fifi", "r");
    if (fp == NULL) {
        stop("File not found.\n");
    }

    // read in the file and send
    int size;
    while ((size = fread(buffer, 1, BUFSIZE - 1, fp)) == BUFSIZE - 1) {
        buffer[size] = '\0';
        printf("sent buffer %d: %s\n", size ,buffer);
        if (write(sockfd, buffer, size) < 0) {
            stop("error in sending file");
        }
    }
    buffer[size] = '\0';
    if (write(sockfd, buffer, size) < 0) {
        stop("send");
    }

    fclose(fp);

    // Send a message to indicate the end of the file transfer
    // sprintf(buffer, "/file_transfer_end");
    // if (write(sockfd, buffer, strlen(buffer) + 1) < 0) {
    //     fprintf(stderr, "Error sending end of file transfer message.\n");
    // }
    // printf("sent buffer: %s\n", buffer);
    printf("File sent succesfully\n");

}

void recv_file(int sockfd) {
   char buffer[BUFSIZE];

    // create the directory if it doesn't exist
    mkdir(SAVE_DIR, S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);

    // create a new file in the save directory
    char filename[MAX_FILENAME_LENGTH];
    sprintf(filename, "%s/test", SAVE_DIR);


    FILE* fp = fopen(filename, "w");
    if (fp == NULL) {
        printf("Error creating file.\n");
        return;
    }

    printf("start recv_file()\n");
    int valread;
    while ((valread = read(sockfd, buffer, BUFSIZE - 1)) == BUFSIZE - 1) {

        // Check if the received message indicates the end of the file transfer
        // if (!strcmp(buffer, "/file_transfer_end")) {
        //     printf("recv buffer: %s\n", buffer);
        //     break;
        // }

        buffer[valread] = '\0';
        printf("recv buffer %d: %s\n", valread,  buffer);
        fwrite(buffer, 1, valread, fp);
    }

    if (valread != 0) {
        // printf("sent buffer END: %s\n", buffer);

        // if (!strcmp(buffer, "/file_transfer_end")) {
        //     printf("sent buffer END: %s\n", buffer);
        // } 
        // else {}

        buffer[valread] = '\0';
        fwrite(buffer, 1, valread, fp);
        
    }


    printf("end recv_file()\n");
    
    fclose(fp);
}




