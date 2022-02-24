#include "Neuron.hpp"
double Neuron::eta = 0.2;
double Neuron::alpha = 0.5;

Neuron::Neuron(unsigned numSalidas, unsigned Indice){
  // creamos una conexion de salida y le asignamos un peso aleatorio
  // ademas de un identificador pasado por parametro
  for(unsigned c = 0; c<numSalidas;c++){
  m_outputWeights.push_back(Conexion());
  m_outputWeights.back().weight = randomWeight();
  }
  m_myIndex = Indice;
}
/**
 * feedForward obtiene una capa de neuronas y calcula los valores de salida en funcion de
 * los valores de salida de las neuronas de la capa anterior y la funcion de transformacion 
 * 
*/
void Neuron::feedForward(Layer &prevLayer){
  double suma = 0.0;
  for(unsigned i = 0 ; i < prevLayer.size(); i++){
    suma+=prevLayer[i].getOutputVal() * prevLayer[i].m_outputWeights[m_myIndex].weight;
  }
  m_outputVal = Neuron::transferFucntion(suma);
}
/**
 * Este metodo recibe los valores objetivos. Calcula la diferencia
 * entre estos valores y los resultantes, para posteriormente multiplicarlos 
 * por la derivada de la tangente del valor resultante 
*/
void Neuron::calcOutputGradients(double targetVals){
  double delta = targetVals - m_outputVal;
  m_gradient = delta * Neuron::transferFucntionDerivada(m_outputVal);
}

void Neuron::calcHiddenGradients(Layer &sigCapa){
  double dow = sumaDOW(sigCapa);
  m_gradient = dow * Neuron::transferFucntionDerivada(m_outputVal);
}

void Neuron::updateInputWeights (Layer &prevCapa){
  // eta : es el rango de aprendizaje comun ( overall learning rate ) min 0 -> 1 max
    // 0.0 lento
    // 0.2 medio
    // 1.0 excesivamente rapido
  // alpha : es el momento, es decir una fraccion del delta antiguo
    // 0.0 no hay 
    // 0.5 fraccion moderada
  for(unsigned i = 0; i < prevCapa.size(); i++){
    Neuron &neurona = prevCapa[i];
    double prevDeltaWeight = neurona.m_outputWeights[m_myIndex].deltaweight;
    double nuevoDeltaWeight = eta * neurona.getOutputVal() * m_gradient 
                            + alpha* prevDeltaWeight;
    neurona.m_outputWeights[m_myIndex].deltaweight = nuevoDeltaWeight;
    neurona.m_outputWeights[m_myIndex].weight += nuevoDeltaWeight;
  }
}

double Neuron::sumaDOW(Layer &sigCapa){
  double suma = 0.0;
  for(unsigned i=0; i< sigCapa.size()-1;i++)
    suma+= m_outputWeights[i].weight * sigCapa[i].m_gradient;
  return suma;
}