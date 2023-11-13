#include "log.h"


int main(void){

    init_log(); 
    log_info("This is a test info message.");
    log_error("Test error message.");
    close_log();
    
    return 0;
}