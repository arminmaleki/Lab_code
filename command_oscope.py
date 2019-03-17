#for a working scipy.signal on raspberry you need:
sudo apt-get install libatlas-base-dev
pi@raspberrypi:~/oscope/usb$ python3
Python 3.5.3 (default, Sep 27 2018, 17:25:39) 
[GCC 6.3.0 20170516] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import usbtmc
>>> instr=usbtmc.Instrument(6833,1416)
>>> instr.ask("*IDN?")
'Rigol Technologies,DS1102E,DS1ET194510708,00.04.02.01.00'
>>> instr.ask(":RUN")
>>> instr.ask(":STOP")
>>> data=instr.ask_raw(b":WAV:DATA? CHAN1")
>>> len(data)
524298
>>>
>>> exit()
>>> import usbtmc
>>> instr=usbtmc.Instrument(6833,1416)
>>> instr.ask(":RUN",wait_reply=False)
0
>>> instr.ask(":CHAN2:DISP OFF",wait_reply=False)
0
>>> instr.ask(":CHAN1:MEMD?")
'1048576'
>>> instr.ask(":STOP",wait_reply=False)
0
>>> data=instr.ask_raw(b":WAV:DATA? CHAN1")
>>> len(data)
1048576
>>> instr.ask(":ACQ:MEMD LONG")
