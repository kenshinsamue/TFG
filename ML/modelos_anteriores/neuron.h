
#ifndef NEURONA_
#define NEURONA_
class Enlace;
class Capa;
#include "enlace.h"
#include <vector>
#include <cmath>
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
    double TransferFunctionDerivative (double);
    double TransferFunction(double);
    void calcularOutputGrandients(double);
    void calcularGradiantesOcultos(Capa*);
    double Neuron::sumDoW(Capa* capa);
    double getgradient(){return m_gradient;}
    void actualizarInputs(Capa*);
  private:
    bool bias;
    std::vector<Enlace*> anteriores;
    std::vector<Enlace*> siguientes;
    double valor;
    double m_gradient;

};
#endif