#include <stdio.h>
#include <math.h>
#include <fenv.h>

float sum(int range) {
  float sum = 0.0;

  for (int i = 0; i < range; i++) {
    sum = sum + 1.0;
  }
  return sum;
}

/* https://en.wikipedia.org/wiki/Kahan_summation_algorithm */
float bkSum(int range) {
  float sum = 0.0;
  float comp = 0.0;
  float oldsum, y;

  for (int i = 0; i < range; i++) {
    y = 1.0 - comp;
    oldsum = sum;
    sum = oldsum + y; /* when oldsum is big, the low-order digits of y are lost */
    comp = (sum - oldsum) - y; /* sum-oldsum cancels high-order part of y */
    //printf("%.7f %.7f %.7f %.7f\n", y, comp, sum, oldsum);
  }
  return sum;
}

// alternative version
float compSum(int range) {
  float sum = 0.0;
  float comp = 0.0;
  float oldsum;

  for (int i = 0; i < range; i++) {
    comp = comp + 1.0;
    oldsum = sum;
    sum = oldsum + comp;
    comp = (oldsum - sum) + comp;
  }
  return sum;
}

int main() {
    int range = ((int)1e8);

    //fesetround(FE_TOWARDZERO);
    printf("naive: %.7f, compensated: %.7f, compensated2: %.7f\n", sum(range), bkSum(range), compSum(range));
}
