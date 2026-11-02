"""SQLite persistence for devices discovered by the network scanner."""

import sqlite3
import threading

class DevicesDb():
    """Create and query the SQLite database of discovered devices."""

    def __init__(self) -> None:
        """Open the database in the current working directory and create its table."""
        self.lock = threading.Lock()
        self.conn = sqlite3.connect(
            "DevicesTracker.sqlite",
            check_same_thread=False,
        )
        self.cursor = self.conn.cursor()
        query = """
                CREATE TABLE IF NOT EXISTS DevicesDb (
                deviceMac TEXT PRIMARY KEY,
                lastDeviceIp TEXT,
                firstSeen REAL NOT NULL,
                lastSeen REAL NOT NULL
                )
                """

        with self.lock:
            self.cursor.execute(query)
            self.conn.commit()

    def create(self, mac, ip, firstSeen, lastSeen) -> None:
        """Insert a device record, using its MAC address as the primary key."""
        query = "INSERT INTO DevicesDb (deviceMac, lastDeviceIp, firstSeen, lastSeen) VALUES (?,?,?,?)"
        with self.lock:
            self.cursor.execute(query, (mac, ip, firstSeen, lastSeen))
            self.conn.commit()

    def read(self, mac) -> list:
        """Return database rows matching a MAC address (normally zero or one)."""
        query = "SELECT * FROM DevicesDb WHERE (deviceMac = ?)"
        with self.lock:
            self.cursor.execute(query, (mac,))
            val = self.cursor.fetchall()

        return val

    def readAll(self) -> list:
        """Return all saved device rows."""
        query = "SELECT * FROM DevicesDb"
        with self.lock:
            self.cursor.execute(query)
            vals = self.cursor.fetchall()

        return vals

    def update(self, ip, lastSeen, mac) -> None:
        """Update a known device's most recent IP address and seen time."""
        query = "UPDATE DevicesDb SET lastDeviceIp = ?, lastSeen = ? WHERE (deviceMac = ?)"
        with self.lock:
            self.cursor.execute(query, (ip, lastSeen, mac))
            self.conn.commit()

    def delete(self, mac) -> None:
        """Delete the record associated with a MAC address."""
        query = "DELETE FROM devicesDb WHERE (deviceMac = ?)"
        with self.lock:
            self.cursor.execute(query, (mac,))
            self.conn.commit()

    def deleteAll(self):
        """Drop the device table."""
        query = "DROP TABLE devicesDb"
        with self.lock:
            self.cursor.execute(query)
            self.conn.commit()

    def disconnect(self) -> None:
        """Close the SQLite connection."""
        with self.lock:
            self.conn.close()

    