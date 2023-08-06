#PyPriroda

'PyPriroda' is a Python package for quantum chemical program 'PRIRODA', which can be used to create hessian "input" files from optimization "out" files, or optimization "input" files from hessian "out" files.

##Installation

```
pip install PyPriroda
```
##Usage

**Here are the main functions that PyPriroda offers:**

__create_optim__(_name_of_out_hess_file = 'name'_)
This  function creates a hessian file from an optimization file.

_Parameters:_
name_of_hess_file : string, default= 'name'. The name of the hessian file, where the coordinates and the energies come from. 
If 'name', the function takes the name of the hessian file from keybord.

__create_hess__(name_of_out_optimization_file='name')

_Parameters:_
name_of_out_optimization_file : string, default= 'name'. 
The name of the optimization file, where the coordinates and the energies come from.
If 'name', the function takes the name of the optimization file from keybord.

##Examples

```
import PyPriroda as pp

pp.create_optim('HESS_structure_2_TS1_step100_new.out)
#or
pp.create_optim() #We can use keyboard to write a name of the hess file


pp.create_hess('structure2_TS1_steps91-100.out')
#or 
pp.create_hess() #We can use keyboard to write a name of the optimization file
```

#License (MIT License)
2023 Copyright (c) Alexey Polukhin, Olga Lavrukhina

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, ITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.