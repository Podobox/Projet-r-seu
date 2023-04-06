#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <stdint.h>

#define  BUF_SIZE  1024
#define  C_TO_PY   2
#define  MESG_KEY  1234
#define  MAX	   10
#define  False     0
#define  True      1



struct python_struct_t {
	int32_t message_type;
	uint64_t posx;
	uint64_t posy;
	uint64_t type;
	uint64_t x;
};

struct python_struct_t *buffer;

struct {
	long  mesg_type;
	struct python_struct_t mes;
} message;

void send_from_c()
{
	// buffer->message_type = 5;
	message.mes.message_type = 5;
	int msqid;
	// msgget creates a message queue and returns identifier
	msqid = msgget(MESG_KEY, 0666 | IPC_CREAT);
	message.mesg_type = C_TO_PY;	

	int length;
    printf("%d \n", message.mes.message_type);
    if ((length = msgsnd(msqid, &message, sizeof(message) - sizeof(long), 0)) == -1)
	{
		perror("Msgsnd() failed");
		exit(1);
	}
}

int main()
{
	buffer = calloc(sizeof(struct python_struct_t), 1);

	while (True)
	{
		send_from_c();
	}
}