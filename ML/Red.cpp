

#include "Red.hpp"
double Red::m_recentAverageSmoothingFactor = 100.0;

Red::Red(const vector<unsigned> &topologia){
  // Optenemos el tipo de topologia 
  unsigned numCapas = topologia.size();
  // Creamos las capas para que se ajuste a la topologia indicada
  for (unsigned indexCapa = 0; indexCapa < numCapas; indexCapa++){
  m_layer.push_back(Layer());
  unsigned numOutputs;
  // unsigned numOutputs = indexCapa == topologia.size()-1 ? 0 : topologia[indexCapa +1];
  if (indexCapa == topologia.size()-1)
      numOutputs=0;
  else{
      numOutputs=topologia[indexCapa + 1];
  }
  
  for (unsigned indexNeuron = 0 ; indexNeuron <= topologia[indexCapa];indexNeuron++)
      m_layer.back().push_back(Neuron(numOutputs,indexNeuron));

  // el valor de salida de las neuronas es 1 por defecto
  m_layer.back().back().setOutputVal(1.0);     
  }
}

void Red::feedForward(vector<double> &inputVals){
  assert(inputVals.size() == m_layer[0].size()-1);
  for(unsigned i = 0;i< inputVals.size();i++){
    m_layer[0][i].setOutputVal(inputVals[i]);
  }
  for(unsigned indexCapa = 1; indexCapa < m_layer.size();indexCapa++){
    Layer &prevCapa = m_layer[indexCapa -1 ];
    for(unsigned indexNeurona = 0; indexNeurona < m_layer[indexCapa].size()-1;indexNeurona++ ){
      m_layer[indexCapa][indexNeurona].feedForward(prevCapa);
    }
  }
}

void Red::backProp(vector<double> &targetVals){
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

  for(unsigned indexCapa = m_layer.size() -1 ;indexCapa>0;indexCapa--){   // indice a la ultima capa
    Layer &capa = m_layer[indexCapa];   // ultima capa 
    Layer &prevCapa = m_layer[indexCapa-1];   // capa anterior
    for(unsigned i=0; i < capa.size() -1 ;i++)  // para cada una de las neuronas de la capa anterior 
      capa[i].updateInputWeights(prevCapa);     // actualizamos los datos
  }
}

void Red::getResults(vector<double> &resultVals){
  resultVals.clear();
  for(unsigned i  =0 ; i<m_layer.back().size() -1 ;i++){
    resultVals.push_back(m_layer.back()[i].getOutputVal());
  }
}