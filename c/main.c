#include <stdio.h>
#include <locale.h>
#include <string.h>
#include <pcre.h>

#include "parser.h"

int main(int argc, const char* argv[]) {
    if (argc == 2) {
        char* code = NULL;
        FILE* f = fopen(argv[1], "r");

        if (f != NULL) {
            fseek(f, 0, SEEK_END);
            size_t length = ftell(f);
            fseek(f, 0, SEEK_SET);

            size_t cur = 0;
            code = (char*)calloc(length + 1, sizeof(char));

            char* buffer = (char*)calloc(128, sizeof(char));
            while (fgets(buffer, 127, f) != NULL) {
                strncpy(code + cur, buffer, strlen(buffer));
                cur = ftell(f) - 1;
            }
            free(buffer);

            // Parsing
            const unsigned char* tables = NULL;
            setlocale(LC_CTYPE, (const char*)"ru.");
            tables = pcre_maketables();

            parse(code);

            pcre_free((void*)tables);
        } else {
            printf("Can't open file %s\n", argv[1]);
        }
        fclose(f);
    } else {
        printf("Unknown file name\n");
    }

    return 0;
}
