# SlowCooker-Pi
The source of all information

## CEG 4981 Team Projects II
- Advisor: Dr. Steve Gorman
- Members: Mariah Doepker, Mark Carson, Corey Brown, Jonathon Gebhardt

## The designed slow cooker
- A network connected slow cooker that can be controlled via an android application

## Getting the IP address of the Raspberry Pi
To ease development of the project, the IP address of the Raspberry Pi can be retrieved from our AWS instance. This is done by adding a systemd service on the Raspberry Pi that sends it's own IP address to the AWS instance on boot.
### Adding the systemd service
- Edit the `ExecStart` parameter in the `send_address.service` file
- Move the `send_address.service` file to `/etc/systemd/system/`
- Execute `sudo systemctl daemon-reload` and `sudo systemctl enable send_address`
After the Raspberry Pi reboots, check the AWS instance website page `rpi-address`.
