#include "log.h"
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

static FILE *log_file = NULL; 

void init_log() {
    log_file = fopen("communication.log", "w"); 
    if (log_file == NULL) {
        perror("Failed to open log file");
        exit(EXIT_FAILURE);
    }
}

void log_message(const char *message, const char *log_level) {
    if (log_file != NULL) { // Ensure file exists
        time_t now = time(NULL); // Get current time 
        char *time_str = ctime(&now); // Convert to string
        time_str[24] = '\0';  // Remove new line character 

        fprintf(log_file, "[%s] %s: %s\n", time_str, log_level, message); // Format message
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
