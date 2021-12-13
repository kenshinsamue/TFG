#include <vector>
#include <fstream>
#include <iostream>
#include <cassert>
using namespace std ;

struct enlace{
  double weight;
  double delta_weight;
};
////////////////////////////////////// Neurona

class Neurona{

  public:
    Neurona(int id_){
      id = id_;
      output_value=0.0;
    }
    Neurona(){
      output_value=0.0;
    }
    void CrearConexion(){
      struct enlace nuevo_enlace;
      conexion.push_back(nuevo_enlace);
    }
    void setOutput(double valor){
      output_value = valor;
    } 
    void feedforward(Capa* capa_anterior){
      
    }
  private:
    vector<enlace> conexion;
    int id;
    double output_value;
};


////////////////////////////////////// Capa //////////////////////////
class Capa{
  public:
    Capa(){}
    void InsertarNeurona(Neurona* nueva_neurona ){
      neuronas.push_back(nueva_neurona);
    }
    vector<Neurona*>* GetNeuronas(){return &neuronas;}
    int size(){
      return neuronas.size();
    }
    void InsertarBias(Neurona* bias_){
      Bias = bias_;
    }
    Neurona* GetNeurona(int pos){
      return neuronas[pos];
    }
  private:
    vector<Neurona*> neuronas;
    Neurona* Bias;
};

////////////////////////////////////// Red //////////////////////////


class Red {
  public:
    Red (){}
    void InsertarCapas(int numero_capas){
      Capa* nueva;
      for(int i=0;i<numero_capas;i++){
        nueva = new Capa();
        capas.push_back(nueva);
      }
    }
    void InsertarNeuronas(int numero, int index){
      Neurona* neurona_actual;
      for(int i=0;i<numero;i++){
        neurona_actual = new Neurona(i);
        capas[index]->InsertarNeurona(neurona_actual);
      }
    }
    void ConectarNeuronas(){
      for (int i=0;i<capas.size()-1;i++){
        vector<Neurona*>* capa_actual = capas[i]->GetNeuronas();
        for(int j = 0;j<capa_actual->size();j++){
          Neurona* neurona_actual = (*capa_actual)[j];
          for(int k = 0;k<capas[i+1]->size();i++){
            neurona_actual->CrearConexion();
          }
        }
      } 
    }
    void CrearBias(){
      Neurona* bias;
      for(int i = 0; i<capas.size()-1;i++){
        bias = new Neurona();

        for(int j=0;j<capas[i]->size()-1;j++)
          bias->CrearConexion();
        
        capas[i]->InsertarBias(bias);
      }
    }
    void Fordward(vector<double> inputs){
      assert(inputs.size() == capas[0]->size());
      for(unsigned i =0 ;i<inputs.size();i++){
        capas[0]->GetNeurona(i)->setOutput(inputs[i]);
      }

      for(unsigned i =1;i <capas.size();i++){
        Capa* anterior = capas[i-1];
        for(unsigned j =0 ; j<capas[i]->size()-1;j++){
          capas[i]->GetNeurona(j)->feedforward(anterior);
        } 
      }

    }
  private:
    vector<Capa*> capas;

};

////////////////////////////////////// Main


int main(int argc, char *argv[]){

  fstream fichero ("format.txt",fstream::in);
  Red* red_neuronal = new Red; 
  //  Leemos el numero de capas que usara la red neuronal
  int capas =0;
  fichero >> capas;
  red_neuronal->InsertarCapas(capas);

  // creando el numero de neuronas en cada capa
  int numero_neuronas =0;

  for(int i=0; i<numero_neuronas;i++){
    fichero >> numero_neuronas;
    red_neuronal->InsertarNeuronas(numero_neuronas,i);
  }

  // Conectamos todas las neuronas 
  red_neuronal->ConectarNeuronas();
  // Crear y conectar las BIAS
  red_neuronal->CrearBias();
  // Carga de inputs
  vector<double> valores;
  valores.push_back(1.0);
  valores.push_back(1.0);
  valores.push_back(1.0);
  valores.push_back(1.0);
  red_neuronal->Fordward(valores);
}


