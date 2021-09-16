
#include "red.h"


RedNeuronal::RedNeuronal(){}

RedNeuronal::~RedNeuronal(){}

// Insertamos las capas de la red
void RedNeuronal::InsertCapas(int num){
  for(int i=0;i<num;i++){
    NuevaCapa();
  }
}

// Insertamos una nueva capa dentro de la red
void RedNeuronal::NuevaCapa(){
  Capa* capa = new Capa();
  capas.push_back(capa);
}


// Obtiene el puntero a una capa 
Capa* RedNeuronal::ObtenerCapa(int pos){
  return capas[pos];
}

// dado una capa, insertamos una cantidad determinada de neuronas
void RedNeuronal::InsertNeuronas(int n, int pos){
  for(int i =0;i<n;i++){
    ObtenerCapa(pos)->InsertNeurona();
  }
}
void RedNeuronal::ConectarNeuronas(){
  std::vector<Neuron*> a;
  std::vector<Neuron*> b;
  for(int i=1; capas.size();i++){
    a=capas[i-1]->GetNeuronas();
    b=capas[i]->GetNeuronas();
    for(auto primera : a){
      for(auto segunda: b){
        Enlace* link = new Enlace();
        link->SetPar(primera,segunda);
        primera->setEnlaceSiguiente(link);
        segunda->setEnlaceAnterior(link);
      }
    }
  }
}
void RedNeuronal::InsertarBias(){
  
  for (int i=0; i<capas.size()-1;i++){

    Neuron* bias = new Neuron(true);
    capas[i]->SetBias(bias);
    std::vector<Neuron*> siguientes = capas[i+1]->GetNeuronas();
    for(auto a:siguientes){
      Enlace* link = new Enlace();
      link->SetPar(bias,a);
      bias->setEnlaceSiguiente(link);
      a->setEnlaceAnterior(link);
    }
  }
  
}