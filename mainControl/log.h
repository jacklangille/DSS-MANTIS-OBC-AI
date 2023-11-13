#ifndef LOG_H // Ensure LOG_H has not been defined
#define LOG_H // Define LOG_H

// Function to initialize the logging system
void init_log();

// Function to log an informational message
void log_info(const char *message);

// Function to log an error message
void log_error(const char *message);

// Function to close the logging system
void close_log();

#endif 
