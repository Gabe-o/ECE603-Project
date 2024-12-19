# Hardware Data
This folder contains the two sets of power traces collected from the Arduino Pro Micro Dev board used.

We are using an Arduino Pro Micro dev board, with a Teledyne ADQ32 digitizing oscilloscope to capture the power draw (using a custom power draw board to get the live power draw) at a sample rate of 19531250Hz (2.5Ghz/128) as this is close to the clock rate of the board (16MhZ).

More information about the hardware can be found in [./extension_work.ipynb](./extension_work.ipynb)

## AES
The AES data was collected over 256 trials, with initial states from 0 to 256.