# autopi-ioniq5

Notes taken from getting my autopi up and running with a Hyundai Ioniq 5.

The official documentation seems relatively comprehensive, but it also unfortunately appears to have a lot of assumed knowledge.  In case anyone else ever wants to get autopi working on an Ioniq 5, I wanted to share what worked for me.

I didn't reverse engineer the Ioniq 5 PIDs, they came from here: https://github.com/Esprit1st/Hyundai-Ioniq-5-Torque-Pro-PIDs.  Instead I used these to guide the implementation of PIDs I needed and also used some tips [from this post](https://community.autopi.io/t/copying-txt-pid-file-from-torque-pro/1031/2) on how to convert them.


Note - this guide assumes you have purchased an autopi device and that you have access to the (quite feature rich) autopi.io cloud dashboards. I also point out that despite the [autopi website](https://www.autopi.io/electric-vehicle-types/hyundai-ioniq-5-integrate-with-autopi/) implying there is native support for the Ioniq 5, it all seems up to the end user to develop the sensors and controllers.

## Learnings

 - The Ioniq 5 seems to use a 3 digit PID and 3 digit code PID schema.

# Setup in AutoPi

## Setup a CAN Bus

Create an entry for a new vehicle in autopi, with the following settings for the CAN Bus (I think you only need one):

 - **Protocol** : [6] ISO 15765-4 (CAN 11/500)
 - **Baud Rate** - 500000
 - **Default** - Yes

    [Screenshot of my CAN Bus setup.](/img/can-bus-setup.png)

Note how at time of writing, autopi did not have the "Ioniq 5" model available in it's database.  This didn't seem to effect functionality, but it did prevent sharing of PIDs between community members etc. Update: they have added the model now as per this [Community post](https://community.autopi.io/t/add-the-hyundai-ioniq-5-model-to-community-library/3033/3)

I note that at no stage did the "Auto-detect" CAN Bus functionality in autopi work for me.

## Telling autopi when to turn on & stay on

Note that the Ioniq 5 will not respond to the CAN Bus when it is powered off. Instead you'll see responses like: 

`No data received from vehicle within timeout`

Originally I was doing initial connection testing leaving the car on, however I've discovered that the CAN bus "turns on" when the car is charging. So, rather than leaving the car on, I just setup the car to trickle charge so I could test against it.

The autopi apparently be default relies on a RPM reading from an ICE engine to know when to turn the autopi "minion" on or not. In an EV, there is no default RPM concept and will mean that nothing works for you until you fix it. As such, start there.

Reference material: 
https://docs.autopi.io/guides/power-cycle-for-electric-vehicles/

Note that I have shared the two new PIDs to the Community, so you should be able to just search for them rather than have to manually create them again.


### Tell autopi to turn on when car turns on (drives)

Using the `rpm_motor_event` mechanism in autopi (described [here](https://docs.autopi.io/guides/power-cycle-for-electric-vehicles/#setup-a-pid-logger-using-the-rpm_motor_event-trigger)), we can get the autopi to turn on when the electric motors spin. 
In "My Library" I needed to create a new PID:

| Name | Description | Mode | Code | Header | Bytes | Formula | Unit | Min | Max |
|--|--|--|--|--|--|--|--|--|--|
| RPM | Drive Motor Speed 1 | 220 | 101 | 7E4 | 64 | twos_comp(bytes_to_int(message.data[56:57])*256+bytes_to_int(message.data[57:58]),16) | Revolutions per minute | -10100 | 10100 |

In "Loggers" create a new PID logger off that PID: 

| PID | Interval | Enabled | Converter | Filter | Trigger | Returner | Verify |
|--|--|--|--|--|--|--|--|
| RPM | 10 | Yes | | alternating_readout | rpm_motor_event | cloud | No

Then sync the changes and restart the autopi

###  Tell autopi to turn on when charging

Using the `communication_event` mechanism in autopi (described [here](https://docs.autopi.io/guides/power-cycle-for-electric-vehicles/#setup-a-pid-logger-using-the-communication_event-trigger)), we can get the autopi to turn on when the car is charging: 

| Name | Description | Mode | Code | Header | Bytes | Formula | Unit | Min | Max |
|--|--|--|--|--|--|--|--|--|--|
| SOC_Display | State of Charge Display | 220 | 105 | 7E4 | 64 | bytes_to_int(message.data[34:35])/2.0 | Percent | 0 | 100 |

In "Loggers" create a new PID logger off that PID: 

| PID | Interval | Enabled | Converter | Filter | Trigger | Returner | Verify |
|--|--|--|--|--|--|--|--|
| SOC_Display | 30 | Yes | | alternating_readout | communication_event | cloud | No

In **Advanced > Settings > Power**, we need to change the:

  - **Sleep Timer > Event Driven > Event Regex**: `^vehicle/communication/disconnected`

    the default was `^vehicle/motor/stopped`
  - **Sleep Timer > Event Driven > Reason**: `vehicle_communication_disconnected`

    the default was: `motor_stopped`
  - **Sleep Timer > Suppress > Event Regex**: `^vehicle/communication/established`

    the default was: `^vehicle/motor/running`


Then sync the changes and restart the autopi


# TODO - Convert all PIDs from Torque Pro

TODO - convert the lot with a script - see some intial workings in the sub folders of this post, however none of it is remotely functional. It may just make more sense to manually convert anything required.