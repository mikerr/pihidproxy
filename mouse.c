#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>

int main(int argc, char** argv)
{
    int fd, bytes;
    unsigned char data[3];

    const char *pDevice = "/dev/input/mice";
    //const char *pDevice = "/dev/input/mouse0";

    // Open Mouse
    fd = open(pDevice, O_RDWR);
    if(fd == -1)
    {
        printf("ERROR Opening %s\n", pDevice);
        return -1;
    }

    int left, middle, right;
    signed char x, y;
    while(1)
    {
        // Read Mouse
        bytes = read(fd, data, sizeof(data));

        if(bytes > 0)
        {
            left = data[0] & 0x1;
            right = data[0] & 0x2;
            middle = data[0] & 0x4;

            x = data[1];
            y = data[2];
            printf("x=%d, y=%d, left=%d, middle=%d, right=%d\n", x, y, left, middle, right);
        }
    }
    return 0;
}
