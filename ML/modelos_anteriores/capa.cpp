#include "capa.h"
#include <iostream>
Capa::Capa(){}
Capa::~Capa(){}
void Capa::SetBias(Neuron* bias){
    Bias = bias;
}
void Capa::InsertNeurona(){

    neuronas.push_back(new Neuron);
}
int Capa::GetNumeroNeuronas(){
    return neuronas.size();
}
Neuron* Capa::GetNeurona(int pos){
    return neuronas[pos];
}
std::vector<Neuron*> Capa::GetNeuronas(){
    return neuronas;
}