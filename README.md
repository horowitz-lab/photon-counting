# photon-counting
Photon counting with an SR400 Photon Counter.

## How to run the code:
1. Open Anaconda Navigator
2. Launch Spyder
3. Click on the "open file" button
4. Head to the Photon-Counting folder
5. The Code controlls the Photon Counter is: Photon_Counter_GPIB.py
6. Before doing anything, MAKE SURE YOU TURN ON THE APD, CONNECT IT TO THE 
 SR400, AND TURN ON THE SR400! a failure to do so will cause the code or the
 SR400 to bug out
7. Run the code by pressing the big green Play button at the top of the screen.
 An additional spyder window should pop up. Click on it to open the controll panel
8. You can set the time interval, or period, by editing the number on the white 
 box to the left, and you can set the threshold rate the same way on the box to
 the right.
9. Any rate detected above the threshold will cause the program to 
 tell the Arduino connected via the serial port to actuate the valve, as long 
 as the DC power supply is set to 24 volts.
10. The start button starts the program to start measuring rates, and the stop 
 button stops the program. 
11. Unchecking the "scale" checkbox scrolls thegraph window, clearing old data off the 
 graph. This does not experience lag. (lag mainly affects stoping measuring and 
 starting a new measurement, and is due to the rvtgraph application being not
 an ideal application) 
12. Checking the "scale" checkboxscales the window to fit all the data. This 
 becomes laggy when dealing with large quantities of data, but is good to see 
 slow phenomena such as photo-bleaching.
13. If you want to save your data, make sure you click on the little save checkbox.
14. To access your saved data, go to Documents, SavedData. You will see your last data 
 set in a folder with the date and time you its recording. You can always 
 change the folder’s name after you close out of Spyder. 
## How to edit the code:
See the [wiki](https://github.com/horowitz-lab/photon-counting/wiki) for more info.

Note:  	SR400_GUI.ui is not up to date; we are making edits directly in	SR400_GUI.py.
