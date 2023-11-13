#include "log.h"
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

static FILE *log_file = NULL; // Declare a static file pointer. Initialize it to NULL.

void init_log() {
    log_file = fopen("uart_communication.log", "a"); // Open the log file in append mode
    if (log_file == NULL) {
        perror("Failed to open log file");
        exit(EXIT_FAILURE);
    }
}

void log_message(const char *message, const char *log_level) {
    /*
    Helper function for logging messages. Take message to log and level of logging.
    */
    if (log_file != NULL) {
        // Get the current time for the log timestamp
        time_t now = time(NULL);
        char *time_str = ctime(&now); // Convert to string
        time_str[24] = '\0';  // Remove new line character 

        fprintf(log_file, "[%s] %s: %s\n", time_str, log_level, message);
        fflush(log_file); // Flush buffer
    }
}

void log_info(const char *message) {
    log_message(message, "INFO");
}

void log_error(const char *message) {
    log_message(message, "ERROR");
}

void close_log() {
    if (log_file != NULL) {
        fclose(log_file);
        log_file = NULL;
    }
}
