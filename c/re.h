//
// Created by admin on 12.09.2020.
//

#ifndef STACK_VM_RE_H
#define STACK_VM_RE_H

#include <stdlib.h>
#include <string.h>
#include <pcre.h>

typedef struct {
    char** list;
    size_t count;
} find_t;

void clear_find_t(find_t* find) {
    for (size_t i = 0; i < find->count; ++i) {
        free(find->list[i]);
    }
    free(find);
}

find_t* re_findall(const char* pattern, char* str, size_t list_length) {
    pcre* re;
    int options = 0;
    const char* err;
    int err_offset;
    re = pcre_compile((char*)pattern, options, &err, &err_offset, NULL);

    if (re) {
        int offset = 0;
        int count = 0;
        int ovector[12];

        find_t* find = (find_t*)malloc(sizeof(find));
        find->count = 0;
        find->list = (char**)calloc(list_length, sizeof(char*));

        while ((count = pcre_exec(re, NULL, (char*)str, strlen(str), offset, 0, ovector, 12)) > 0) {
            for (int c = 0; c < 2 * count; c += 2) {
                if (ovector[c] >= 0) {
                    offset = ovector[c+1];

                    find->list[find->count] = (char*)calloc(ovector[c+1] - ovector[c] + 1, sizeof(char));
                    strncpy(find->list[find->count], str + ovector[c], ovector[c+1] - ovector[c] + 1);

                    ++find->count;
                }
            }
        }

        return find;
    }

    pcre_free((void*)re);
    return NULL;
}

#endif //STACK_VM_RE_H
