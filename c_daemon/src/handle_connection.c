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

// recuperer le fichier de souvegarde
void send_file_by_socket(int sock) {
    char *file_contents;
    long file_size;
    FILE *file;
    char buffer[BUFSIZE];
    bzero(buffer, BUFSIZE);

    // Open file
    file = fopen("/home/dini/Documents/S6/Projet reseaux/Projet-r-seu/Save/dini", "rb");
    if (file == NULL) {
        perror("Failed to open file\n");
        exit(EXIT_FAILURE);
    }

    // Get file size
    fseek(file, 0, SEEK_END);
    file_size = ftell(file);
    fseek(file, 0, SEEK_SET);

    // Allocate buffer for file contents
    file_contents = malloc(file_size);
    if (file_contents == NULL) {
        printf("Failed to allocate memory for file contents\n");
        exit(EXIT_FAILURE);
    }

    // Read file contents into buffer
    fread(file_contents, file_size, 1, file);

    // Close file
    fclose(file);

    // Send file contents
    if (send(sock, file_contents, file_size, 0) != file_size) {
        printf("Failed to send file contents\n");
        exit(EXIT_FAILURE);
    }

    printf("File sent successfully\n");
}

void recv_file() {
    // create the directory if it doesn't exist
    mkdir(SAVE_DIR, S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);

    // create a new file in the save directory
    char filename[MAX_FILENAME_LENGTH];
    sprintf(filename, "%s/Test", SAVE_DIR);
    FILE* fp = fopen(filename, "wb");

    // read the file data in chunks and write it to the file
    char buffer[BUFSIZE];
    int num_bytes_read;
    while ((num_bytes_read = recv(listenfd, BUFSIZE, 1024, 0)) > 0) {
        fwrite(buffer, sizeof(char), num_bytes_read, fp);
    }

    printf("File received successfully\n");

    // close the file
    fclose(fp);

}



