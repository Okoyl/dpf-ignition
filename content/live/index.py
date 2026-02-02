FILES = [
    # Content files
    ("/etc/bf.env", 644,
     "data:,HOSTNAME={{.DPUHostName}}\nKERNEL_PARAMETERS={{.KernelParameters}}\nNVCONFIG_PARAMS={{.NVConfigParams}}\nDPF_SF_NUM={{.SFNum}}\nDPF_TRUSTED_SFS={{.TrustedSFs}}"),
    # Trick DPF checking for these strings
    ("/etc/temp_bfcfg_strings.env", 420,
     "data:,bfb_pre_install%20bfb_modify_os%20bfb_post_install"),

    ("/usr/local/bin/install-rhcos-dpf.sh", 755, "install-rhcos-dpf.sh"),
    ("/usr/local/bin/update_ignition.py", 755, "update_ignition.py"),
]
