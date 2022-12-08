//
// Created by zjh on 1/6/21.
//
#ifndef CONV_CONV_OOP_H
#define CONV_CONV_OOP_H

#include <iostream>
#include <vector>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include "timer.h"

class CONV{
protected:
    // kernel used to conv
    vector<vector<float>> kernel;

    // create a random kernel
    vector<vector<float>>create_random_kernel();

    // show kernel
    void kernel_show();

    // conv for pictures
    vector<vector<unsigned char>> conv_2d(vector<vector<unsigned char>> &image, vector<vector<float>> &kernel);

    // exam whether the result is overflowed
    float exam(float result);
};

// inheritance
class IMAGE:virtual public CONV{
public:
    // Gather all the function together
    void img_conv(string filename);

private:
    // width and height of the input image
    int width,height;

    // store the original image by channels
    vector<vector<unsigned char>> img_origin_b;
    vector<vector<unsigned char>> img_origin_g;
    vector<vector<unsigned char>> img_origin_r;

    // store the conv_2d result by channels
    vector<vector<unsigned char>> img_result_b;
    vector<vector<unsigned char>> img_result_g;
    vector<vector<unsigned char>> img_result_r;

    //result mat
    cv::Mat result;

    // read image into 2d-vector
    vector<vector<unsigned char>> img_read(string filename,int ch);

    // output result to "result" Mat
    cv::Mat img_output();
};

vector<vector<float>> CONV::create_random_kernel(){
    vector<vector<float>> k(3);
    for(int i =0; i < 3; i++)
        k[i].resize(3);

    for(int i =0; i < 3; i++){
        for(int j =0; j < 3; j++){
            float temp;
            temp = (float)(rand()/(float)RAND_MAX);
            k[i][j]=1.0*temp;
        }
    }
    return k;
}

void CONV::kernel_show(){
    cout<<"The kernel of oop is:"<<endl;
    for(int i =0; i < 3; i++){
        for(int j =0; j < 3; j++){
            cout.setf(ios::fixed);
            cout<<fixed<<setprecision(5)<<kernel[i][j]<<" ";
        }
        cout<<endl;
    }
}

float CONV::exam(float result)
{
    if (result>=0&&result<=255) //未溢出
    {
        return result;
    }
    else //溢出
    {
        if (result>255)
            return 255;
        if (result<0)
            return 0;
    }
}

vector<vector<unsigned char>> CONV::conv_2d(vector<vector<unsigned char>> &image, vector<vector<float>> &kernel)
{
    int image_row = image.size();
    int image_col = image[0].size();
    int kernel_row = kernel.size();
    int kernel_col = kernel[0].size();
    vector<vector<unsigned char>> result;
    int result_row = image_row - kernel_row + 1;
    int result_col = image_col - kernel_col + 1;

    for (int i = 0; i < result_row; i++)
    {
        vector<unsigned char> row_result;
        for (int j = 0; j < result_col; j++)
        {
            float res = 0;
            for (int k = 0; k < kernel_col; k++)
                for (int m = 0; m < kernel_row; m++)
                {
                    long int row = i + k;
                    long int col = j + m;
                    float mul = image[row][col]* kernel[k][m];
                    res = res + mul;
                }
            res = exam(res);
            row_result.push_back((unsigned char)res);
        }
        result.push_back(row_result);
    }
    return result;
}

vector<vector<unsigned char>> IMAGE::img_read(string filename,int ch) {
    cv::Mat image;
    image = cv::imread(filename);

    width = image.rows;
    height =image.cols;
    vector<cv::Mat> channels;
    split(image,channels);
    cv::Mat M = channels.at(ch);

    int i;
    vector<vector<unsigned char>> Img(height);
    for (i = 0; i < Img.size(); i++)
        Img[i].resize(width);

    for (i = 0; i < height; i ++){
        for (int j = 0; j < width; j ++){
            Img[i][j] = M.at<uchar>(i, j);
        }
    }
    return Img;
}

cv::Mat IMAGE::img_output() {
    typedef cv::Vec<unsigned char,3> Vec3d;

    cv::Mat M = cv::Mat::zeros(height-2, width-2, CV_8UC3);

    for (int i = 0; i < M.rows; i++)
    {
        for (int j = 0; j < M.cols; j++)
        {
            for (int c = 0; c <M.channels(); c++)
            {
                if (c==0)
                    M.at<Vec3d>(i, j)[c] = img_result_b[i][j];
                if (c==1)
                    M.at<Vec3d>(i, j)[c] = img_result_g[i][j];
                if (c==2)
                    M.at<Vec3d>(i, j)[c] = img_result_r[i][j];
            }
        }
    }
    return M;

}

void IMAGE::img_conv(string filename)
{
    TIMER t1;
    t1.start();

    kernel=create_random_kernel();
    kernel_show();

    img_origin_b = img_read(filename,0);
    img_origin_g = img_read(filename,1);
    img_origin_r = img_read(filename,2);

    img_result_b = conv_2d(img_origin_b, kernel);
    img_result_g = conv_2d(img_origin_g, kernel);
    img_result_r = conv_2d(img_origin_r, kernel);

    result = img_output();

    cv::imwrite("../result_oop.jpeg",result);
    cv::imshow("result_oop",result);

    t1.finish();
}

#endif //CONV_CONV_OOP_H
