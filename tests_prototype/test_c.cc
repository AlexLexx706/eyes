#include "stdio.h"

#define ROT_LEFT(val)    ((val << 2)  |  (val >> 6))
unsigned char crc8_light(char *buf, int buf_length)
{
    // printf("buf_length:%d\n", buf_length);
	unsigned char res = 0;
	while (buf_length--) {
		res = ROT_LEFT(res)  ^  (unsigned char)(*buf++);
	}
	return ROT_LEFT(res);
}

int main() {
    char data[] = "1231345311213425236235743673223411356ujhgfdcwdqdberth";
    printf("res:%d\n", crc8_light(data, sizeof(data) - 1));
    return 0;
}