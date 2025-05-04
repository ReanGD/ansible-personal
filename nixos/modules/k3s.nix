{ config, pkgs, ... }:

{
  services.k3s = {
    enable = true;
    role = "server";
    configPath = config.sops.templates."k3s-conf".path;
  };

  sops.templates."k3s-conf".content = ''
    cluster-init: true
    disable:
      - traefik
      - servicelb
    tls-san:
      - "${config.sops.placeholder."k3s/public_ip"}"
      - "${config.sops.placeholder."k3s/local_ip"}"
    token: "${config.sops.placeholder."k3s/token"}"
    write-kubeconfig-mode: "0644"
    bind-address: "0.0.0.0"
  '';

  boot.kernelModules = [ "overlay" "br_netfilter" ];

  networking.firewall = {
    allowedTCPPorts = [ 6443 80 443 2379 2380 10250 ];
    allowedUDPPorts = [ 8472 ];
  };

  environment.systemPackages = with pkgs; [ k3s kubectl kubernetes-helm ];
  environment.variables.KUBECONFIG = "/etc/rancher/k3s/k3s.yaml";
}
