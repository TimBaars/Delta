# File used to call everything perhaps in treads to start in the future
import time
import sys
sys.path.append('/home/koen/git/Delta/')  # replace with the actual path to the Delta directory
import Pathplanning.Controller_RRT as Controller_RRT

if __name__ == "__main__":
    controller = Controller_RRT.Controller_RRT()
    while True:
        try: 
            controller.run()
            print("------------------------- Sleeping for 5 seconds -------------------------")
            time.sleep(5)
        except KeyboardInterrupt: ## TODO or Noodstop == True:
            print("Exiting")
            controller.robot_driver.shutdown_robot()
            break