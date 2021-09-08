
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
    ObtenerCapa(pos)->InserNeurona();
  }
}