#ifndef TCP_PROTOCOLS_H
#define TCP_PROTOCOLS_H

int connect_existed_players(int index);

int create_master_socket(char *myIP);

char *gethostIP();

void stop(char *msg);

#endif