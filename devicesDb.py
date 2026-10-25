"""SQLite persistence for devices discovered by the network scanner."""

import sqlite3

class DevicesDb():
    # Create and query the local device-tracking database.

    def __init__(self) -> None:
        # Open DevicesTracker.sqlite in the current working directory.
        self.conn = sqlite3.connect("DevicesTracker.sqlite")
        self.cursor = self.conn.cursor()
        query = """
                CREATE TABLE IF NOT EXISTS DevicesDb (
                deviceMac TEXT PRIMARY KEY,
                lastDeviceIp TEXT,
                firstSeen REAL NOT NULL,
                lastSeen REAL NOT NULL
                )
                """

        self.cursor.execute(query)
        self.conn.commit()

    def create(self, mac, ip, firstSeen, lastSeen) -> None:
        # Insert a device record using its MAC address as the primary key.
        query = "INSERT INTO DevicesDb (deviceMac, lastDeviceIp, firstSeen, lastSeen) VALUES (?,?,?,?)"
        self.cursor.execute(query, (mac, ip, firstSeen, lastSeen))
        self.conn.commit()

    def read(self, mac) -> list:
        # Return the database row matching mac, or an empty list.
        query = "SELECT * FROM DevicesDb WHERE (deviceMac = ?)"
        self.cursor.execute(query, (mac,))
        val = self.cursor.fetchall()

        return val

    def readAll(self) -> list:
        # Return all device records.
        query = "SELECT * FROM DevicesDb"
        self.cursor.execute(query)
        vals = self.cursor.fetchall()

        return vals

    def update(self, ip, lastSeen, mac) -> None:
        # Update a known device's last-seen IP address and timestamp.
        query = "UPDATE DevicesDb SET lastDeviceIp = ?, lastSeen = ? WHERE (deviceMac = ?)"
        self.cursor.execute(query, (ip, lastSeen, mac))
        self.conn.commit()

    def delete(self, mac) -> None:
        # Delete the record for mac.
        query = "DELETE FROM devicesDb WHERE (deviceMac = ?)"
        self.cursor.execute(query, (mac,))
        self.conn.commit()

    def disconnect(self) -> None:
        # Close the SQLite connection.
        self.conn.close()

    