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

// void send_file_by_socket(int sockfd) {
//     FILE *fp;
//     char buffer[BUFSIZE];
//     long file_size;

//     // TO DO 
//     // get the name of the file
//     char cwd[BUFSIZE];
//     getcwd(cwd, sizeof(cwd));

//     // for(int i=strlen(cwd) -1; 0 <= i; i--){
//     //     if(cwd[i] == '/'){
//     //         cwd[i+1] = '\0';
//     //         break;
//     //     }
//     // }

//     /*sprintf(cwd,"%s/Save/online_game",cwd);*/
//     strcat(cwd, "/Save/online_game");
//     printf("\t$PWD: %s\n", cwd);

//     // sent info to start sending file
//     if (write(sockfd, "/file_start", strlen("/file_start") + 1) < 0) {
//         stop("cannot send file_start info");
//     }

//     if ((fp = fopen(cwd, "r"))== NULL) {
//         stop("File not found.\n");
//     }

//     // Determine the size of the file
//     fseek(fp, 0, SEEK_END);
//     file_size = ftell(fp);
//     rewind(fp);

//     sprintf(buffer, "/file_size %ld", file_size);
//     printf("\tsent = %s\n", buffer);
//     if (write(sockfd, buffer, strlen(buffer) + 1) < 0) {
//         stop("cannot send file_size info");
//     }

//     // read in the file and send
//     int size;
//     while ((size = fread(buffer, 1, BUFSIZE - 1, fp)) == BUFSIZE - 1) {
//         buffer[size] = '\0';
//         printf("\tsent buffer %d: %s\n", size ,buffer);
//         if (write(sockfd, buffer, size) < 0) {
//             stop("error in sending file");
//         }
//     }

//     buffer[size] = '\0';
//     if (write(sockfd, buffer, size) < 0) {
//         stop("send");
//     }
//     printf("\tsent buffer %d: %s\n", size ,buffer);


//     fclose(fp);

//     printf("\tFile sent succesfully\n");

// }

// void recv_file(int sockfd) {
//     printf("IN IP RESPONSE\n");

//     char buffer[BUFSIZE];
//     long file_size;
//     char *cmd;
//     int total_bytes_read = 0;

//     // create a new file in the save directory
//     char cwd[BUFSIZE];
//     getcwd(cwd, sizeof(cwd));
//     strcat(cwd, "/Save/on_game");
//     printf("\t$PWD received file: %s\n", cwd);

//     FILE* fp = fopen(cwd, "w");
//     if (fp == NULL) {
//         printf("Error creating file.\n");
//         return;
//     }

//     printf("\tstart recv_file()\n");
//     int valread;


//     valread = read(sockfd, buffer, BUFSIZE - 1);
//     cmd = strtok(buffer, " ");

//     // get the file size to verify the file is sent correctly
//     file_size = atoi(strtok(NULL, " "));
//     printf("cmd in recv_file, file size = %ld\n", file_size);
//     printf("in recv_file, total bytes read = %d\n", total_bytes_read);


//     while ( total_bytes_read + BUFSIZE - 1 <= file_size ) {

//         valread = read(sockfd, buffer, BUFSIZE - 1);
//         buffer[valread] = '\0';
//         fwrite(buffer, 1, valread, fp);
//         total_bytes_read += BUFSIZE - 1; 
//         printf("\trecv buffer, total_bytes_read = %d, valread = %dB: %s\n", total_bytes_read, valread,  buffer);
        
//     }

//     valread = read(sockfd, buffer, BUFSIZE - 1);
//     if (valread != 0) {
//         buffer[valread] = '\0';
//         // printf("\trecv buffer, total_bytes_read = %d, valread = %dB: %s\n", total_bytes_read, valread,  buffer);
//         fwrite(buffer, 1, valread, fp);  
//         total_bytes_read += valread; 
//     }

//     fclose(fp);


//     printf("in recv_file out while, total bytes read = %d\n", total_bytes_read);
//     if(total_bytes_read == file_size) {
//         printf("\tReceived file of %ld successfully\n", file_size);
//         // return 0;
//     }
//     else {
//         printf("\tReceived file of %ld unsuccessfully\n", file_size);
//         // return 1;
//     }

    
// }

void send_file_by_socket(int sockfd) {
    FILE *fp;
    char buffer[BUFSIZE];
    long file_size;


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
    if (write(sockfd, buffer, strlen(buffer) + 1) < 0) {
        stop("cannot send file_size info");
    }

    // read in the file and send
    int size;
    while ((size = fread(buffer, 1, BUFSIZE - 1, fp)) == BUFSIZE - 1) {
        buffer[size] = '\0';
        printf("\tsent buffer %d: %s\n", size ,buffer);
        if (write(sockfd, buffer, size) < 0) {
            stop("\terror in sending file");
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
    printf("IN IP RESPONSE\n");

    char buffer[BUFSIZE];
    long file_size;
    char *cmd;
    int total_bytes_read = 0;

    // create a new file in the save directory
    char cwd[BUFSIZE];
    getcwd(cwd, sizeof(cwd));
    strcat(cwd, "/Save/on_game");
    printf("\t$PWD received file: %s\n", cwd);

    FILE* fp = fopen(cwd, "w");
    if (fp == NULL) {
        printf("Error creating file.\n");
        return;
    }

    printf("start recv_file()\n");
    int valread;

    valread = read(sockfd, buffer, BUFSIZE - 1);
    cmd = strtok(buffer, " ");

    // get the file size to verify the file is sent correctly
    file_size = atoi(strtok(NULL, " "));
    printf("cmd in recv_file, file size = %ld\n", file_size);
    printf("in recv_file, total bytes read = %d\n", total_bytes_read);
    
    while ((valread = read(sockfd, buffer, BUFSIZE - 1)) == BUFSIZE - 1) {

        // Check if the received message indicates the end of the file transfer
        // if (!strcmp(buffer, "/file_transfer_end")) {
        //     printf("recv buffer: %s\n", buffer);
        //     break;
        // }

        buffer[valread] = '\0';
        printf("recv buffer %d: %s\n", valread,  buffer);
        fwrite(buffer, 1, valread, fp);
        total_bytes_read += valread; 

    }

    if (valread != 0) {
        // printf("sent buffer END: %s\n", buffer);

        // if (!strcmp(buffer, "/file_transfer_end")) {
        //     printf("sent buffer END: %s\n", buffer);
        // } 
        // else {}

        buffer[valread] = '\0';
        fwrite(buffer, 1, valread, fp);
        total_bytes_read += valread; 

        
    }

    printf("end recv_file()\n");
    
    fclose(fp);

    printf("in recv_file out while, total bytes read = %d\n", total_bytes_read);
    if(total_bytes_read == file_size) {
        printf("\tReceived file of %ld successfully\n", file_size);
        // return 0;
    }
    else {
        printf("\tReceived file of %ld unsuccessfully\n", file_size);
        // return 1;
    }

}











