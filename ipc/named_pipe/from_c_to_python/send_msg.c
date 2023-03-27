#include <stdio.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>

#define FIFO_FILE "MYFIFO3"
int main() {
   int fd;
   int end_process;
   int stringlen;
   char readbuf[80];
   char end_str[5];
   printf("FIFO_CLIENT: Send messages, infinitely, to end enter \"end\"\n");
   mknod(FIFO_FILE, __S_IFIFO | 0640, 0);
   fd = open(FIFO_FILE, O_RDWR);
   strcpy(end_str, "end");
   
   while (1) {
      printf("Enter string: ");
      fgets(readbuf, sizeof(readbuf), stdin);
      stringlen = strlen(readbuf);
      readbuf[stringlen - 1] = '\0';
      readbuf[stringlen] = '\n';
      end_process = strcmp(readbuf, end_str);
      
      if (end_process != 0) {
         write(fd, readbuf, strlen(readbuf));
         printf("Sent string: \"%s\" and string length is %d\n", readbuf, (int)strlen(readbuf));
      } else {
         write(fd, readbuf, strlen(readbuf));
         printf("Sent string: \"%s\" and string length is %d\n", readbuf, (int)strlen(readbuf));
         unlink(FIFO_FILE);
         close(fd);
         break;
      }
   }
   return 0;
}