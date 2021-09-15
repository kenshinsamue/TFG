#ifndef ENLACE_
#define ENLACE_

#include "vector"
#include "tuple"
#include "neuron.h"

class Enlace{
  public:
    Enlace();
    ~Enlace();
    void SetPar(Neuron*,Neuron*);
  private:
    std::vector<std::tuple<Neuron*,Neuron*>> par;
    double weigh;

};
#endif