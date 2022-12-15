# PDF Search Engine
 It will search for supplied value in PDFs inside the location supplied to it

![alt text](https://github.com/xerone9/PDF-Value-Finder/blob/main/photo.jpeg)

## How To Use:
When launch the app...

1- It asks for set location _give location and it will search for all the PDF files inside the folder and also in all sub-directories_

2- Then Set Value you want to find inside the PDF files and it will start searching. _you can see the log built in the app_

3- Once the search ends it will show the results _either showing value not found or showing the files on which the value is found and you can open the file too if proper option is selected_


### Select Options

#### 1- Open File if value is found

You can activate this option (Switch Button). If you have 1000s of file you can check this option on so that if the value found it will instantly open the file for you. But its highly unstable if you had mistakenly supplied the value that is present in all the PDF file inside the folder you designated and they are 1000s in number. The app wil start opeining all the files and soon your system will get exhausted. So use this option wisely _like when you are sure that the value you are supplying is very unique_

If this option is not turned on. You can see the value found but the app will not open the file for you can see the location in the logs and locate and open the file your self or wait till the program ends and then it will give you the button via which you can select file via log and press open file button to open the file

#### 2- Mutiple Values

You can set multiple values with comma space separtor (like 12345, jhon, 111-454-999 etc.) if you swithed on this option it will find these values in all the PDFs but if you dont turn that Multiple values option on then it will consider the entire value as single "12345, Jhon, 111-454-99" value. _So Be Careful with That_

## Note:
The app is still underdevelopment and will not guarantee the results because PDF has so many encoding and not all the encodings are supported


## Executable File:
Its in windows setup folder. _Will work on windows only. Windows 7 sp1 and above_
