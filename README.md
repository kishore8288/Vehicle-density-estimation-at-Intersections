# Vehicle density Estimation at intersections
**Basically this project was presented by my team at UYIR hackathon in 2025.**

### Features in this project :
#### Dynamic signalling :
		First we tried to estimate the number of vehicles in all the four directions of the intersection. To make sure not to count the vehicles going away from the signal, we introduced a code **which crops the image taken by it's own to only capture the images of the incoming vehicles**.
    Turn on the green signal for the lane having high vehicle density and counting will be done based on the vehicle density. i.e; we produced a **relation btw vehicles and the timer to calculate and count dynamically**.
    Now it takes the images of other three lanes before the green signal ends to that lane. And 10 seconds before the green ends, the lane which has higher density among the three get an yellow lane to make sure them to ready. This process will iterate over and over.

#### Dynamic timer :
    The timings for all the 4 lanes and decrement is displayed on the 7 segment display.

*This whole project was done on the Raspberrypi 4B model*
