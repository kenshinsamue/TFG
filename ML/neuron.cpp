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
std::vector<Enlace*> Neuron::getEnlaces(){
  return siguientes;
}

void Neuron::setValor(double val){
  valor = val;
}
double Neuron::getValor(void){
  return valor;
}
void Neuron::forward(){

  double sum =0.0;
  for(unsigned n =0;n<anteriores.size();++n){
    sum+= anteriores[n]->GetA()->getValor() * anteriores[n]->GetWeigh();
  }
}
