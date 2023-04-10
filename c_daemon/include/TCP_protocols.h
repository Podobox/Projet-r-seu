#ifndef TCP_PROTOCOLS_H
#define TCP_PROTOCOLS_H

int connect_existed_players(int index);

int create_master_socket(char *myIP);

void stop(char *msg);

void add_connection(int, char*);

void print_connections();

void close_connection(int);

void send_file_by_socket(int);

void recv_file(int);

char* get_my_IP();

#endif