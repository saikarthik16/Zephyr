from pymavlink import mavutil


class Pixhawk:

    def __init__(self, connection, baud=57600):

        print("Connecting to Pixhawk...")

        self.master = mavutil.mavlink_connection(
            connection,
            baud=baud
        )

        self.master.wait_heartbeat()

        print("Pixhawk connected!")

    def get_gps(self):

        msg = self.master.recv_match(
            type="GLOBAL_POSITION_INT",
            blocking=True,
            timeout=2
        )

        if msg is None:
            return None

        latitude = msg.lat / 1e7
        longitude = msg.lon / 1e7
        altitude = msg.relative_alt / 1000.0

        return {
            "latitude": latitude,
            "longitude": longitude,
            "altitude": altitude
        }