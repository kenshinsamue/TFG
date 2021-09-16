#include "neuron.h"

Neuron::Neuron(){
    bias=false;
}
Neuron::Neuron(bool is_bias){
  bias=is_bias;
}
Neuron::~Neuron(){}

void Neuron::setEnlaceAnterior(Enlace* link){
  anteriores.push_back(link);
}

void Neuron::setEnlaceSiguiente(Enlace* link){
  siguientes.push_back(link);
}