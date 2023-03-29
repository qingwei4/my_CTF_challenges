#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(){
	char buf[0x10];
	printf("Please input your message.\n");
	scanf(" %s", buf);
	getchar();
	printf("your message: ");
	printf(buf);
	printf("\n");
	printf("Do you want to edit the message?\n");
	char option = getchar();
	getchar();
	printf("%c", option);
	if(option == 'y'){
		scanf(" %s", buf);
		printf("your message: %s\n", buf);
	}
	return 0;
}
