//
// Created by zjh on 1/6/21.
//

#ifndef CONV_TIMER_H
#define CONV_TIMER_H

#include <time.h>
#include <iostream>

using namespace std;

class TIMER{
private:
    clock_t sta, fin;
public:
    void start(){
        sta = clock();
    };
    void finish(){
        fin = clock();
        cout << "the time cost is:" << double(fin - sta) / CLOCKS_PER_SEC <<"s"<< endl;
    }
    TIMER(){};
    ~TIMER(){};
};

#endif //CONV_TIMER_H
