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

/* Dependencies */
#include "log.h" 							    // Header file for logging functions
#include "listen.h" 							// Header file for listening functions
#include "parse.h"							    // Header file for parsing commands

#include <stdio.h> 							    // Standard input/output header file
#include <unistd.h>  							// Header file for various types and constants
#include <string.h> 							// Header file for basic string ops

#define UART_PORT "/dev/ttys003" 				// Port to opened and listen on
#define BUFFER_SIZE 1024 						// Size of buffer

/* Command list */
#define WAKE "w" 							    // Wake Jetson and initialize systems. Wait for further command
#define SLEEP "s"							    // Routine shutdown. Shut off systems and enter low power mode
#define IMAGE_RX "irx"
#define RESULTS_TX "rtx"						// Transmit cached results
#define INF_1_START "inf1"						// Begin performing HAB inference 
#define INF_2_START "inf2"						// Begin performign tree infernece
#define EMERG_STOP "estp"						// Emergency shutdown. Save system state and turn off asap

/* Main entry point */
int main(void) {

    init_log(); 							    // Initialize logging 
    log_info("Starting UART communication");
        
    int uart_fd = open_uart(UART_PORT); 		// Open port and log error on fail
									
    if (uart_fd == -1) {
        log_error("Failed to open UART port");
        
	return 1;
    }

    log_info("UART port opened successfully");

    char buffer[BUFFER_SIZE];					// Create a character array for incoming data
    
    /* Main listen loop */
    while (1) {
        int read_bytes = read_uart(uart_fd, buffer, BUFFER_SIZE - 1);
   
	if (read_bytes > 0) { 						// Append a null terminator and print command if msg received 
            buffer[read_bytes] = '\0'; 
            char log_message[BUFFER_SIZE + 50]; 	
            sprintf(log_message, "Received command: %s", buffer); 
            log_info(log_message);           
        }
    }
	
    parse_command(buffer);
    close_uart(uart_fd); 
    log_info("UART port closed"); 
    close_log(); 

    return 0;
}
