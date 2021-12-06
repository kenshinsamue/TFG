
#include <vector>
#include <fstream>
#include <iostream>
// clases 
#include "Neuron.hpp"
#include "Red.hpp"
using namespace std;

int main (void){

  fstream file;
  file.open("format.txt",fstream::in);

  string cadena;
  file >> cadena;
  unsigned size = stoi(cadena);
  vector <unsigned> topologia;
  for (unsigned i = 0; i<size;i++){
    file>>cadena;
    if(cadena != " "&& cadena!="\n"){
      topologia.push_back(stoi(cadena));
    }
  }
  Red neuronal (topologia);

  vector<double> inputVals;
  vector<double> targetVals;
  vector<double> resultVals;
  inputVals.push_back(1.0);
  inputVals.push_back(1.0);
  inputVals.push_back(1.0);
  inputVals.push_back(1.0);
  // introducimos los valores iniciales
  neuronal.feedForward(inputVals);

  targetVals.push_back(10.0);
  targetVals.push_back(15.0);

  // aprendizaje
  neuronal.backProp(targetVals);
  // ejecutamos la red neuronal para obtener los valores resultantes
  neuronal.getResults(resultVals);

  for(int i =0 ; i<resultVals.size();i++){
    cout<<"i: "<<resultVals[i]<<endl;
  }
}