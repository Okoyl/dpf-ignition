# File definitions for ignition template
# Each entry: (target_path, mode, content_source)
# content_source is either:
#   - a string starting with "data:" for direct source URLs
#   - a filename for content files in this directory

FILES = [
    # Templated/plain source files
    ("/etc/modules-load.d/br_netfilter.conf", 420, "data:,br_netfilter"),

    # Content files
    ("/etc/mellanox/mlnx-bf.conf", 644, "mlnx-bf.conf"),
    ("/etc/mellanox/mlnx-ovs.conf", 644, "mlnx-ovs.conf"),
    ("/etc/NetworkManager/system-connections/pf0vf0.nmconnection",
     600, "pf0vf0.nmconnection"),
    ("/etc/NetworkManager/system-connections/br-comm-ch.nmconnection",
     600, "br-comm-ch.nmconnection"),
    ("/etc/NetworkManager/system-connections/tmfifo_net0.nmconnection",
     600, "tmfifo_net0.nmconnection"),
    ("/etc/NetworkManager/system-connections/oob_net0.nmconnection",
     600, "oob_net0.nmconnection"),
    ("/etc/crio/crio.conf.d/99-ulimits.conf", 644, "99-ulimits.conf"),
    ("/etc/sysctl.d/98-dpunet.conf", 644, "98-dpunet.conf"),
    ("/usr/local/bin/dpf-configure-sfs.sh", 644, "dpf-configure-sfs.sh"),
    ("/usr/local/bin/set-nvconfig-params.sh", 755, "set-nvconfig-params.sh"),
    ("/etc/sysconfig/openvswitch", 600, "openvswitch"),
]
