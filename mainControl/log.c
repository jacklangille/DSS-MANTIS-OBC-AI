/*
Function definitions for logging capability.
*/

#include "log.h" // Header file
#include <stdio.h> // Standard input/output operations
#include <stdlib.h> // Standard library header 
#include <time.h> // Header for time related functions

static FILE *log_file = NULL; // Declare static file pointer, initialized to NULL. Only accessible in this file.

void init_log() {
    /* Opens a file named "communication.log" for writing.
    If fopen fails (indicated by log_file being NULL), it prints an error message and exits the program. */
    log_file = fopen("communication.log", "w"); 
    if (log_file == NULL) {
        perror("Failed to open log file");
        exit(EXIT_FAILURE);
    }
}

void log_message(const char *message, const char *log_level) {
    /*
    Inputs: 
    *message = pointer to message to log.
    *log_level = logging level. e.g. INFO, ERROR, etc.
    */
    if (log_file != NULL) { // Ensure file exists
        time_t now = time(NULL); // Get current time 
        char *time_str = ctime(&now); // Convert to string
        time_str[24] = '\0';  // Remove new line character 

        fprintf(log_file, "[%s] %s: %s\n", time_str, log_level, message); // Write log message with time, message, and level
        fflush(log_file); // Flush buffer
    }
}

void log_info(const char *message) {
    /* Convenience/wrapper function with INFO level predefined. */
    log_message(message, "INFO");
}

void log_error(const char *message) {
    /* Convenience/wrapper function with ERROR level predefined. */
    log_message(message, "ERROR");
}

void close_log() {
    /* Close the log file and reset log_file pointer to NULL.
    Clean-up function to be called before the program exits. */
    if (log_file != NULL) {
        fclose(log_file);
        log_file = NULL;
    }
}
