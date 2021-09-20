
#include "red.h"


RedNeuronal::RedNeuronal(){}

RedNeuronal::~RedNeuronal(){}

void RedNeuronal::Forward(std::vector <double> inputs){
  assert(inputs.size() == capas[0]->GetNeuronas().size());
  // Inicializamos los valores de las neuronas de la primera capa
  for(unsigned i =0 ; i< inputs.size();i++){
    capas[0]->GetNeurona(i)->setValor(inputs[i]);
  }

  for(unsigned i =1 ; i<capas.size(); ++i ){
    for(unsigned j =0; j<capas[i]->GetNeuronas().size();++j){
      capas[i]->GetNeurona(j)->forward();
    } 
  }
}
void RedNeuronal::Imprimir(){
  for(int i=0;i<capas.size();i++){
    std::cout<<"Capa: "<<i<<std::endl<<std::endl;
    std::vector<Neuron*> neuronas = capas[i]->GetNeuronas(); 
    if(i==capas.size()-1){
      for(int j = 0;j<neuronas.size();j++){
        std::cout<<"O"<<std::endl;
      }
      
    }
    else{
      
      for(int j=0; j<neuronas.size();j++){
        Neuron* neurona = neuronas[j];
        std::vector<Enlace*> enlace = neurona->getEnlaces();
        for(int k=0 ;k<enlace.size();k++){
          std::cout<<"N --"<<" "<<"--->"<<"N"<<std::endl;
        }
        std::cout<<std::endl;
      }
      Neuron* bias =  capas[i]->GetBias();
      std::vector<Enlace*> enlace = bias->getEnlaces();
      for(int k=0 ;k<enlace.size();k++){
        std::cout<<"B --"<<" "<<"--->"<<"N"<<std::endl;
      }
      std::cout<<std::endl;
    }
    

  }
}

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

  for(int i=1; i<capas.size();i++){
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