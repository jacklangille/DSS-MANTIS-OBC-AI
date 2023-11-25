#include "parse.h"
#include <stdio.h>
#include <string.h>
void parse_command(const char *command){
	if (strcmp(command, WAKE) == 1){
		printf("wake"); // call wake routine
	}
	else if(strcmp(command, SLEEP) == 0){
		printf("sleep"); // call sleep routine
	}
	else if(strcmp(command, IMAGE_RX) == 0){
		printf("image_rx"); // call image receive routine
	}
	else if(strcmp(command, RESULTS_TX) == 0){
		printf("results_tx"); // call transmit results routine
	}
	else if(strcmp(command, INF_1_START) == 0){
		printf("inf_1_start"); // call inference 1 routine 
	}
	else if(strcmp(command, INF_2_START) == 0){
		printf("inf_2_start"); // call inference 2 routine 
	}
	else if(strcmp(command, EMERG_STOP) == 0){
		printf("emerg_stop"); // call emergency stop routine
	}
}


