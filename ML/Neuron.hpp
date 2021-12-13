#include <vector>
#include <cstdlib>
#include <cmath>
#include <iostream>
#ifndef Neuronas
#define Neuronas

using namespace std;

struct Conexion{
    double weight;
    double deltaweight;
};
class Neuron;

typedef vector<Neuron>Layer;

class Neuron{

  public:
    Neuron(unsigned numSalidas, unsigned Indice);
    void feedForward(Layer &prevLayer);
    void calcOutputGradients(double targetVals);
    void calcHiddenGradients(Layer &sigCapa);
    void setOutputVal(double val){ m_outputVal = val;}
    double getOutputVal(){return m_outputVal;}
    void updateInputWeights (Layer &prevCapa);
  private:
    double sumaDOW(Layer &sigCapa);
    static double eta;
    static double alpha;
    double m_outputVal;
    unsigned m_myIndex;
    double m_gradient;
    vector<Conexion>m_outputWeights;
    static double transferFucntion(double x){
      // esta funcion se encarga de aplicar una funcion a un valor dado para ajustarlo al un rango de valores predeterminados
      // en este caso usamos la funcion tangente para obteenr valores desde -1 hasta 1 
      return tanh(x);
    }
    static double transferFucntionDerivada(double x){
      // esta funcion se encarga de retornar la derivada de la funcion anteriormente usada  
      return 1.0-(x * x);
    }
    static double randomWeight(){return rand()/double(RAND_MAX);}

};

#endif