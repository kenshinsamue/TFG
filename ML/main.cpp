
#include <vector>
#include <fstream>
#include <iostream>
#include <algorithm>
#include <bitset>
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
#define CSV "-C"
string nombre_configuracion ="";

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

void ParsearMAC(string &MAC){
  string tmp = "";
  char puntos = ':';
  for (int i=0;i<MAC.size();i++){
    if(MAC[i]!=puntos){
      tmp+=MAC[i];
    }
  }
  MAC = tmp;
}

double TraduccirHex(char H){
  double valor =0;
  switch (H){
  case '0':
    valor = 0;
    break;
  case '1':
    valor = 1;
    break;
  case '2':
    valor = 2;
    break;
  case '3':
    valor = 3;
    break;
  case '4':
    valor = 4;
    break;
  case '5':
    valor = 5;
    break;
  case '6':
    valor = 6;
    break;
  case '7':
    valor = 7;
    break;
  case '8':
    valor = 8;
    break;
  case '9':
    valor = 9;
    break;
  case 'A':
    valor = 10;
    break;
  case 'B':
    valor = 11;
    break;
  case 'C':
    valor = 12;
    break;
  case 'D':
    valor = 13;
    break;
  case 'E':
    valor = 14;
    break;
  case 'F':
    valor = 15;
    break;
  default:
    valor =-1;
    break;
  }
  return valor;
}

void HexToDouble(string HEX,vector<double>& vector){
  int Valor_caracter =0;
  int valor=0;
  int mascara = 8;
  while(HEX.length()!=0){
    Valor_caracter = TraduccirHex(HEX[0]);
    for(int i=0;i<4;i++){
      valor = Valor_caracter & mascara;
      valor = valor>>(4-(i+1));
      mascara = mascara >> 1;
      vector.push_back(valor);
    }
    mascara=8;
    HEX.erase(0,1);
  }
}

void ObtenerValorCSV(fstream& fs, vector<double>& my_vector,vector<double>& resultados){
  string linea, MAC,clk,resultado,objetivo;
  int valor;
  getline(fs,linea);
  stringstream ss(linea);
  ss>>resultado;
  MAC = resultado.substr(0,17);

  ParsearMAC(MAC);
  HexToDouble(MAC,my_vector);
  clk = resultado.substr(18,8);
  HexToDouble(clk,my_vector);

  objetivo = resultado.substr(27,32);
  HexToDouble(objetivo,resultados);
}


