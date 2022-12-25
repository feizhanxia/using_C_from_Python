# 在Python中调用C/C++



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

用 C 编写对整数数组中每个元素求和的函数；

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

编译成动态库 `libsum.so`；

命令行：

```shell
cc -fPIC -shared -o libsum.so sum.c
```

在python中调用ctypes进行封装；

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



封装得到了 `sum.py` 可作为模块直接调用。

用Python调用求整数list的元素和。

```python
>>> import sum
>>> print sum.our_function([1,2,-3,4,-5,6])
5
```

### cython

#### 介绍

与 ctypes 完全用 Python 进行封装来使用C代码不同，Cython是一种全新的语言。它的工作原理是通过Cython编译器将 Cython 代码 (.pyx) 转化为 C (.c) 代码，再通过C编译器编译为Python直接可以调用的动态库 (`xxx.so`) 。

Cython语法是Python语法的超集。基本所有Python代码都可以作为Cython代码编译为C代码；Cython代码又有着定义静态类型声明和内存分配和释放的语法，与C的特性相对应。于是Cython成为了一种Python语法与C特性混合的语言，可以很方便的在Python代码中调用C库，也可以通过简单的Python代码改写利用C语言的优势加速代码，同时通过成熟的Cython编译器可以得到极为优化的十分高效的C代码。值得一提的是，静态类型声明在Cython代码加速中常常有着十分显著的作用。([source](https://cython.readthedocs.io/en/latest/index.html))

通常从Cython代码到动态库的构建是通过写构建文件 `setup.py` 然后直接构建得到的。但同样也有替代的方式来直接构建或手动转化为C代码再手动从C代码编译。我们只展示文档中推荐的平常方式即通过 `setup.py` 文件直接构建。

#### 使用示例

编写示例Cython代码；

```cython
""" example.py """
cdef int a
a = 3
print("hello{}".format(a))
def list_sum(arr):
    return sum(arr)
```

编写Python构建代码；

```python
""" setup.py """
from distutils.core import setup
from Cython.Build import cythonize

setup(
        name = "Hello world 3 App",
        ext_modules = cythonize("example.pyx")
        )
```

编译为C代码 `example.c` 和自动编译构建为动态库 `example.so` ；

命令行：

```shell
python setup.py build_ext --inplace
```

`example.so`作为Python模块直接调用。

```python
>>> import example
hello3
>>> example.list_sum([1,2,3])
6
>>> help(example)
```

<img src="./README.assets/Screenshot 2022-12-25 at 16.21.23.png" alt="Screenshot 2022-12-25 at 16.21.23" style="zoom:40%;" />

### pybind11

#### 介绍

运用 C++11 以上的新特性，pybind11是一个**仅包含头文件**的轻量级库，能建立 Python 代码和 C++ 代码之间的连接，主要用于Python代码调用现有的C++代码。

pybind11 通过在 C++ 文件中引用 pybind11 的头文件和添加代码块的简单修改，可以直接编译得到符合 Python 接口的动态库作为 Python 外部模块调用。pybind11构建的动态库的 Python 文档的编辑也更加便利和现代化。

pybind11 构建的方法有很多，既可以普通的设置编译器参数构建也可以通过CMake工具或者Python的 `setuptools` 进行跨平台的构建。下面为了便于展示只做在命令行用设置编译器进行普通构建。

#### 使用示例

编写示例C++代码文件;

```c++
/* example.cpp */
#include <pybind11/pybind11.h>

namespace py = pybind11;

int add(int i, int j) {
	return i + j;
}

// pybind11 模块
PYBIND11_MODULE(example, m) {
	m.doc() = "pybind11 example plugin"; // 文档字段，非必须

	m.def("add", &add, "A function that adds two numbers",
      py::arg("i"), py::arg("j"));
}
```

编译文件，命令行：

```shell
c++ -O3 -Wall -shared -std=c++11 -undefined dynamic_lookup $(python3 -m pybind11 --includes) example.cpp -o example$(python3-config --extension-suffix)
```

`example.so` 作为Python模块直接调用。

```python
>>> import example
>>> example.add(1,2)
3
>>> help(example)
```

<img src="./README.assets/Screenshot 2022-12-25 at 16.20.12.png" alt="Screenshot 2022-12-25 at 16.20.12" style="zoom:40%;" />

## 评价及总结

**ctypes**

是Python标准库中的模块，可以通过编写纯Python的封装来调用C动态库，是Python调用C的原生工具，但没有代码自动优化功能效率不如编译器优化的cython，且由于是较为初级的工具，数据类型转换的手动声明较为繁琐。

**cython**

性能很好，在Python调用C中备受青睐，由于是新的语言有一定的学习成本，但作为Python语法的超集，与C语言联动更加灵活，代码的灵活性强，且在大规模代码的使用中性能可靠且提速明显。

**pybind11**

2015年出现，较新，只支持C++，利用C++11以上的新特性使得工具轻便易用且功能完整，是Python调用C++的不错选择。

了解了这些工具，在Python中调用C/C++并不困难，可以考虑所需选取合适的工具来完成。但对于Python代码的提速除了调用C/C++以外，已经有了很多成熟的现代化工具，如Numba等Python包或者Taichi等与Python结合的DSL，使用C/C++加速并非唯一选择，应该权衡利弊考虑效率的情况下用较低的成本来提速我们的运算代码。





**注：** 这个Note已经放在Github上，你可以在这里( [https://github.com/feizhanxia/using_C_from_Python](https://github.com/feizhanxia/using_C_from_Python) )找到这个Slide以及展示中用到的全部文件。
