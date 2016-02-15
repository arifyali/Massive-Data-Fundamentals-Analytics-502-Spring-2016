#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc,char **argv)
{
#pragma omp parallel
    {
        // Code inside this region runs in parallel.
        printf("Greating from thread %d process %d\n",
               omp_get_thread_num(),getpid());
    }
    exit(0);
}
