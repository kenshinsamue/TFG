#ifndef CAPA_NEURONAS
#define CAPA_NEURONAS
#include "neuron.h"
#include <vector>
class Capa{

  public:

    Capa();
    ~Capa();
    void InsertNeurona();
    int GetNumeroNeuronas();
    Neuron* GetNeurona(int);
    void SetBias(Neuron*);
  private:
    std::vector<Neuron*> neuronas;
    Neuron* Bias;
};

#endif