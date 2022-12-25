# 在Python中调用C/C++

[toc]

## 为什么要？

1. 对于已有的稳定的效率高的C/C++代码进行复用。
2. 绕过限制了多线程并行的GIL，用C/C++替代部分python代码从而实现加速。
3. 解释语句改为编译后的库，在大规模运算中提高效率节约资源。

## 实现思路

#### 在Python中调用C/C++面临的主要问题

1. 数据类型的编码和储存在两种语言种不同，Python中一切都是对象，数字存储类型可以自动转换，而C/C++数据类型很多且通常需要开发者定义。将两种语言的数据类型相互转换和传递是Python与C/C++混合编程的重要问题。
2. 不同语言参数传递的机制不同。
3. 两种语言的内存管理机制不同。

#### 主要问题的解决思路

1. 数据类型相互转换是每一次在Python中调用C都需要处理的问题，编码转换的过程可以由包装好的工具实现，但变量在C/C++中的的具体存储类型需要开发者在编写代码时指定。

2. 对于列表（数组）等的传递在不同工具中会有不尽相同的具体的方法，通常参数传递由使用的封装工具解决而不用开发者过分考虑，使用特定的接口而不考虑直接用C/C++对Python存储某些变量的内存进行修改。
3. Python会对引用计数为0的内存地址自动释放内存，而C/C++需要手动释放不用的内存，Python调用C/C++面向对象编程时这个问题将格外明显，在包装好的工具中通常也有所体现。

下面看几种常用到的实现Python调用C/C++的工具，将会发现，这些工具及其使用，都是围绕帮助开发者解决以上问题所展开的。

## 工具及介绍

正如前面提到的，为了在Python中调用C/C++，需要对C/C++代码进行封装，从而连接Python和C/C++代码，下面介绍和展示三种不同的工具的部份用法。

**注：**

| 实验环境 |         版本型号          |
| :------: | :-----------------------: |
|    OS    | macOS 13.0.1 22A400 arm64 |
|  Kernel  |          22.1.0           |
|  Shell   |         zsh 5.8.1         |
|   CPU    |       Apple M1 Pro        |

### ctypes

#### 介绍

ctypes 是 Python 的外部函数库，提供了与 C 兼容的数据类型，并允许调用 DLL 或共享库中的函数。可使用该模块以**纯 Python 形式**对这些库进行**封装**。([source](https://docs.python.org/zh-cn/3/library/ctypes.html))

#### 使用示例--求Python列表元素和

**用 C 编写对整数数组中每个元素求和的函数；**

```c
/* sum.c */
int our_function(int num_numbers, int *numbers) {
    int i;
    int sum = 0;
    for (i = 0; i < num_numbers; i++) {
        sum += numbers[i];
    }
    return sum;
}
```

**编译成动态库 `libsum.so`；**

命令行：

```shell
cc -fPIC -shared -o libsum.so sum.c
```

**在python中调用ctypes进行封装；**

```python
""" sum.py """
import ctypes

_sum = ctypes.CDLL('libsum.so') # 将从C代码编译好的动态库加载为实例 _sum
_sum.our_function.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_int)) # 指定C函数变量类型 


def our_function(numbers): # 接口转换，包装出可以直接调用的python函数
    global _sum # 找到 _sum 实例
    num_numbers = len(numbers) # 列表长度
    array_type = ctypes.c_int * num_numbers # 规定C数组类型&长度
    result = _sum.our_function(ctypes.c_int(num_numbers), array_type(*numbers)) # C函数可以作为_sum的成员函数访问，调用 _sum 计算结果
    return int(result)
```



**用Python调用求整数list的元素和。**

```python
>>> import sum
>>> print sum.our_function([1,2,-3,4,-5,6])
5
```

### cython

#### 介绍

#### 使用方式

#### 使用示例

### pybind11

#### 介绍

#### 使用方式

#### 使用示例

## 评价及总结







## 附：代码包内容







ctypes

是标准库中的模块，调用C动态库

cython

性能很好，在Python调用C中备受青睐

pybind11

2015年出现，较新，利用C++11以上的新特性，是Python调用C++的不错选择

 

1. 



