#ifndef IPC_H
#define IPC_H

#include "global_var.h"

void handle_sigterm();

void handle_parent_exit();

void send_from_c(int32_t msg_type, uint64_t posx, uint64_t posy, uint64_t type, uint64_t x);
void send_from_c_mt(int32_t msg_type, uint64_t posx, uint64_t posy, uint64_t type, uint64_t x, int mt);

python_struct_t* recv_from_python();
python_struct_t* recv_from_python_mt(int mt);

#endif
