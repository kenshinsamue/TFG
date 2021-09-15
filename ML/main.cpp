#include "red.h"
#include <iostream>



int main(void){
  RedNeuronal* red_neuronal = new RedNeuronal(); 
  // leer el numero de capas y guardarlo
  int capas = 0;
  red_neuronal->InsertCapas(capas);
  // obtenemos el numero de neuronas y la capa 
  int numero_neuronas =0;
  int capa =0;
  red_neuronal->InsertNeuronas(numero_neuronas,capa);
  red_neuronal->ConectarNeuronas();
  red_neuronal->InsertarBias();
}