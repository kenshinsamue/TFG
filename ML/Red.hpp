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
    void SetWeight(string configFile){
      ifstream fichero = ifstream(configFile);
      string linea;
      vector<Conexion> conexiones;
      Conexion conexion_tmp;
      unsigned size,size_neuronas,size_conexiones;
      double weight, prevweigh;
      fichero>>linea;
      // cout<<linea<<endl;
      size = stoi(linea);
      for(int i = 0; i<size;i++){
        fichero>>linea;
        // cout<<linea<<endl;
        size_neuronas = stoi(linea);
        for (int j =0; j<size_neuronas;j++){
          fichero>>linea;
          // cout<<linea<<endl;
          size_conexiones = stoi(linea);
          conexiones.clear();
          for(int k = 0; k<size_conexiones;k++){
            fichero>>linea;
            // cout<<linea<<endl;
            if (linea=="["){
              // cout<<"conexion: "<<k<<endl;

              fichero>>linea;
              // cout<<"weight: "<<linea<<" ";
              weight = stod(linea);
              
              fichero>>linea;
              // cout<<" previous weight: "<<linea<<endl;
              prevweigh = stod(linea);

              conexion_tmp = Conexion();
              conexion_tmp.weight = weight;
              conexion_tmp.deltaweight = prevweigh;
              conexiones.push_back(conexion_tmp);

              fichero>>linea; // "]"
            }
          }

          m_layer[i][j].setConections(conexiones);

        }
      }
      fichero.close();
      mostrar();
    }
    void SafeConfig(){
      ofstream fichero =ofstream("config.txt");
      fichero<<m_layer.size()<<endl;
      
      for(int i=0;i<m_layer.size();i++){          // Para cada capa
        fichero<<m_layer[i].size()<<endl;
        for(int j=0;j<m_layer[i].size();j++){     // para cada neurona
          fichero<<m_layer[i][j].getConections().size()<<endl;
          for(int k=0;k<m_layer[i][j].getConections().size(); k++){ // para cada elemento de la conexion
            fichero<<"[ "<<m_layer[i][j].getConections().at(k).weight<<" "<<m_layer[i][j].getConections().at(k).deltaweight<<" ] ";
          }
          fichero<<endl;
        }
      }
      fichero.close();
    }
    void mostrar(){
      for(int i=0;i<m_layer.size();i++){          // Para cada capa
        cout<<m_layer[i].size()<<endl;
        for(int j=0;j<m_layer[i].size();j++){     // para cada neurona
          cout<<m_layer[i][j].getConections().size()<<endl;
          for(int k=0;k<m_layer[i][j].getConections().size(); k++){ // para cada elemento de la conexion
            cout<<"[ "<<m_layer[i][j].getConections().at(k).weight<<" "<<m_layer[i][j].getConections().at(k).deltaweight<<" ] ";
          }
          cout<<endl;
        }
      }
    }
  private:
    double m_error;
    double m_recentAverageError;
    static double m_recentAverageSmoothingFactor;
    vector<Layer> m_layer;
};

#endif