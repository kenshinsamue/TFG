
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
  for(int i=1;i<capas.size();i++){
    Enlace*  link = new Enlace();
    for(int a=0 ; a<capas[i-1]->GetNumeroNeuronas();a++){
      for(int b=0 ; b<capas[i]->GetNumeroNeuronas();b++){
        link->SetPar(capas[i-1]->GetNeurona(a),capas[i-1]->GetNeurona(b)); 
      }
    }
    enlaces.push_back(link);
  }
}
void RedNeuronal::InsertarBias(){
  for (int i=0; i<capas.size()-1;i++){
    Neuron* bias = new Neuron();
    capas[i]->SetBias(bias);
    for(int j=0;j<capas[i+1]->GetNumeroNeuronas();j++){
      Enlace* link = new Enlace();
      link->SetPar(bias, capas[i+1]->GetNeurona(j));
      enlaces->push_back(link);
    }
  }
  
}