void EntrenarCSV (Red &neuronal,string RSC_IN){
  // leemos los inputs del fichero 
  fstream inputs = fstream(RSC_IN,fstream::in);
  string encabezado;
  // string nombreConfiguracionResultados = "log_";
  // leemos los resultados para ese input
  vector<double> inputVals,targetVals,resultVals;
  getline(inputs,encabezado);
  while(!inputs.eof()){
    ObtenerValorCSV(inputs,inputVals,targetVals);
    // introducimos los valores 
    for(int i=0;i<inputVals.size();i++){
     std::cout <<"\033[1;34m"<<inputVals[i]<<"\033[0m ";
    }
    neuronal.feedForward(inputVals);

    std::cout<<"-> ";
    for(int i=0;i<targetVals.size();i++){
     std::cout <<"\033[1;32m"<<targetVals[i]<<"\033[0m ";
    }
    std::cout<<"| Resultado: ";
    // obtenemos los resultados 
    neuronal.getResults(resultVals);
    for(int i=0;i<resultVals.size();i++){
     std::cout <<"\033[1;36m"<<resultVals[i]<<"\033[0m ";
    }
    std::cout<<"| margen de error: ";
    // entrenamos 
    neuronal.backProp(targetVals);
    std::cout<<endl<<"\033[1;91m"<<neuronal.getRecentAverageError()<<"\033[0m"<<endl;
    inputVals.clear();
    targetVals.clear();
    resultVals.clear();
  }
  // nombreConfiguracionResultados +=neuronal.Get_n_cap_ocultas();
  // ofstream resultados = ofstream(nombreConfiguracionResultados,std::ios_base::app);
  // resultados<<neuronal.getRecentAverageError()<<endl;
  neuronal.SafeConfig(nombre_configuracion);
  inputs.close();
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
     std::cout <<"\033[1;34m"<<inputVals[i]<<"\033[0m ";
    }
    neuronal.feedForward(inputVals);

   std::cout<<"-> ";
    for(int i=0;i<targetVals.size();i++){
     std::cout <<"\033[1;32m"<<targetVals[i]<<"\033[0m ";
    }
   std::cout<<"| Resultado: ";
    // obtenemos los resultados 
    neuronal.getResults(resultVals);
    for(int i=0;i<resultVals.size();i++){
     std::cout <<"\033[1;36m"<<resultVals[i]<<"\033[0m ";
    }
   std::cout<<"| margen de error: ";
    // entrenamos 
    neuronal.backProp(targetVals);
   std::cout<<"\033[1;91m"<<neuronal.getRecentAverageError()<<"\033[0m"<<endl;
    inputVals.clear();
    targetVals.clear();
    resultVals.clear();
  }
  neuronal.SafeConfig(nombre_configuracion);
  inputs.close();
}
void Computar(Red &neuronal,string RSC_IN){

  fstream inputs = fstream(RSC_IN,fstream::in);
  vector<double> inputVals,targetVals,resultVals;
  while(!inputs.eof()){
    ObtenerValor(inputs,inputVals);
    for(int i=0;i<inputVals.size();i++){
     std::cout <<"\033[1;34m"<<inputVals[i]<<"\033[0m ";
    }
    neuronal.feedForward(inputVals);

   std::cout<<"-> ";
   std::cout<<"| Resultado: ";
    // obtenemos los resultados 
    neuronal.getResults(resultVals);
    for(int i=0;i<resultVals.size();i++){
     std::cout <<"\033[1;36m"<<resultVals[i]<<"\033[0m ";
    }
   std::cout<<endl;
    inputVals.clear();
  }
  inputs.close();
  
}
void help(){
 std::cout<<"Ayuda de ejecucion del programa"<<endl;
 std::cout<<"Para la ejecucion se leeran dos ficheros: "<<endl;
   std::cout<<"\t1) Para cargar el layout/plantilla de la red neuronal esta seguira el siguiente patron:"<<endl;
     std::cout<<"\t\t[numero de capas]\n\t\t[numero neuronas capa 1] [numero neuronas capa 2] [numero neuronas capa 3] ..."<<endl;
     std::cout<<"\t\t Por defecto el nombre del fichero que se leera para la plantilla de la red es 'format.txt'"<<endl;
   std::cout<<"\t2) Para cargar el fichero Inputs o informacion de entrada: "<<endl;
     std::cout<<"\t\tPor defecto se leera el fichero con el objetivo de obtener resultados, es decir, la opcion b"<<endl;
     std::cout<<"\t\tPor defecto el nombre del fincero de entrada a leer es 'Inputs.txt'"<<endl;
     std::cout<<"\t\ta) Para la lectura de Inputs con el objetivo de entrenar la red se sigue el siguiente formato:"<<endl;
       std::cout<<"\t\t\t[valor entrada 1] [valor entrada 2] [valor entrada 3] [valor entrada 4] ...."<<endl;
       std::cout<<"\t\t\t[valor salida  1] [valor salida  2] [valor salida  3] ..."<<endl;
     std::cout<<"\t\tb) Para la lectura de Inputs con el objetivo de obtener directamente los resultados con la red ya entrenada"<<endl;
       std::cout<<"\t\t\t[valor entrada 1] [valor entrada 2] [valor entrada 3] [valor entrada 4] ...."<<endl;
     std::cout<<"\t\t Para la lectura de los fichero se tendra en cuenta que el numero de valores de entrada coinciden"<<endl;
     std::cout<<"\t\t con el numero de neuronas de la primera capa, de la misma forma el numero de valores de salida "<<endl;
     std::cout<<"\t\t con el del numero de neuronas en la ultima capa\n"<<endl;
 std::cout<<"Los parametros que se podran leer son los siguientes : \n"<<endl;
   std::cout<<"\t -h : Se mostrara esta guia de uso"<<endl;
   std::cout<<"\t -l [nombre fichero]: Se leera el fichero especificado que contendra la plantilla de la red "<<endl;
   std::cout<<"\t -t : Se establecera el modo de entrenamiento de la red"<<endl;
   std::cout<<"\t -i [nombre fichero]: Se establece el nombre del fichero con los inputs de la red"<<endl;
   std::cout<<"\t -c [nombre fichero]: Se cargara la configuracion de la red"<<endl;
   std::cout<<"\t -C [nombre fichero]: Se encarga de leer los inputs desde un fichero CSV"<<endl;
}


string layout = "format.txt";
bool entrenar = false;
string input = "Inputs.txt";
string config = "config.txt";
string csvfile ="";

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
  return topologia;
}
void leerArgumentos(int size,char* arg[],Red &mi_red,bool &csv){
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
      cout<<"Encontrado fichero de configuracion"<<endl;
      auto it = std::find(argumentos.begin(), argumentos.end(), CONFIG);
      int index = it - argumentos.begin();
      config = argumentos[index+1];
      cout<<"El fichero se llama: "<<config<<endl;
      nombre_configuracion = config;
    }
    if(std::find(argumentos.begin(),argumentos.end(),CSV)!= argumentos.end()){
      auto it = std::find(argumentos.begin(),argumentos.end(),CSV);
      csv = true;
      int index = it - argumentos.begin();
      csvfile = argumentos[index +1];
    }
    vector<unsigned> formato = leerLayout();
    mi_red = Red(formato);
    
    if(config!=""){                             // verificamos que el nombre del fichero existe
      ifstream file (config);
      if(file.peek()!=ifstream::traits_type::eof()){  // en caso de que el fichero NO este vacio
        mi_red.SetWeight(config);                     // lo cargamos
        std::cout<<"Se termino de cargar"<<endl;
      }
    }
      
  }
}

int main(int argc, char* argv[]) {
  Red mi_red= Red();
  bool csv =false;
  leerArgumentos(argc,argv,mi_red,csv);
  if(entrenar==true){
    if(csv==true){
      std::cout<<"entramos"<<endl;
      EntrenarCSV(mi_red,csvfile);
    }
    else{
      Entrenar(mi_red,input);
    }
  }
  else{
    Computar(mi_red,input);
  }
  return 0;
}