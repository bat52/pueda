#include <stdio.h>
#include <stdlib.h> // for EXIT_SUCCESS
#include "dut.h"

////////// DUT functions extensions //////////////////////////////

int test_count_down()
{
    uint8_t index, count;
    for(index=15; index>0; index--)
        {
            count = read_count();                        
            if( count != index) 
                {
                printf("INDEX: %d, COUNT: %d\n", index, count);
                return(EXIT_FAILURE);
                }
            clock_tick();
        }
    
    return(EXIT_SUCCESS);
}
/////////////// C tests top ///////////////////////////

int test_all()
{
    int retval = EXIT_SUCCESS;
    
    dut_init();

    retval = test_count_down();

    dut_close();

    return(retval);
}