#include "pico/multicore.h"
#include "pico/stdlib.h"
#include <stdio.h>

#define FLAG_VALUE 123

extern void mash3();

void core1_entry() {

  multicore_fifo_push_blocking(FLAG_VALUE);

  uint32_t g = multicore_fifo_pop_blocking();

  if (g != FLAG_VALUE)
    printf("Hmm, that's not right on core 1!\n");
  else
    printf("Its all gone well on core 1!");

  mash3();

  while (1)
    tight_loop_contents();
}

int main() {
  stdio_init_all();

  mash3();

  // multicore_launch_core1(core1_entry);

  // uint32_t g = multicore_fifo_pop_blocking();

  // if (g != FLAG_VALUE)
  //   printf("Hmm, that's not right on core 0!\n");
  // else {
  //   multicore_fifo_push_blocking(FLAG_VALUE);
  //   printf("It's all gone well on core 0!");
  // }

  while (1)
    tight_loop_contents();

  return 0;
}
