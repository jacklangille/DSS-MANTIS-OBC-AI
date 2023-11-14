/*
This program sets up UART communication on a Unix-like OS, logs the process, 
and reads incoming UART messages. It is designed to work with virtual UART ports 
created using 'socat', allowing for UART communication simulation. 
The program initializes logging, opens a specified UART port, continuously reads and logs 
received messages, and cleans up by closing the UART port and the log file.

To use with 'socat' for simulating UART ports:
- Set up a pair of virtual serial ports using 'socat'.
    - From a terminal run "socat -d -d pty,raw,echo=0 pty,raw,echo=0"
    - From another terminal run "echo "WAKE" > /dev/ttys004" where WAKE is the message to be sent.
- Assign one of these virtual ports to UART_PORT in this program.
- Run this program, which will then listen and log messages from the virtual UART port.
- To quit, send "SHUT_DOWN" command to port.
*/


#include "log.h" // Header file for logging functions
#include "listen.h" // Header file for listening functions
#include <stdio.h> // Standard input/output header file
#include <unistd.h>  // Header file for various types and constants
#include <string.h> // Header file for basic string ops

#define UART_PORT "/dev/ttys003" // Port to be opened and listen with
#define BUFFER_SIZE 256 // Size of buffer

#define STOP_COMMAND "SHUT_DOWN" // Stop condition

int main(void) {

    init_log(); // Initialize logging 
    log_info("Starting UART communication");

    int uart_fd = open_uart(UART_PORT); // Open port. Log error if this fails.
    if (uart_fd == -1) {
        log_error("Failed to open UART port");
        return 1;
    }
    log_info("UART port opened successfully");

    char buffer[BUFFER_SIZE]; // Create a character array for incoming data.

    while (1) {
        int read_bytes = read_uart(uart_fd, buffer, BUFFER_SIZE - 1); // Fetch number of bytes read
        
        if (read_bytes > 0) { // If number of bytes greater than 0, append a null terminator and print command.
            buffer[read_bytes] = '\0'; 
            // Log the received data
            char log_message[BUFFER_SIZE + 50]; // Extra space for the log message
            sprintf(log_message, "Received command: %s", buffer); 
            log_info(log_message);

            // Print the received data to the terminal
            printf("%s\n", log_message);
            
            // Check for stop command
            if (strcmp(buffer, STOP_COMMAND)) {
                log_info("Stop command received, aborting.");
                break; 
            }
        }
        sleep(1);
    }

    close_uart(uart_fd); // Close port
    log_info("UART port closed"); 
 
    close_log(); // Close log

    return 0;
}

