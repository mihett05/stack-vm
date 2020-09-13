//
// Created by admin on 13.09.2020.
//

#ifndef STACK_VM_PARSER_H
#define STACK_VM_PARSER_H

#include "re.h"

const char* re_op_code = "^\\s*(\\w+)(\\s+(.*)|)\\s*$";
const char* re_mark = "^\\s*(\\w+):\\s*$";


enum e_opcodes {
    o_mov
};

void print_err(size_t line, const char* err) {
    printf("Line: %d: %s\n", line + 1, err);
}

void parse(char* code) {
    size_t n = 0;
    char* line = strtok(code, "\n");

    

    while (line != NULL) {
        find_t* opcodes = re_findall(re_op_code, line, 4);
        if (opcodes->count == 4) {

        } else  {
            clear_find_t(opcodes);
            find_t* marks = re_findall(re_mark, line, 2);
            if (marks->count == 2 ) {

            } else {
                print_err(n, "Invalid syntax");
            }
        }

        line = strtok(NULL, "\n");
        ++n;
    }
}



#endif //STACK_VM_PARSER_H
