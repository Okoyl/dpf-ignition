FILES = [
    # TMFIFO network
    ("/etc/systemd/network/10-tmfifo_net.link", 644, "10-tmfifo_net.link"),
    ("/etc/NetworkManager/system-connections/tmfifo_net0.nmconnection",
     600, "tmfifo_net0.nmconnection"),
    #

    # RSHIM Logging
    ("/usr/local/bin/bflog.sh", 755, "bflog.sh"),
    ("/usr/local/bin/bfupsignal.sh", 755, "bfupsignal.sh"),
]
