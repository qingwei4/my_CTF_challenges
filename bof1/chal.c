#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void backdoor(void){
	execve("/bin/sh", 0, 0);
}

int main(){
	setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    char article[0x100];
	char author[0x10];

	printf("author:");
	read(0, author, 0x10);
	printf("content(max length of content is 0x100):");
	gets(article);
	printf("Here is your article!\n");
	printf("author: %s", author);
	printf("content: %s", article);
	
	return 0;
}