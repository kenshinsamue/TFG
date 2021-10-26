#ifndef RED_NEURONAL
#define RED_NEURONAL
#include "capa.h"
// #include "enlace.h"
#include <vector>
#include <iostream>
#include <cassert>
class RedNeuronal{
  public:
  // constructor 
    RedNeuronal();
    ~RedNeuronal();
    void Forward(std::vector<double>);
    void NuevaCapa();
    void InsertCapas(int num);
    void InsertNeuronas(int neuronas,int pos);
    Capa* ObtenerCapa(int pos);
    void ConectarNeuronas ();
    void InsertarBias();
    void BackProp(const std::vector<double> &);
    void Imprimir();
  private:
    std::vector<Capa*> capas;
    std::vector<Enlace*> enlaces;
    double m_error;
    double m_recentAverageError;
    static double m_recentAverageSmoothingFactor;

};


#endif