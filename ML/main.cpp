#include "red.h"
#include <iostream>
#include <fstream>


int main(int argc, char *argv[]){


  std::fstream fichero ("format.txt",std::fstream::in);
  RedNeuronal* red_neuronal = new RedNeuronal(); 
  // // leer el numero de capas y guardarlo
  int capas = 0;
  fichero>>capas;
  red_neuronal->InsertCapas(capas);
  // // obtenemos el numero de neuronas y la capa 
  int numero_neuronas =0;
  
  
  for (int i =0 ;i<capas;i++){
    fichero>>numero_neuronas;
    red_neuronal->InsertNeuronas(numero_neuronas,i);

    // std::cout<<numero_neuronas<<std::endl;
  }
  red_neuronal->ConectarNeuronas();
  red_neuronal->InsertarBias();
  std::vector<double> valores;
  valores.push_back(1.0);
  valores.push_back(1.0);
  valores.push_back(1.0);
  valores.push_back(1.0);
  red_neuronal->Forward(valores);
  red_neuronal->Imprimir();
}