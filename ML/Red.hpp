#include "Neuron.hpp"
#include <vector>
#include <cassert>
#ifndef RED_
#define RED_
using namespace std;
class Red{

  public:
    Red(const vector<unsigned> &topologia);
    void feedForward(vector<double> &inputVals);
    void backProp(vector<double> &targetVals);
    void getResults(vector<double> &resultVals);
  private:
    double m_error;
    double m_recentAverageError;
    static double m_recentAverageSmoothingFactor;
    vector<Layer> m_layer;
};

#endif