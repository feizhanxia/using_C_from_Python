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

1. 数据类型相互转换是每一次在python中调用C都需要处理的问题，编码转换的过程可以由包装好的工具实现，但变量在C/C++中的的具体存储类型需要开发者在编写代码时指定。

2. 对于列表（数组）等的传递在不同工具中会有不尽相同的具体的方法，通常参数传递使用特定的接口而不考虑丑陋和具体的直接用C/C++对python某些变量进行修改。
3. python会对引用计数为0的内存地址自动释放内存，而C/C++需要手动释放不用的内存，python调用C/C++面向对象编程时这个问题将格外明显，在包装好的工具中通常也有所体现。

下面看几种常用到的实现python调用C/C++的工具，将会发现，这些工具及其使用，都是围绕帮助开发者解决以上问题所展开的。

## 工具及介绍

**注：实验环境**

|        |           版本            |
| :----: | :-----------------------: |
|   OS   | macOS 13.0.1 22A400 arm64 |
| Kernel |          22.1.0           |
| Shell  |         zsh 5.8.1         |
|  CPU   |       Apple M1 Pro        |

### ctypes

#### 介绍

#### 使用方式

#### 使用示例

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



