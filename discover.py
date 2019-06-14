from blesuite import connection_manager
import time
import gevent
import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
import pickle
def general_scan(adapter=0,timeout=50):
    """
    Scan for BTLE Devices and print out results
    :param timeout: Scan timeout (seconds)
    :param adapter: Host adapter to use for scanning (Use empty string to use host's default adapter)
    :type timeout: int
    :type adapter: str
    :return: Discovered devices ({<address>:(<addressType>, <data>)})
    :rtype: dict
    """
    if timeout < 0:
        raise Exception("%s is an invalid scan timeout value. The timeout must be a positive integer" % timeout)

    with connection_manager.BLEConnectionManager(adapter, "central") as connectionManager:
        connectionManager.start_scan()
        start = time.time() * 1000
        logger.debug("Starting sleep loop")
        while ((time.time() * 1000) - start) < (timeout * 1000):
            logger.debug("Scanning...")
            gevent.sleep(1)
            connectionManager.stop_scan()
        logger.debug("Done scanning!")
        discovered_devices = connectionManager.get_discovered_devices()

    return discovered_devices


def main():
    import sys
    if len(sys.argv) < 2:
        print "Usage: discover.py #adapter"
        return
    adapter = int(sys.argv[1])
    discovered_devices = general_scan(adapter)
    print len(discovered_devices)
    with open("device_list.txt","w") as file:
        for device in discovered_devices:
            file.write(device+"\n")


if __name__ == "__main__":
    main()