#include "log.h"
#include "listen.h"
#include <stdio.h>
#include <unistd.h>  // For sleep function

#define UART_PORT "/dev/ttys003"  // Port to listen on
#define BUFFER_SIZE 256

int main(void) {
    init_log();
    log_info("Starting UART communication");

    // Open UART port
    int uart_fd = open_uart(UART_PORT);
    if (uart_fd == -1) {
        log_error("Failed to open UART port");
        return 1;
    }
    log_info("UART port opened successfully");

    char buffer[BUFFER_SIZE];
    while (1) {
        int read_bytes = read_uart(uart_fd, buffer, BUFFER_SIZE - 1); 
        log_info("Awaiting command.");
        if (read_bytes > 0) {
            buffer[read_bytes] = '\0'; 
            printf("Received command: %s\n", buffer);
            log_info("Received command.");

        sleep(1);
    }
    }
    
    close_uart(uart_fd);
    log_info("UART port closed");

    close_log();

    return 0;
}
