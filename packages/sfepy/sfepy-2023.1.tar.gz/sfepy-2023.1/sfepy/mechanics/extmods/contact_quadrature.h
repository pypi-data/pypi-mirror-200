#ifndef CONTACT_QUADRATURE_H
#define CONTACT_QUADRATURE_H

#include <stdio.h>
#include <stdlib.h> // due to malloc and free
#include <math.h> // due to sqrt

struct Quadrature {
    int npd; // Number of Parametric Dimensions
    int nqp; // Number of Quadrature points
    double* qp; // Quadrature Points
    double* qw; // Quadrature Weights
};

typedef struct Quadrature Quadrature;

void  initQuadrature(Quadrature* quadrature, int npd, int nqp);
void  freeQuadrature(Quadrature* quadrature);

#endif // CONTACT_QUADRATURE_H
