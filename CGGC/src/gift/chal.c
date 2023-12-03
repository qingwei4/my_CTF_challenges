#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(){
	char buf[0x20];
	u_int64_t *addr = NULL, value;
	setvbuf(stdin, 0, 2, 0);
	setvbuf(stdout, 0, 2, 0);
	puts("Here is a Gift for you!");
	printf("Give me a address: ");
	scanf("%llu", &addr);
	printf("Value: ");
	scanf("%llu", &value);
	getchar();
	*addr = value;
	puts("Try your best!");
	gets(&buf);
	puts("Bye!");
	return 0;
}
