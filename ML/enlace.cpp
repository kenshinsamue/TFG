#include "enlace.h"

Enlace::Enlace(){
    weigh =1;
}
Enlace::~Enlace(){}

void Enlace::SetPar(Neuron* a, Neuron* b){
    par.push_back(std::make_tuple(a,b));
}
