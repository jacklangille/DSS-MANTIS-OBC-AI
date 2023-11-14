/*
Function definition for listening capability. 
Nov 14 2023: 
- UART listening capability
- Works with simulated ports using socat
- Three primary functions:
    1. Open port 
    2. Close port
    3. Read incoming UART comm

*/
#include "listen.h"
#include <fcntl.h>   // File control definitions
#include <unistd.h>  // UNIX standard function definitions
#include <termios.h> // POSIX terminal control definitions
#include <errno.h>   // Error number definitions
#include <string.h>  // String function definitions

int open_uart(const char *portname) {
    /* Function to open UART port for comms */
    /* Input: the name of the UART port to be opened */
    /* Returns an integer file descriptor for the opened port */
    
    /* Call open function. Flags: O_RDWR = read/write access. O_NOCTTY = not controlling terminal for the process.
    O_NDELAY = non-blocking mode */ 
    int uart_fd = open(portname, O_RDWR | O_NOCTTY | O_NDELAY); 
    /* Standard error handling in event port fails to open. */
    if (uart_fd == -1) {
        return -1;
    }

    /* Configure for Unix/Unix-like envs. Applies settings immediately to port.
    struct termios options: Create a struct for options.
    tcgetattr(uart_fd, &options): Get the current settings set by uart_fd and store in the termios structure.
    tcgetattr(uart_fd, TCSANOW, &options):  Set settings of uart_fd. TCSANOW implements changes immediately. */
    struct termios options;
    tcgetattr(uart_fd, &options);
    tcsetattr(uart_fd, TCSANOW, &options);

    return uart_fd;
}

void close_uart(int uart_fd) {
    /* Function to close UART port pointed to by file descriptor. Uses the close function - a standard UNIX function
    to close file descriptors. */
    close(uart_fd);
}

int read_uart(int uart_fd, char *buffer, int buffer_size) {
    /* Reads incoming data in buffer. Buffer size set in main.c.
    uart_fd = file descriptor of port
    *buffer = pointer to character array containing read data
    buffer_size = size of buffer */
    return read(uart_fd, buffer, buffer_size);
}