## Project: Building an Estimator
In this project, the estimation portion of the controller used in the CPP simulator is developed.  The simulated quad is flying with the developed estimator and the custom controller from the previous project (https://github.com/paulitaky/FCND-Controls-CPP)!

![Quad Image](images/predict-slow-drift.png)

# Required Steps for a Passing Submission:
1. Sensor Noise
2. Attitude Estimation
3. Prediction Step
4. Magnetometer Update
5. Closed Loop + GPS Update
6. Adding Your Controller

---
### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  You can submit your writeup as markdown or pdf. 

You're reading it! Below I describe how I addressed each rubric point and where in my code each point is handled.

### Implement Estimator

#### 2. Determine the standard deviation of the measurement noise of both GPS X data and Accelerometer X data.
A python script was implemented for this, reading in the two text files "config/log/Graph1.txt" and "config/log/Graph2.txt" which contained the logged GPS and imu acceleration data from simulation (Quad-GPS-X and Quad-IMU-AX respectively). Excluding the first row with the naming, the data was converted to numpy arrays and the numpy method *std* over the respective column was applied, leading to values approximating the values set in "SimulatedSensors.txt", i.e. *MeasuredStdDev_GPSPosXY* = 0.71080995 and *MeasuredStdDev_AccelXY* = 0.48935066.


#### 3. Implement a better rate gyro attitude integration scheme in the UpdateFromIMU() function.
As stated in the description, the implemented integration scheme uses quaternions to improve the performance over the previous simple integration scheme. The implementation steps are the following:
- calculate quaternion from estimated Euler angles
- call *IntegrateBodyRate(...)* with the quaternion calculated before and the given body rates from the gyroscope
- set predicted pitch, roll and yaw in the world frame
- normalize yaw from -pi to pi

#### 4. Implement all of the elements of the prediction step for the estimator.
The first step in the prediction function calls *PredictState(...)* to predict the current state vector. The implementation of *PredictState(...)* follows the formulas from the Estimator document (https://www.overleaf.com/project/5c34caab7ecefc04087273b9) section 7.2 and the implementation done in Drone 3D Estimation exercise. For the further implementation of *PredictState(...)* the following steps were implemented:
- set all elements for the Jacobian of the motion model **gPrime** that are different from the identity matrix, thereby following the python implementation from Drone 3D Estimation exercise.
- calculate the predicted ekf covariance matrix based on the formulas used in the Drone 3D Estimation exercise 

#### 5. Implement the magnetometer update.
Implements the ekf update step for the magnetometer, i.e. the measured yaw. The implementation procedure was the following:
- set missing value of Jacobian of the measurement model **hPrime**
- set current estimated yaw
- normalize difference between measured and estimated yaw
- call *Update(...)* performing the actual update steps for updating the yaw, including calculating the Kalman gain etc.

#### 6. Implement the GPS update.
Implements the ekf update step for the GPS sensor, i.e. measured 3D-position and respective velocities. The following steps were implemented:
- fill measurement vector with GPS 3D-position and velocities
- set all "diagonal" elements of the measurement model Jacobian to 1.0 (not a squared matrix, so last column stays with the zeros)
- set current estimated position
- call *Update(...)* performing the actual update steps for updating the 3D-position and velocities, including calculating the Kalman gain etc.

### Flight Evaluation

#### 7. Meet the performance criteria of each step.
After some parameter tuning the final estimator is able to successfully meet all performance criteria with the provided controller.

#### 8. De-tune your controller to successfully fly the final desired box trajectory with your estimator and realistic sensors.
The controller developed in the previous project was de-tuned and successfully meets the performance criteria of the final scenario (<1m error for entire box flight).
