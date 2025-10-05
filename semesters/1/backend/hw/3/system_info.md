# Linux System Info

## Kernel Version

- Command:

    ```bash
    uname -r
    ```

- Output:

    ```txt
    6.8.0-49-generic 
    ```

## Shell

- Command:

    ```bash
    echo $SHELL
    ```

- Output:

    ```txt
    /usr/bin/zsh 
    ```

## Desktop Environment

- Command:

    ```bash
    echo $XDG_CURRENT_DESKTOP
    ```

- Output:

    ```txt
    GNOME
    ```

## Init system

- Command:

    ```bash
    ps -p 1 -o comm=
    ```

- Output:

    ```txt
    systemd
    ```

## Kernel Params

- Command:

    ```bash
    cat /proc/cmdline
    ```

- Output:

    ```txt
    BOOT_IMAGE=/boot/vmlinuz-6.8.0-49-generic root=UUID=2d7cd80b-29de-4696-8a32-6b6af9a35627 ro quiet splash vt.handoff=7
    ```

## Second Running Process

- Command:

    ```bash
    ps -p 2
    ```

- Output:

    ```txt
    PID TTY          TIME CMD
      2 ?        00:00:04 kthreadd
    ```

## Running services

- Command:

    ```bash
    systemctl list-units --type=service --state=running
    ```

- Output:

    ```txt
        UNIT                          LOAD   ACTIVE SUB     DESCRIPTION
        accounts-daemon.service       loaded active running Accounts Service
        acpid.service                 loaded active running ACPI event daemon
        avahi-daemon.service          loaded active running Avahi mDNS/DNS-SD Stack
        colord.service                loaded active running Manage, Install and Generate Color Profiles
        containerd.service            loaded active running containerd container runtime
        cron.service                  loaded active running Regular background program processing daemon
        cups-browsed.service          loaded active running Make remote CUPS printers available locally
        cups.service                  loaded active running CUPS Scheduler
        dbus.service                  loaded active running D-Bus System Message Bus
        docker.service                loaded active running Docker Application Container Engine
        gdm.service                   loaded active running GNOME Display Manager
        irqbalance.service            loaded active running irqbalance daemon
        kerneloops.service            loaded active running Tool to automatically collect and submit kernel crash signatures
        ModemManager.service          loaded active running Modem Manager
        NetworkManager.service        loaded active running Network Manager
        nvidia-persistenced.service   loaded active running NVIDIA Persistence Daemon
        packagekit.service            loaded active running PackageKit Daemon
        polkit.service                loaded active running Authorization Manager
        power-profiles-daemon.service loaded active running Power Profiles daemon
        rsyslog.service               loaded active running System Logging Service
        rtkit-daemon.service          loaded active running RealtimeKit Scheduling Policy Service
        snapd.service                 loaded active running Snap Daemon
        ssh.service                   loaded active running OpenBSD Secure Shell server
        switcheroo-control.service    loaded active running Switcheroo Control Proxy service
        systemd-journald.service      loaded active running Journal Service
        systemd-logind.service        loaded active running User Login Management
        systemd-oomd.service          loaded active running Userspace Out-Of-Memory (OOM) Killer
        systemd-resolved.service      loaded active running Network Name Resolution
        systemd-timesyncd.service     loaded active running Network Time Synchronization
        systemd-udevd.service         loaded active running Rule-based Manager for Device Events and Files
        udisks2.service               loaded active running Disk Manager
        upower.service                loaded active running Daemon for power management
        user@1000.service             loaded active running User Manager for UID 1000
        user@128.service              loaded active running User Manager for UID 128
        wpa_supplicant.service        loaded active running WPA supplicant

    LOAD   = Reflects whether the unit definition was properly loaded.
    ACTIVE = The high-level unit activation state, i.e. generalization of SUB.
    SUB    = The low-level unit activation state, values depend on unit type.
    35 loaded units listed.
    ```
