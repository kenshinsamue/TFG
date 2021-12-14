#include "Neuron.hpp"
#include <iostream> 
#include <vector>
#include <cassert>
#include <fstream>
#ifndef RED_
#define RED_
using namespace std;
class Red{

  public:
    Red(){}
    Red(const vector<unsigned> &topologia);
    void feedForward(vector<double> &inputVals);
    void backProp(vector<double> &targetVals);
    void getResults(vector<double> &resultVals);
    double getRecentAverageError(){return m_recentAverageError;}
    void SetWeight(string configFile){}
    void SafeConfig(){
      ofstream fichero =ofstream("config.txt");
      fichero<<m_layer.size()<<endl;
      
      for(int i=0;i<m_layer.size();i++){          // Para cada capa
        fichero<<m_layer[i].size()<<endl;
        for(int j=0;j<m_layer[i].size();j++){     // para cada neurona
          fichero<<m_layer[i][j].getConections().size()<<endl;
          for(int k=0;k<m_layer[i][j].getConections().size(); k++){ // para cada elemento de la conexion
            fichero<<"[ "<<m_layer[i][j].getConections().at(k).weight<<" "<<m_layer[i][j].getConections().at(k).deltaweight<<" ]";
          }
          fichero<<endl;
        }
      }
      fichero.close();
    }
  private:
    double m_error;
    double m_recentAverageError;
    static double m_recentAverageSmoothingFactor;
    vector<Layer> m_layer;
};

#endif