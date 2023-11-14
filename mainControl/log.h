#ifndef LOG_H 
#define LOG_H 

void init_log();

void log_info(const char *message);

void log_error(const char *message);

void close_log();

#endif 
