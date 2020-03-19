# -*- coding: utf-8 -*-
##########################
####    工具类        ####
##########################


def log_title(title):
    print()
    print(f'--------   {title}    ----------')
    print()

def log_h1(h1):
    print()
    print()
    print(f'==========    {h1}    =============')
    print()
    print()

def log_h1_start(h1):
    print_newLine(8)
    print('=============================================================')
    print(f'====================    {h1}    =========================')
    print()

def log_h1_end(h1):
    print()
    print(f'================    {h1}    ===================')
    print('=============================================================')
    print_newLine(8)


def print_newLine(n):
    for i in range(n):
        print()


if __name__ == '__main__':
    log_title('test')