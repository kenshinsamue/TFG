#include "neuron.h"

Neuron::Neuron(){
    bias=false;
}
Neuron::Neuron(bool is_bias){
  bias=is_bias;
}
Neuron::~Neuron(){}
double Neuron::sumDoW(Capa* capa){
  double suma =0.0;
  for(unsigned n = 0 ; n<capa->GetNeuronas().size()-1;++n){
    suma += siguientes[n]->GetWeigh() * capa->GetNeurona(n)->getgradient();
  }
  return suma;
}
void Neuron::calcularGradiantesOcultos(Capa* siguienteCapa){
  double dow = sumDoW(siguienteCapa);
  m_gradient= dow * TransferFunctionDerivative(valor);
}

void Neuron::calcularOutputGrandients(double target){
  double delta = target - valor;
  m_gradient = delta * TransferFunctionDerivative(valor);
}

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
  valor = TransferFunction(sum);
}
double Neuron::TransferFunctionDerivative(double value){
  return 1.0 - value * value;  
}
double Neuron::TransferFunction(double value){
  return tanh(value);
}

void Neuron::actualizarInputs(Capa* capa){
  int size = capa->GetNeuronas().size();
  for(unsigned n = n<size;++n){
    Neuron* neurona = capa->GetNeurona(n);
    double DeltaAntiguo = neurona->
  }
}
