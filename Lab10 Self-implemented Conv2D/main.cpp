#include <iostream>
#include <cstdlib>
#include <iomanip>
#include "conv_oop.h"
#include "conv_pop.h"

int main() {
    string filename = "../img.jpeg";

    // output the origin image
    cv::Mat image1;
    image1 = cv::imread(filename);
    cv::imshow("origin",image1);

    // OOP Part
    cout<<"Image Convolution in OOP:";
    IMAGE c1;
    c1.img_conv(filename);

    // POP Part
    vector<vector<float>> ker(3);
    TIMER t1;
    t1.start();

    for(int i =0; i < 3; i++)
        ker[i].resize(3);

    cout<<"The kernel of pop is:"<<endl;
    for(int i =0; i < 3; i++){
        for(int j =0; j < 3; j++){
            float temp;
            temp = (float)(rand()/(float)RAND_MAX);
            ker[i][j]=1.0*temp;
            cout.setf(ios::fixed);
            cout<<fixed<<setprecision(5)<<ker[i][j]<<" ";
        }
        cout<<endl;
    }

    img_origin_b = img_read(filename,0);
    img_origin_g = img_read(filename,1);
    img_origin_r = img_read(filename,2);

    img_result_b = convolution(img_origin_b, ker);
    img_result_g = convolution(img_origin_g, ker);
    img_result_r = convolution(img_origin_r, ker);

    result = img_output();

    cout<<"Image Convolution in POP:";
    cv::imwrite("../result_pop.jpeg",result);
    cv::imshow("result_pop",result);

    t1.finish();

    cv:: waitKey(0);
}
