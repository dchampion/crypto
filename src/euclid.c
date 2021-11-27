#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <stdbool.h>

void swap(int* a, int* b);
int gcd_r(int a, int b);
int gcd_i(int a, int b);
int gcdx_r(int a, int b, int* x, int* y);
int gcdx_i(int a, int b, int* x, int* y);
int inverse(int a, int b, bool recurse);

/**
 * Driver code for the Euclidean algorithms. Make this code executable using a C (or C++)
 * compiler specific to the platform you wish to run it on; i.e. gcc (or g++) euclid.c -o euclid.
 * 
 * Usage: euclid a b (where a and b are the positive integer values for which to compute
 * the greatest common divisor, and the modular multiplicative inverse of a modulo b.)
 * 
 * Example:
 * $ ./euclid 60 7
 * GCD of 7 and 60     (via recursion) is 1
 * GCD of 7 and 60     (via iteration) is 1
 * Inverse of 60 mod 7 (via recursion) is 43
 * Inverse of 60 mod 7 (via iteration) is 43
 */
int main(int argc, char** argv) {
    
    if (argc < 3) {
        printf("Usage: %s a b\n", argv[0]);
        exit(1);
    }

    int a = strtol(argv[1], (char**)NULL, 10);
    int b = strtol(argv[2], (char**)NULL, 10);

    swap(&a, &b);

    printf("GCD of %d and %d     (via recursion) is %d\n", a, b, gcd_r(a, b));
    printf("GCD of %d and %d     (via iteration) is %d\n", a, b, gcd_i(a, b));
    printf("Inverse of %d mod %d (via recursion) is %d\n", b, a, inverse(a, b, true));
    printf("Inverse of %d mod %d (via iteration) is %d\n", b, a, inverse(a, b, false));
}

/**
 * Enforces left-to-right, increasing order of parameters a and b.
 */
void swap(int* a, int* b) {
    if (*b < *a) {
        int temp = *a;
        *a = *b;
        *b = temp;
    }
}

/**
 * Recursive implementation of the Euclidean algorithm.
 * 
 * @param a A positive integer
 * @param b A positive integer
 * 
 * @return The greatest common divisor (GCD) of a and b
 */
int gcd_r(int a, int b) {
    assert(a >= 0);
    assert(b >= 0);
    
    if (b == 0) {
        return a;
    }

    swap(&a, &b);

    return gcd_r(a, b % a);
}

/**
 * Iterative implementation of the Euclidean algorithm.
 * 
 * @param a A positive integer
 * @param b A positive integer
 * 
 * @return The greatest common divisor of a and b
 */
int gcd_i(int a, int b) {
    assert(a >= 0);
    assert(b >= 0);

    do {
        swap(&a, &b);
        b = b % a;

    } while (b != 0);
    
    return a;
}

/**
 * Recursive implementation of the extended Euclidean algorithm.
 * 
 * @param a A positive integer
 * @param b A positive integer
 * @param x The x integer solution to Bezout's identity; i.e., the modular
 * multiplicative inverse of a modulo b
 * @param y The y integer solution to Bezout's identity
 * 
 * @return int The greatest common divisor of a and b
 */
int gcdx_r(int a, int b, int* x, int *y) {
    assert(a >= 0);
    assert(b >= 0);

    if (b == 0) {
        *x = 0;
        *y = 1;
        return a;
    }

    swap(&a, &b);

    int x1, y1;
    int gcd = gcdx_r(a, b % a, &x1, &y1);

    *x = y1 - (b / a) * x1;
    *y = x1;
    
    return gcd;
}

/**
 * Iterative implementation of the extended Euclidean algorithm.
 * 
 * @param a 
 * @param b 
 * @param x The x integer solution to Bezout's identity; i.e., the modular
 * multiplicative inverse of a modulo b
 * @param y The y integer solution to Bezout's identity
 * 
 * @return int The greatest common divisor of a and b
 */
int gcdx_i(int a, int b, int* x, int* y) {
    assert(a >= 0);
    assert(b >= 0);

    swap(&a, &b);

    int a1 = 1, b1 = 0, x1 = 1, y1 = 0;
    do {
        int quot = a / b;
        
        int temp = b;
        b = a - quot * b;
        a = temp;
        
        temp = a1;
        a1 = y1 - quot * a1;
        y1 = temp;
        
        temp = b1;
        b1 = x1 - quot * b1;
        x1 = temp;
    
    } while (b != 0);
    
    *x = x1;
    *y = y1;
    
    return a;
}

/**
 * Returns the modular multiplicative inverse of parameter a modulo b.
 * 
 * @param a A positive integer
 * @param b A positive integer
 * @param recurse If true, this function calls the recursive implementation
 * of the extended Euclidean algorithm; otherwise it calls the iterative implementation
 * 
 * @return int The modular multiplicative inverse of a modulo b; or -1 if none exists
 */
int inverse(int a, int b, bool recurse) {
    assert(a >= 0);
    assert(b >= 0);

    int x, y;
    int gcd = recurse ? gcdx_r(a, b, &x, &y) : gcdx_i(a, b, &x, &y);
    if (gcd == 1) {
        return ((x % b) + b) % b; 
    }
    return -1;
}