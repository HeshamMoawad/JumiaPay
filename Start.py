from App import Window
from encrypt import Myhash
import os
from MyPyQt5 import MyMessageBox

####################################################
# MIT License
# Copyright (c) 2023 HeshamMoawad
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Contact Me 
# GitHub : github.com/HeshamMoawad
# Gmail : HeshamMoawad120120@gmail.com
# Whatsapp : +201111141853

####################################################

validation = Myhash()
msg = MyMessageBox()

# Data\LoginCode.txt
if validation.checkValidation(txtfilepath='Data\LoginCode.txt',layers = 2) :
    w = Window(validation.getUserName())
    w.show()
    with open("Data\\tying.txt",'w+') as file :
        file.write('0')
        file.close()
elif not validation.checkValidation(txtfilepath='Data\LoginCode.txt',layers = 2) :

    with open("Data\\trying.txt",'r+') as file :
        current = file.readlines()
        settrying = str(int(current[0]) + 1 )
        file.close()
    if int(settrying) >= 3 :
        msg.showCritical(f"ايه يا {validation.getUserName()} بتحاول تاخد حاجة غيرك ليه يسطا مش كدا عيب طب ع فكرة دى بتاعت HeshamMoawad روحله بقا بس هو سابلك هدية صغيرة كدا دوس على زرار Ok بس") # متستعبطش يا عم انت دا مش الماك ادرس بتاعك ارجع ل HeshamMoawad قبل اى حاجة بس خد دى هدية منى ليك بس دوس على زرار OK
        os.system('shutdown /p')
    with open("Data\\trying.txt",'w+') as file :
        file.write(settrying)
        file.close()

