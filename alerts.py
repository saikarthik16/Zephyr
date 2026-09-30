from datetime import datetime


def create_alert(detection, gps):

    alert = {
        "time": datetime.now().isoformat(),

        "object": detection["class"],

        "confidence": round(
            detection["confidence"] * 100,
            2
        ),

        "latitude": gps["latitude"],

        "longitude": gps["longitude"],

        "altitude": gps["altitude"]
    }

    return alert


def print_alert(alert):

    print("\n" + "=" * 50)

    print("        SEARCH & RESCUE ALERT")

    print("=" * 50)

    print(
        f"Object      : {alert['object']}"
    )

    print(
        f"Confidence  : {alert['confidence']}%"
    )

    print(
        f"Latitude    : {alert['latitude']}"
    )

    print(
        f"Longitude   : {alert['longitude']}"
    )

    print(
        f"Altitude    : {alert['altitude']} m"
    )

    print(
        f"Time        : {alert['time']}"
    )

    print("=" * 50)