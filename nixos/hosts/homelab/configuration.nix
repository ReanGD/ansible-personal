{ config, pkgs, modulesPath, inputs, ... }:

{
  imports = [
    inputs.sops-nix.nixosModules.sops
    (modulesPath + "/installer/scan/not-detected.nix")
     ../../modules/k3s.nix
    ./disk-config.nix
  ];

  networking.hostName = "homelab";
  networking.networkmanager.enable = true;

  boot.loader.systemd-boot.enable = true;
  boot.loader.efi.canTouchEfiVariables = true;

  sops = {
    defaultSopsFile = ./secrets/secrets.yaml;
    defaultSopsFormat = "yaml";

    # private key
    age.keyFile = "/var/lib/sops-nix/key.txt";
    secrets = {
      "k3s/token" = { };
      "k3s/public_ip" = { };
      "k3s/local_ip" = { };
    };
  };

  services.openssh = {
    enable = true;
    settings = {
      PermitRootLogin = "prohibit-password";
      PasswordAuthentication = false;
    };
  };

  users.users.rean = {
    isNormalUser = true;
    extraGroups = [ "wheel" "networkmanager" ];
    openssh.authorizedKeys.keys = [
      "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIFEQ9TF0OaX0IH2WaMjFXoxIfLud1q1VTUDICo6Rz+vi homelab-server"
    ];
  };

  security.sudo.wheelNeedsPassword = false;

  networking.firewall = {
    enable = true;
    allowedTCPPorts = [ 22 ];
  };

  systemd.tmpfiles.rules = [
    "d /var/lib/sops-nix 0700 root root -"
  ];

  system.stateVersion = "25.11";
}
