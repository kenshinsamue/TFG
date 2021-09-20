
#ifndef NEURONA_
#define NEURONA_
class Enlace;
class Capa;
#include "enlace.h"
#include <vector>
class Neuron{

  public:
    Neuron();
    ~Neuron();
    Neuron(bool);
    void setEnlaceAnterior(Enlace* a);
    void setEnlaceSiguiente(Enlace* a);
    std::vector<Enlace*> getEnlaces();
    void setValor(double);
    double getValor();
    void forward();
    
  private:
    bool bias;
    std::vector<Enlace*> anteriores;
    std::vector<Enlace*> siguientes;
    double valor;

};
#endif