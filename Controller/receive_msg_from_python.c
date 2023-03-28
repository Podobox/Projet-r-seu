#include <stdio.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>

#define BUF_SIZE 1024
#define MAX 10
#define MESG_KEY 1234
#define PY_TO_C 2
#define False 0
#define True 1

// structure for message queue
struct mesg_buffer
{
    long mesg_type;
    char mesg_text[100];
} message;

void recv_from_python()
{

    int msgid;
    // msgget creates a message queue and returns identifier
    msgid = msgget(MESG_KEY, 0666 | IPC_CREAT);
    message.mesg_type = PY_TO_C;

    int length;
    // msgsnd to send message
    if ((length = msgrcv(msgid, &message, sizeof(message), message.mesg_type, 0)) == -1)
    {
        perror("Msgrcv failed");
    }
    // display the message
    message.mesg_text[length] = '\0';
}

int main()
{
    while (True)
    {
        recv_from_python();
        printf("Data send is : %s \n", message.mesg_text);
    }
}