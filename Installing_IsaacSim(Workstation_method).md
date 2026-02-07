# Installing Isaac Sim with workstation method

There are several Isaac Sim versions available on NVIDIA’s website, but the **Workstation** version is usually the easiest to install and run.


## 1) Prerequisites
But before we move any further please note that the prerequisites for this specific installation is as follows:

1. `Operating System: Ubuntu 20.04/22.04` (Linux is preferred for Isaac Sim performance and ROS compatibility).
2. `GPU: NVIDIA RTX 4060 or higher` (Isaac Sim requires RTX-enabled cards for compatibility).
3. `RAM: 32GB+ `(Very important for handling complex USD structures and real-time rendering).
4. `Drivers: NVIDIA Drivers` (v525.60+).

## 2) Download Isaac Sim (Workstation) for Linux
Go to the official page below and download the **latest Workstation version for Linux** into your **Downloads** folder:

https://docs.isaacsim.omniverse.nvidia.com/latest/installation/install_workstation.html#isaac-sim-install-workstation

## 3) Install and Launch (Terminal)
Run the commands below:

1. **Create a folder named `isaac`:**
   ```bash
   mkdir -p ~/isaac
    ```

2. Replace the filename below with the exact zip name you downloaded.
    ```
   unzip ~/Downloads/isaac-sim-standalone-5.1.0-linux-x86_64.zip -d ~/isaac
   ```

3. Finally run isaac sim in your computer!
    ```
    cd ~/isaac
    ./post_install.sh
    ./isaac-sim.sh
    ```


