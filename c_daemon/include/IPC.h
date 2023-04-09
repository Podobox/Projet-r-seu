#ifndef IPC_H
#define IPC_H

#include "global_var.h"

void handle_sigterm();

void handle_parent_exit();

void send_from_c(int32_t msg_type, uint64_t posx, uint64_t posy, uint64_t type, uint64_t x);

python_struct_t* recv_from_python();

#endif