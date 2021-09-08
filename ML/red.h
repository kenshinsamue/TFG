#ifndef RED_NEURONAL
#define RED_NEURONAL
#include "capa.h"
#include <vector>
class RedNeuronal{
  public:
    RedNeuronal();
    ~RedNeuronal();
    void NuevaCapa();
    void InsertCapas(int num);
    void InsertNeuronas(int neuronas,int pos);
    Capa* ObtenerCapa(int pos);
  private:
    std::vector<Capa*> capas;


};


#endif