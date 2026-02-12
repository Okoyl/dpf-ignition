FILES = [
    # Content files

    # Trick DPF checking for these strings
    ("/etc/temp_bfcfg_strings.env", 420,
     "data:,bfb_pre_install%20bfb_modify_os%20bfb_post_install"),

    # NVConfig parameters using mstflint
    ("/usr/local/bin/set-nvconfig-params-mst.sh", 755, "set-nvconfig-params-mst.sh"),

    # RHCOS installation:
    ("/usr/local/bin/install-rhcos-dpf.sh", 755, "install-rhcos-dpf.sh"),
    ("/usr/local/bin/update_ignition.py", 755, "update_ignition.py"),
]
