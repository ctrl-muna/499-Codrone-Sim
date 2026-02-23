import airsim
import time

def main():
    print("Starting AirSim test...")

    client = airsim.MultirotorClient()
    client.confirmConnection()
    print("Connected to AirSim")

    client.enableApiControl(True)
    client.armDisarm(True)
    print("API control enabled and drone armed")

    print("Taking off...")
    client.takeoffAsync().join()
    time.sleep(2)

    print("Landing...")
    client.landAsync().join()

    client.armDisarm(False)
    client.enableApiControl(False)
    print("Test completed successfully")

if __name__ == "__main__":
    main()