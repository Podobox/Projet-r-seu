#include "IPC.h"

void send_from_c(int32_t msg_type, uint64_t posx, uint64_t posy, uint64_t type, uint64_t x) {
    send_message message;
    message.mes.message_type = msg_type;
    message.mes.posx = posx;
    message.mes.posy = posy;
    message.mes.type = type;
    message.mes.x = x;

    int msqid = msgget(MESG_KEY, 0666 | IPC_CREAT);
    message.mesg_type = C_TO_PY;

    if (msgsnd(msqid, &message, sizeof(message) - sizeof(long), 0) < 0) {
        perror("MSGSND");
        exit(1);
    }
}

python_struct_t* recv_from_python() {
    int msqid;
    msqid = msgget(MESG_KEY, 0666 | IPC_CREAT);
    recv_message message;
    message.mesg_type = PY_TO_C;
    int length;
    if ((length = msgrcv(msqid, &message, sizeof(message), message.mesg_type, 0)) < 0) {
        perror("MSGRCV");
        exit(1);
    }
    return (python_struct_t*)message.mesg_text;
}