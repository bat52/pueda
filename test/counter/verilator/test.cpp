#include <iostream>
#include "tests.h"

int main(int argc, char** argv, char** env) {

    int retval=EXIT_SUCCESS;
    retval = test_all();
    exit(retval);
    
}