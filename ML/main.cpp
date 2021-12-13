
#include <vector>
#include <fstream>
#include <iostream>
#include <algorithm>
// clases 
#include "Neuron.hpp"
#include "Red.hpp"
#include <sstream>
using namespace std;
#define HELP "-h"
#define LAYOUT "-l"
#define TRAIN "-t"
#define INPUT "-i"
#define CONFIG "-c"


void ObtenerValor(fstream& fs,vector<double>& my_vector){
  string linea,valor;
  getline(fs,linea);
  stringstream ss(linea);
  double valor_obtenido=0.0;
  while(!ss.eof()){
    ss>>valor;
    valor_obtenido = stod(valor);
    my_vector.push_back(valor_obtenido);
  }
}

void Entrenar (Red &neuronal,string RSC_IN){
  // leemos los inputs del fichero 
  fstream inputs = fstream(RSC_IN,fstream::in);

  // leemos los resultados para ese input
  vector<double> inputVals,targetVals,resultVals;
  while(!inputs.eof()){
    ObtenerValor(inputs,inputVals);
    ObtenerValor(inputs,targetVals);
    
    // introducimos los valores 
    for(int i=0;i<inputVals.size();i++){
      cout <<"\033[1;34m"<<inputVals[i]<<"\033[0m ";
    }
    neuronal.feedForward(inputVals);

    cout<<"-> ";
    for(int i=0;i<targetVals.size();i++){
      cout <<"\033[1;32m"<<targetVals[i]<<"\033[0m ";
    }
    cout<<"| Resultado: ";
    // obtenemos los resultados 
    neuronal.getResults(resultVals);
    for(int i=0;i<resultVals.size();i++){
      cout <<"\033[1;36m"<<resultVals[i]<<"\033[0m ";
    }
    cout<<"| margen de error: ";
    // entrenamos 
    neuronal.backProp(targetVals);
    cout<<"\033[1;91m"<<neuronal.getRecentAverageError()<<"\033[0m"<<endl;
    inputVals.clear();
    targetVals.clear();
    resultVals.clear();
  }
  
  inputs.close();
}
void Computar(Red &neuronal,string RSC_IN){

  fstream inputs = fstream(RSC_IN,fstream::in);
  vector<double> inputVals,targetVals,resultVals;
  while(!inputs.eof()){
    ObtenerValor(inputs,inputVals);
    for(int i=0;i<inputVals.size();i++){
      cout <<"\033[1;34m"<<inputVals[i]<<"\033[0m ";
    }
    neuronal.feedForward(inputVals);

    cout<<"-> ";
    cout<<"| Resultado: ";
    // obtenemos los resultados 
    neuronal.getResults(resultVals);
    for(int i=0;i<resultVals.size();i++){
      cout <<"\033[1;36m"<<resultVals[i]<<"\033[0m ";
    }
  }
  inputs.close();
  
}
void help(){
  cout<<"Ayuda de ejecucion del programa"<<endl;
  cout<<"Para la ejecucion se leeran dos ficheros: "<<endl;
    cout<<"\t1) Para cargar el layout/plantilla de la red neuronal esta seguira el siguiente patron:"<<endl;
      cout<<"\t\t [numero de capas]\n\t\t[numero neuronas capa 1] [numero neuronas capa 2] [numero neuronas capa 3] ..."<<endl;
      cout<<"\t\t Por defecto el nombre del fichero que se leera para la plantilla de la red es 'format.txt'"<<endl;
    cout<<"\t2) Para cargar el fichero Inputs o informacion de entrada: "<<endl;
      cout<<"\t\tPor defecto se leera el fichero con el objetivo de obtener resultados, es decir, la opcion b"<<endl;
      cout<<"\t\tPor defecto el nombre del fincero de entrada a leer es 'Inputs.txt'"<<endl;
      cout<<"\t\ta) Para la lectura de Inputs con el objetivo de entrenar la red se sigue el siguiente formato:"<<endl;
        cout<<"\t\t\t[valor entrada 1] [valor entrada 2] [valor entrada 3] [valor entrada 4] ...."<<endl;
        cout<<"\t\t\t[valor salida  1] [valor salida  2] [valor salida  3] ..."<<endl;
      cout<<"b) Para la lectura de Inputs con el objetivo de obtener directamente los resultados con la red ya entrenada"<<endl;
        cout<<"\t\t\t[valor entrada 1] [valor entrada 2] [valor entrada 3] [valor entrada 4] ...."<<endl;
      cout<<"\t\t Para la lectura de los fichero se tendra en cuenta que el numero de valores de entrada coinciden"<<endl;
      cout<<"\t\t con el numero de neuronas de la primera capa, de la misma forma el numero de valores de salida "<<endl;
      cout<<"\t\t con el del numero de neuronas en la ultima capa"<<endl;
  cout<<"Los parametros que se podran leer son los siguientes : "<<endl;
    cout<<"\t -h : Se mostrara esta guia de uso"<<endl;
    cout<<"\t -l [nombre fichero]: Se leera el fichero especificado que contendra la plantilla de la red "<<endl;
    cout<<"\t -t : Se establecera el modo de entrenamiento de la red"<<endl;
    cout<<"\t -i [nombre fichero]: Se establece el nombre del fichero con los inputs de la red"<<endl;
    cout<<"\t -c [nombre fichero]: Se cargara la configuracion de la red"<<endl;
}


string layout = "format.txt";
bool entrenar = false;
string input = "Inputs.txt";
string config = "";
vector<unsigned> leerLayout(){
// Abrimos el formato de la red y la aplicamos a la red
  fstream file;
  file.open(layout,fstream::in);

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
}
void leerArgumentos(int size,char* arg[],Red* mi_red){
  vector<string> argumentos;
  if(size==1){
    help();
    exit(1);
  }
  else{
    for(int i =1; i<size; i++){
      argumentos.push_back(arg[i]);
    }
  }
  if ( std::find(argumentos.begin(), argumentos.end(), HELP) != argumentos.end() ){
    help();
    exit(0);
  }
  else{
    
    if(std::find(argumentos.begin(), argumentos.end(), LAYOUT) != argumentos.end()){
      auto it = std::find(argumentos.begin(), argumentos.end(), LAYOUT);
      int index = it - argumentos.begin();
      layout = argumentos[index+1];
    }
    if(std::find(argumentos.begin(), argumentos.end(), TRAIN) != argumentos.end()){
      entrenar = true;
    }
    if(std::find(argumentos.begin(), argumentos.end(), INPUT) != argumentos.end()){
      auto it = std::find(argumentos.begin(), argumentos.end(), INPUT);
      int index = it - argumentos.begin();
      input = argumentos[index+1];
    }
    if(std::find(argumentos.begin(), argumentos.end(), CONFIG) != argumentos.end()){
      auto it = std::find(argumentos.begin(), argumentos.end(), CONFIG);
      int index = it - argumentos.begin();
      input = argumentos[index+1];
    }
    vector<unsigned> formato = leerLayout();
    mi_red = new Red(formato);
    if(config!="")
      mi_red->SetWeight(config);
  }
}

int main(int argc, char* argv[]) {
  Red* mi_red= new Red();
  leerArgumentos(argc,argv,mi_red);
  if(entrenar==true){
    Entrenar(*mi_red,input);
  }
  else{
    Computar(*mi_red,input);
  }
  
}