### OOP（C++）大作业

---

#### 题目要求：

> - 设计一个计时器（类），实现程序运行时间的精确测量。
> - 分别基于面向对象和面向过程两种方法实现1个3×3卷积核（卷积核元素随机初始化）遍历1张图像（不小于64×64）的卷积计算。
> - 比较计算时间。



#### 环境：

Ubuntu 20.04, OpenCV 4.5.1,C14

#### Attention：“cmake-build-debug”文件夹下的文件”Conv“须在Linux系统中运行！

#### 说明:

##### 1. 计时器类

调用了头文件<time.h>中的clock();函数，用开始和结束的时间之差计算出运行时间。

```c++
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
};
```



##### 2. 面向过程的图像卷积：

* 定义了基类CONV，包含了卷积核算子Kernel以及对图像卷积函数conv_2d，可在后续拓展出对其他类型对象的卷积。

```c++
class CONV{
protected:
    // kernel used to conv
    vector<vector<float>> kernel;

    // create a random kernel
    vector<vector<float>>create_random_kernel();

    // show kernel
    void kernel_show();

    // conv for pictures
    vector<vector<unsigned char>> conv_2d (vector<vector<unsigned char>> &image, vector<vector<float>> &kernel);

    // exam whether the result is overflowed
    float exam(float result);
};
```



* 对图像的卷积继承了基类CONV，包含了输入输出图像矩阵，输入输出函数。其中输入输出函数中调用了OpenCV库。

```c++
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
```



##### 3. 面向过程的图像卷积

为 读取图像 -> 图像卷积 -> 输出图像 这3个步骤。