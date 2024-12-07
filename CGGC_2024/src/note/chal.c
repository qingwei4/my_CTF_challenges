#include <stdio.h>
#include <stdlib.h>

#define MAX 0x10

typedef struct note{
	void *content;
	int size;
}note;

note notes[0x10];

void menu(void){
	puts("1. add note");
	puts("2. delete note");
	puts("3. show note");
	puts("4. edit note");
	puts("5. exit");
	printf("your choice: ");
	return;
}

void input(void *addr, int len){
	int current = 0;
	while (current <= len){
		read(0, addr, 1);
		char ch = *(char*)addr;
		if (ch == '\n')break;
		addr++;
		current++;
	}
	return;
}

void add_note(){
	int idx = -1, size = 0;
	printf("Note index: ");
	scanf("%d", &idx);
	if (idx < 0 || idx >= MAX || notes[idx].content){
		puts("Nope");
		return;
	}
	printf("Size: ");
	scanf("%d", &size);
	getchar();
	if (size < 0 || size > 0x68){
		puts("Nope");
		return;
	}
	notes[idx].content = (void*)malloc(size);
	notes[idx].size = size;
	puts("Done!");
	return;
}

void delete_note(){
	int idx = -1;
	printf("Note index: ");
	scanf("%d", &idx);
	if (idx < 0 || idx >= MAX || !notes[idx].content){
		puts("Nope");
		return;
	}
	free(notes[idx].content);
	notes[idx].content = NULL;
	notes[idx].size = 0;
	puts("Done!");
	return;
}
void show_note(){
	int idx = -1;
	printf("Note index: ");
	scanf("%d", &idx);
	if (idx < 0 || idx >= MAX || !notes[idx].content){
		puts("Nope");
		return;
	}
	printf("%s\n", notes[idx].content);
	puts("Done!");
	return;
}
void edit_note(){
	int idx = -1;
	printf("Note index: ");
	scanf("%d", &idx);
	getchar();
	if (idx < 0 || idx >= MAX || !notes[idx].content){
		puts("Nope");
		return;
	}
	printf("Content: ");
	input(notes[idx].content, notes[idx].size);
	puts("Done!");
	return;
}

void bye(void){
	puts("Bye!");
	exit(0);
}

int main(){
	setvbuf(stdin, 0, 2, 0);
	setvbuf(stdout, 0, 2, 0);
	while (1){
		menu();
		char choice[0x2];
		read(0, choice, 2);
		switch (atoi(choice)){
			case 1:
				add_note();
				break;
			case 2:
				delete_note();
				break;
			case 3:
				show_note();
				break;
			case 4:
				edit_note();
				break;
			case 5:
				bye();
				break;
			default:
				puts("No such choice!");
		}
	}
	return 0;
}
