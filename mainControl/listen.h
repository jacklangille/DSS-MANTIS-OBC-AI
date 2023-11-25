#ifndef UART_COMM_H
#define UART_COMM_H

int open_uart(const char *portname);
void close_uart(int uart_fd);
int read_uart(int uart_fd, char *buffer, int buffer_size);

#endif




