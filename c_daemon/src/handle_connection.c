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



