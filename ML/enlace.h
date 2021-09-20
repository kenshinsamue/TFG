#ifndef ENLACE_
#define ENLACE_
class Neuron;
#include "neuron.h"

class Enlace{
  public:
    Enlace();
    ~Enlace();
    void setValor(double);
    void SetPar(Neuron*,Neuron*);
    Neuron* GetA(){return A;}
    Neuron* GetB(){return B;}
    double GetWeigh(){return weigh;}
  private:
    Neuron* A;
    Neuron* B;
    double weigh;
    

};
#endif