#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "oven_utils.h"

#define OVEN_BUFFER_SIZE 65535 // Error occurs this value is small. Need bug fix.
#define OVEN_BUFFER_MARGIN 64

void oven_request_value(char var_name[])
{
    printf("@oven<|%s\n", var_name);
    fflush(stdout);    
}

void oven_request_array(char var_name[])
{
    printf("@oven.array<|%s\n", var_name);
    fflush(stdout);    
}

double oven_receive_double(char var_name[])
{
    char buffer[OVEN_BUFFER_SIZE];
    double x;
    oven_request_value(var_name);
    if (fgets(buffer, OVEN_BUFFER_SIZE, stdin) == NULL)
    {
        exit(1);
    }
    x = strtod(buffer, NULL);
    return x;
}

void oven_receive_double_array1d(char var_name[], double *array)
{
    long i, n;
    char buffer[OVEN_BUFFER_SIZE];
    char *endptr;
    unsigned int remaining;
    double x;
    oven_request_array(var_name);
    if (fgets(buffer, OVEN_BUFFER_SIZE, stdin) == NULL)
    {
        exit(1);
    }
    
    n = strtol(buffer, NULL, 10);
    endptr = buffer;
    for (i = 0; i < n; i++)
    {
        remaining = OVEN_BUFFER_SIZE-(endptr-buffer);
        if (i == 0 || (remaining < OVEN_BUFFER_MARGIN))
        {
            if (endptr-buffer > 0)
            {
                memmove(endptr, buffer, remaining);
                endptr = remaining + buffer;
            }
            if (fgets(endptr, OVEN_BUFFER_SIZE, stdin) == NULL)
            {
                exit(1);
            }
        }

        x = strtod(endptr, &endptr);
        if (*endptr == ',')
        {
            endptr++;
        }
        array[i] = x;
    }
}