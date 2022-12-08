//
// Created by zjh on 1/6/21.
//

#ifndef CONV_CONV_POP_H
#define CONV_CONV_POP_H

#include <iostream>
#include <vector>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include "timer.h"

typedef cv::Vec<unsigned char,3> Vec3d;

using namespace std;

int width,height;
//图像矩阵
vector<vector<unsigned char>> img_origin_b;
vector<vector<unsigned char>> img_origin_g;
vector<vector<unsigned char>> img_origin_r;
//卷积结果矩阵
vector<vector<unsigned char>> img_result_b;
vector<vector<unsigned char>> img_result_g;
vector<vector<unsigned char>> img_result_r;
//result mat
cv::Mat result;

// read image into vector
vector<vector<unsigned char>>img_read(string filename,int ch) {
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

float exam(float result)
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

// convolution process
vector<vector<unsigned char>>convolution(vector<vector<unsigned char>> &image, vector<vector<float>> &kernel)
{
    int image_row = image.size();                //获取图片矩阵的行数
    int image_col = image[0].size();             //获取图片矩阵的列数
    int kernel_row = kernel.size();              //获取卷积核矩阵的行数
    int kernel_col = kernel[0].size();           // 获取卷积核矩阵的列数
    vector<vector<unsigned char>> result;        //定义二维vector用于接收卷积结果
    int result_row = image_row - kernel_row + 1; //计算结果矩阵的行数
    int result_col = image_col - kernel_col + 1; //计算结果矩阵的列数

    for (int i = 0; i < result_row; i++)
    {
        vector<unsigned char> row_result; //定义一维行矩阵以便于填入二维的result矩阵
        for (int j = 0; j < result_col; j++)
        {
            float res = 0; //用于记录每一次卷积过程，图片与卷积核矩阵中数字乘积的结果
            for (int k = 0; k < kernel_col; k++)
                for (int m = 0; m < kernel_row; m++)
                {
                    long int row = i + k;
                    long int col = j + m;
                    float mul = image[row][col]* kernel[k][m];
                    res = res + mul;
                }
            res = exam(res);
            row_result.push_back((unsigned char)res); //将一次的卷积结果填入行矩阵中
        }
        result.push_back(row_result); //将某一行的卷积结果填入二维卷积结果矩阵中
    }
    return result;
}
// output the result
cv::Mat img_output() {

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
#endif //CONV_CONV_POP_H
