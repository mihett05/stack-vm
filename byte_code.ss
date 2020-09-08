main:
    arr_new endl
    arr_push endl, '\n'

    mov i, 0

    while:
        lt i, 10

        jne end
            push i
            call itos
            call print

            push endl
            call print

            add i, 1
            pop i
        jmp while
    end: