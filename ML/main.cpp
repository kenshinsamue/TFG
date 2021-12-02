
#include <vector>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <cassert>
#include <cmath>

using namespace std;

struct Conexion{
    double weight;
    double deltaweight;
};
class Neuron;

typedef vector<Neuron>Layer;
//////////////// Clase Neurona ///////////////////


class Neuron{

  public:
    Neuron(unsigned numSalidas, unsigned Indice){
      // creamos una conexion de salida y le asignamos un peso aleatorio
      // ademas de un identificador pasado por parametro
      for(unsigned c = 0; c<numSalidas;c++){
        m_outputWeights.push_back(Conexion());
        m_outputWeights.back().weight = randomWeight();
      }
      m_myIndex = Indice;
    }
    void feedForward(Layer &prevLayer){
      double suma = 0.0;
      for(unsigned i =0 ; i<prevLayer.size();i++){
        suma+=prevLayer[i].getOutputVal() * prevLayer[i].m_outputWeights[m_myIndex].weight;
      }
      m_outputVal = Neuron::transferFucntion(suma);
    }
    void calcOutputGradients(double targetVals){
      double delta = targetVals-m_outputVal;
      m_gradient = delta * Neuron::transferFucntionDerivada(m_outputVal);
    }
    void calcHiddenGradients(Layer &sigCapa){
      double dow = sumaDOW(sigCapa);
      m_gradient = dow * Neuron::transferFucntionDerivada(m_outputVal);
    }
    void setOutputVal(double val){ m_outputVal = val;}
    double getOutputVal(){return m_outputVal;}
    void updateInputWeights (Layer prevCapa){
      // eta : es el rango de aprendizaje comun ( overall learning rate ) min 0 -> 1 max
        // 0.0 lento
        // 0.2 medio
        // 1.0 excesivamente rapido
      // alpha : es el momento, es decir una fraccion del delta antiguo
        // 0.0 no hay 
        // 0.5 fraccion moderada

      for(unsigned i= 0;i<prevCapa.size();i++){
        Neuron &neurona = prevCapa[i];
        double prevDeltaWeight = neurona.m_outputWeights[m_myIndex].deltaweight;
        double nuevoDeltaWeight = eta * neurona.getOutputVal() * m_gradient 
                                + alpha* prevDeltaWeight;
        neurona.m_outputWeights[m_myIndex].deltaweight = nuevoDeltaWeight;
        neurona.m_outputWeights[m_myIndex].weight += nuevoDeltaWeight;
      }
    }
  private:
    double sumaDOW(Layer &sigCapa){
      double suma = 0.0;
      for(unsigned i=0; i< sigCapa.size()-1;i++)
        suma+= m_outputWeights[i].weight * sigCapa[i].m_gradient;
      return suma;
    }
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

double Neuron::eta = 0.15;
double Neuron::alpha = 0.5;
/////// Red ////////////

class Red{

  public:
    Red(const vector<unsigned> &topologia){
      // Optenemos el tipo de topologia 
      unsigned numCapas = topologia.size();
      // Creamos las capas para que se ajuste a la topologia indicada
      for (unsigned indexCapa = 0; indexCapa < numCapas; indexCapa++){
        m_layer.push_back(Layer());
        unsigned numOutputs = indexCapa == topologia.size()-1 ? 0 : topologia[indexCapa +1];
        for (unsigned indexNeuron = 0 ; indexNeuron <= topologia[indexCapa];indexNeuron++){
          m_layer.back().push_back(Neuron(numOutputs,indexNeuron));
          // cout<<"Neurona creada"<<endl;
        }

        // el valor de salida de las neuronas es 1 por defecto
        m_layer.back().back().setOutputVal(1.0);     
      }
    }
    void feedForward(vector<double> &inputVals){
      assert(inputVals.size() == m_layer[0].size()-1);
      for(unsigned i = 0;i< inputVals.size();i++){
        m_layer[0][i].setOutputVal(inputVals[i]);
      }
      for(unsigned indexCapa = 1; indexCapa < m_layer.size();indexCapa++){
        Layer &prevCapa = m_layer[indexCapa -1 ];
        for(unsigned indexNeurona = 0; m_layer[indexCapa].size()-1;indexNeurona++ ){
          m_layer[indexCapa][indexNeurona].feedForward(prevCapa);
        }
      }
    }
    void backProp(vector<double> &targetVals){
      // calcular el error total 
      Layer &outputCapa = m_layer.back();
      m_error = 0.0;
      for (unsigned i = 0 ; i<outputCapa.size() -1 ; i++){
        double delta = targetVals[i] - outputCapa[i].getOutputVal();
        m_error += delta * delta;
      }
      m_error /=outputCapa.size()-1;
      m_error = sqrt(m_error);


      m_recentAverageError = (m_recentAverageError * m_recentAverageSmoothingFactor + m_error)
                            / (m_recentAverageError + 1.0);
      // calcular grandientes de las capas salientes

      for (unsigned i =0;i<outputCapa.size()-1;i++){
        outputCapa[i].calcOutputGradients(targetVals[i]);
      }
      // calcular los gradientes de las capas ocultas (intermedias)
      for (unsigned indexCapa = m_layer.size()-2; indexCapa>0;indexCapa--){
        Layer &capaOculta = m_layer[indexCapa];
        Layer &sigCapa = m_layer[indexCapa+1];
        for(unsigned i =0; i<capaOculta.size();i++){
          capaOculta[i].calcHiddenGradients(sigCapa);
        }
      }
      // actualizar los pesos de las conexiones desde las ultimas hasta las primeras capas

      for(unsigned indexCapa = m_layer.size() -1 ;indexCapa>0;indexCapa--){
        Layer &capa = m_layer[indexCapa];
        Layer &prevCapa = m_layer[indexCapa-1];
        for(unsigned i=0; i< prevCapa.size() -1 ;i++){
          capa[i].updateInputWeights(prevCapa);
        }
      }
    }
    void getResults(vector<double> &resultVals){
      resultVals.clear();
      for(unsigned i  =0 ; i<m_layer.back().size() -1 ;i++){
        resultVals.push_back(m_layer.back()[i].getOutputVal());
      }
    }
  private:
    double m_error;
    double m_recentAverageError;
    static double m_recentAverageSmoothingFactor;
    vector<Layer> m_layer;
};

double Red::m_recentAverageSmoothingFactor = 100.0;


int main (void){

  fstream file;
  file.open("format.txt",fstream::in);

  string cadena;
  file >> cadena;
  unsigned size = stoi(cadena);
  vector <unsigned> topologia;
  for (unsigned i = 0; i<size;i++){
    file>>cadena;
    if(cadena != " "&& cadena!="\n"){
      topologia.push_back(stoi(cadena));
    }
  }



  Red neuronal (topologia);

  vector<double> inputVals;
  vector<double> targetVals;
  vector<double> resultVals;

  // introducimos los valores iniciales
  neuronal.feedForward(inputVals);
  // aprendizaje
  neuronal.backProp(targetVals);
  // ejecutamos la red neuronal para obtener los valores resultantes
  neuronal.getResults(resultVals);
}