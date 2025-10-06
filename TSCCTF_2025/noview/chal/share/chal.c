#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX 0x20

void init(void){
	setvbuf(stdin, 0, 2, 0);
	setvbuf(stdout, 0, 2, 0);
	setvbuf(stderr, 0, 2, 0);
}

void menu(void){
	puts("1. add note");
	puts("2. delete note");
	puts("3. edit note");
	puts("4. copy note");
	puts("5. exit");
	printf("> ");
}

void* notes[MAX];
int sizes[MAX];

void add(void){
	int size = 0, idx = 0;
	printf("index > ");
	scanf("%d", &idx);
	printf("size > ");
	scanf("%d", &size);
	if (idx < 0 || idx >= MAX){
		puts("invalid!");
	}else{
		sizes[idx] = size;
		notes[idx] = malloc(size);
	}
}

void delete(void){
	int idx = 0;
	printf("index > ");
	scanf("%d", &idx);
	if (notes[idx]){
		free(notes[idx]);
	}
}

void edit(void){
	int size = 0, idx = 0;
	printf("index > ");
	scanf("%d", &idx);
	getchar();
	if (!notes[idx]){
		puts("invalid!");
		return;
	}

	printf("content > ");
	read(0, notes[idx], sizes[idx]);
}

void copy(){
	int idx1 = 0, idx2 = 0;
	printf("index1 > ");
	scanf("%d", &idx1);
	getchar();
	printf("inde2 > ");
	scanf("%d", &idx2);
	getchar();
	
	if (notes[idx1] && notes[idx2]){
		memcpy(notes[idx1], notes[idx2], sizes[idx2]);
	}else puts("invalid!");
}

int main(){
	init();
	int choice = 0;
	char buf[0x8];
	while(1){
		menu();
		read(0, buf, 0x8);
		choice = atoi(buf);
		switch(choice){
			case 1:
				add();
				break;
			case 2:
				delete();
				break;
			case 3:
				edit();
				break;
			case 4:
				copy();
				break;
			case 5:
				exit(0);
				break;
			default:
				puts("invalid!");
		}
	}
	return 0;
}
