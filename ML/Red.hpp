#include "Neuron.hpp"
#include <iostream> 
#include <vector>
#include <cassert>
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
  private:
    double m_error;
    double m_recentAverageError;
    static double m_recentAverageSmoothingFactor;
    vector<Layer> m_layer;
};

#endif