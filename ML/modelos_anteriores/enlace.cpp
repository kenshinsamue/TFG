#include "enlace.h"

Enlace::Enlace(){
    weigh =1;
}
Enlace::~Enlace(){}

void Enlace::SetPar(Neuron* a, Neuron* b){
    A=a;
    B=b;
}
