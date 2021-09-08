#ifndef CAPA_NEURONAS
#define CAPA_NEURONAS
#include "neuron.h"
#include <vector>
class Capa{

  public:

    Capa();
    ~Capa();
    void InsertNeurona();
  private:
    Neuron* neurona;
    std::vector<Neuron*> neuronas;
};

#endif