# fpga_sequencer
Hardware timed pulse sequencer is presented here using low cost fpga boards and gui based on Python

For the hardware part, Mojo V3 fpga board is used, which also has the uart communication built in with the help of ATMEGA32U4. In this particular project, the UART speed is set in the firmware installed on ATMega, which is by default set to 500 Kbps. However, any USB to UART converter can be implemented with the allowed baudrates. Only change one needs is to adapt the baudrate in the fpga Uart communication HDL code.

First the configuration file (uart_bram_V9/top.bin ) is uploaded on to the fpga board using Mojo loader software. For different board or pinout configuration, the xise files can be editted as per requirement.

Using Python sequence pattern data is sent to the fpga board. Such a typical pattern is saved in the screenshot.png file. Once the data is sent, the board is ready for accepting triggers. It can either be provided via software (the program itself) or using hardware (in this case, the button on the Mojo V3 board). In fact, various logical combinations can used for complecated trigger. The pinouts are wired to the leds onboard, to see get a direct visual effects.
In this project I am adding two loops in the different section of the pattern. These loops are very flexible as they can run in any order, eg one loop after another or loop inside loop. More number of loops can easily be implemented in the HDL code by small modification. The unique pattern in combination with the loops offer a large number of pattern without consuming much of actual data. The achieved time resolution can be as short as 5ns by using a 200 MHz clock frequency. The board comes with a 50 MHz clock, which is easily multiplied using the in-built clock multiplier.
For the actual output, it is important to a use a high speed line driver such as MC74VHCT240A. This decouples the load from the FPGA input-output pins. It is rather straight forward to implement these ics, for more accurate delay maintainance, the length of all the wires should be maintained to have same length.

The GUI based on Python Tkinter package provides basic features. It diplays all the buttons, time intervals, loop details etc. However depending on the requirement it is very easy to modify the Python code in combination with the FPGA configuration. A screenshot of the Python GUI is attached to get an idea how simple and user friendly could it be.

In the end, I would like to conclude that this project being so simple and cost efficient it offers a much more time demanding task.
I have been successfully using another fpga board with a suitably fast line driver in our main experiment (I work in experimental quantum optics lab) where I need pulses with resolution of 10ns. To me, this solution was much more easier and faster to implement as compared to options available in market considering the flexibility and ease of use.
