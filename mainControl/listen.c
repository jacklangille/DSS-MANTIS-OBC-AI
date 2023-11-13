#include "listen.h"
#include <fcntl.h>   // File control definitions
#include <unistd.h>  // UNIX standard function definitions
#include <termios.h> // POSIX terminal control definitions
#include <errno.h>   // Error number definitions
#include <string.h>  // String function definitions

int open_uart(const char *portname) {
    /* Function to open UART port for comms */
    /* Returns a file descriptor for the opened port */
    /* Takes in a pointer to the name of the port to open */
    
    int uart_fd = open(portname, O_RDWR | O_NOCTTY | O_NDELAY);
    if (uart_fd == -1) {
        return -1;
    }

    struct termios options;
    tcgetattr(uart_fd, &options);
    tcsetattr(uart_fd, TCSANOW, &options);

    return uart_fd;
}

void close_uart(int uart_fd) {
    close(uart_fd);
}

int read_uart(int uart_fd, char *buffer, int buffer_size) {
    return read(uart_fd, buffer, buffer_size);
}