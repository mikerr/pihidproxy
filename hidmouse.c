#include <pthread.h>
#include <string.h>
#include <stdio.h>
#include <ctype.h>
#include <fcntl.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define BUF_LEN 512

struct options {
        const char    *opt;
        unsigned char val;
};

static struct options mmod[] = {
        {.opt = "--b1", .val = 0x01},
        {.opt = "--b2", .val = 0x02},
        {.opt = "--b3", .val = 0x04},
        {.opt = NULL}
};

int mouse_fill_report(char report[8], char buf[BUF_LEN], int *hold)
{
        char *tok = strtok(buf, " ");
        int mvt = 0;
        int i = 0;
        for (; tok != NULL; tok = strtok(NULL, " ")) {

                if (strcmp(tok, "--quit") == 0)
                        return -1;

                if (strcmp(tok, "--hold") == 0) {
                        *hold = 1;
                        continue;
                }

                for (i = 0; mmod[i].opt != NULL; i++)
                        if (strcmp(tok, mmod[i].opt) == 0) {
                                report[0] = report[0] | mmod[i].val;
                                break;
                        }
                if (mmod[i].opt != NULL)
                        continue;

                if (!(tok[0] == '-' && tok[1] == '-') && mvt < 2) {
                        errno = 0;
                        report[1 + mvt++] = (char)strtol(tok, NULL, 0);
                        if (errno != 0) {
                                fprintf(stderr, "Bad value:'%s'\n", tok);
                                report[1 + mvt--] = 0;
                        }
                        continue;
                }
                fprintf(stderr, "unknown option: %s\n", tok);
        }
        return 3;
}

int main(int argc, const char *argv[])
{
        const char *filename = NULL;
        int fd = 0;
        char buf[BUF_LEN];
        int cmd_len;
        char report[8];
        int to_send = 8;
        int hold = 0;
        fd_set rfds;
        int retval, i;

        if (argc < 3) {
                fprintf(stderr, "Usage: %s devname x y\n",
                        argv[0]);
                return 1;
                }

        filename = argv[1];

        if ((fd = open(filename, O_RDWR, 0666)) == -1) {
                perror(filename);
                return 3;
                }

        memset(report, 0x0, sizeof(report));

        cmd_len = sprintf(buf,"%s %s",argv[2],argv[3]);
        hold = 0;

        memset(report, 0x0, sizeof(report));

        to_send = mouse_fill_report(report, buf, &hold);

        if (write(fd, report, to_send) != to_send) {
                        perror(filename);
                        return 5;
                        }
        close(fd);
        return 0;
}
