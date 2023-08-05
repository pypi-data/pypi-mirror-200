#ifndef ELEMENTPROPERTIES_H
#define ELEMENTPROPERTIES_H

#include <stdio.h>  // due to printf
#include <stdlib.h> //due to exit

#include "contact_quadrature.h"

struct ElementProperties {
	int type;
	int nsd;
	int npd;
	int nes;
	int nsn;
	int nen;
	int nnd;
	int ned;
	int nvd;
	int* ISN;
	double* H;
	double* dH;
	int nqp;
	Quadrature quadrature;
};

typedef struct ElementProperties ElementProperties;

void elementProperties(ElementProperties* elementProperties, int type, int qOrder);

void sfd2(double* H, double* dH, double r);
void sfd4(double* H, double* dH, double r, double s);
void sfd6(double* H, double* dH, double r, double s);
void sfd8(double* H, double* dH, double r, double s);

void freeElementProperties(ElementProperties* elementProperties);

#endif // ELEMENTPROPERTIES_H
