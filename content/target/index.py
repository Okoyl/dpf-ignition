FILES = [
    # VF Activation on generic
    ("/usr/local/bin/devlink-activate.sh", 755, "devlink-activate.sh"),

    # DPF configuration
    ("/etc/mellanox/mlnx-bf.conf", 644, "mlnx-bf.conf"),
    ("/etc/mellanox/mlnx-ovs.conf", 644, "mlnx-ovs.conf"),

    # NM connections for VFs
    ("/etc/NetworkManager/system-connections/pf0vf0.nmconnection",
     600, "pf0vf0.nmconnection"),
    ("/etc/NetworkManager/system-connections/br-comm-ch.nmconnection",
     600, "br-comm-ch.nmconnection"),

    # OOB network
    ("/etc/NetworkManager/system-connections/oob_net0.nmconnection",
     600, "oob_net0.nmconnection"),

    # General configuration
    ("/etc/crio/crio.conf.d/99-ulimits.conf", 644, "99-ulimits.conf"),
    ("/etc/sysctl.d/98-dpunet.conf", 644, "98-dpunet.conf"),
    ("/etc/modules-load.d/br_netfilter.conf", 420, "data:,br_netfilter"),
    ("/etc/sysconfig/openvswitch", 600, "openvswitch"),
    ("/usr/local/bin/dpf-configure-sfs.sh", 755, "dpf-configure-sfs.sh"),

    # NVConfig parameters using mlx
    ("/usr/local/bin/set-nvconfig-params.sh", 755, "set-nvconfig-params.sh"),
]
