#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

void init(void);
void menu(void);
void create(void);
void delete(void);
void edit(void);
void show(void);

struct note{
	char *content;
	bool in_used;
	unsigned long size;
};

struct note notes[0x20];

int main(){
	char option[2];
	init();
	while(1){
		menu();
		read(0, option, 2);
		switch(option[0]){
		case '1':
			create();
			break;
		case '2':
			delete();
			break;
		case '3':
			edit();
			break;
		case '4':
			show();
			break;
		case '5':
			exit(0);
			break;
		}
	}
	return 0;
}

void init(void){
	setvbuf(stdin, 0, 2, 0);
	setvbuf(stdout, 0, 2, 0);
	setvbuf(stderr, 0, 2, 0);
	memset(notes, 0, sizeof(notes));
}

void menu(void){
	puts("1. create note");
	puts("2. delete note");
	puts("3. edit note");
	puts("4. show note");
	puts("5. exit");
	puts("your choice: ");
}

void create(void){
	int idx, size = 0;
	printf("Index: ");
	scanf(" %d", &idx);
	if(idx < 0 || idx >= 0x20 || notes[idx].in_used){
		printf("Bad hacker!\n");
		exit(0);
	}
	printf("Size: ");
	scanf(" %d", &size);
	if(size > 0x100){
		printf("Too large!\n");
		exit(0);
	}else if(size < 0){
		printf("Bad hacker!\n");
		exit(0);
	}
	notes[idx].content = malloc(size);
	notes[idx].in_used = 1;
	notes[idx].size = size;
	printf("Success!\n");
}

void delete(void){
	int idx;
	printf("Index: ");
	scanf(" %d", &idx);
	if(idx < 0 || idx >= 0x20 || !notes[idx].in_used){
		printf("Bad hacker!\n");
		exit(0);
	}
	free(notes[idx].content);
	notes[idx].content = NULL;
	notes[idx].in_used = 0;
	notes[idx].size = 0;
	printf("Success!\n");
}

void edit(void){
	int idx, size = 0;
	printf("Index: ");
	scanf(" %d", &idx);
	if(idx < 0 || idx >= 0x20 || !notes[idx].in_used){
		printf("Bad hacker!\n");
		exit(0);
	}
	printf("Size: ");
	scanf(" %d", &size);
	getchar();
	if(size < 0 || size > notes[idx].size){
		printf("Bad hacker!\n");
		exit(0);
	}
	printf("Content: ");
	read(0, notes[idx].content, size);
	*(notes[idx].content + size) = 0;
}

void show(void){
	int idx;
	printf("Index: ");
	scanf(" %d", &idx);
	if(idx < 0 || idx >= 0x20 || !notes[idx].in_used){
		printf("Bad hacker!\n");
		exit(0);
	}
	printf("note %d: %s", idx, notes[idx].content);	
}
