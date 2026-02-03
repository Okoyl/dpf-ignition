FILES = [
    # Content files
    # Trick DPF checking for these strings
    ("/etc/temp_bfcfg_strings.env", 420,
     "data:,bfb_pre_install%20bfb_modify_os%20bfb_post_install"),

    ("/usr/local/bin/set-nvconfig-params-mst.sh", 755, "set-nvconfig-params-mst.sh"),
    ("/etc/systemd/network/10-tmfifo_net.link", 644, "10-tmfifo_net.link"),
    ("/usr/local/bin/install-rhcos-dpf.sh", 755, "install-rhcos-dpf.sh"),
    ("/usr/local/bin/update_ignition.py", 755, "update_ignition.py"),
    ("/etc/NetworkManager/system-connections/tmfifo_net0.nmconnection",
     600, "tmfifo_net0.nmconnection"),
]
