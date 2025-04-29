{
  description = "NixOS infrastructure";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-25.11";
    disko = {
      url = "github:nix-community/disko";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, disko, ... }: {
    colmena = {
      meta = {
        nixpkgs = import nixpkgs {
          system = "x86_64-linux";
          config.allowUnfree = true;
        };
      };

      homelab = {
        deployment = {
          targetHost = "192.168.1.4";
          targetUser = "rean";
          privilegeEscalationCommand = [ "sudo" "-S" ];
        };

        imports = [
          disko.nixosModules.disko
          ./hosts/homelab/configuration.nix
        ];
      };
    };

    nixosConfigurations.homelab = nixpkgs.lib.nixosSystem {
      system = "x86_64-linux";
      modules = [
        disko.nixosModules.disko
        ./hosts/homelab/configuration.nix
      ];
    };
  };
}
