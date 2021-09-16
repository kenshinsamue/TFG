
#ifndef NEURONA_
#define NEURONA_

#include "enlace.h"
#include <vector>
class Neuron{

  public:
    Neuron();
    ~Neuron();
    Neuron(bool);
    void setEnlaceAnterior(Enlace* a);
    void setEnlaceSiguiente(Enlace* a);
    
  private:
    bool bias;
    std::vector<Enlace*> anteriores;
    std::vector<Enlace*> siguientes;

};
#endif