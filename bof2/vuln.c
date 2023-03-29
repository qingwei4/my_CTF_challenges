#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(){
	char buf[0x10];
	printf("Please input your message.\n");
	read(0, buf, 0x100);
	printf("your message: %s\n", buf);
	printf("Do you want to edit the message?\n");
	char option = getchar();
	getchar();
	if(option == 'y'){
		read(0, buf, 0x100);
		printf("your message: %s\n", buf);
	}
	return 0;
}
