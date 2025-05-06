{
  description = "NixOS infrastructure";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-25.11";

    sops-nix = {
      url = "github:Mic92/sops-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    disko = {
      url = "github:nix-community/disko";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, disko, sops-nix, ... }@inputs: {
    colmena = {
      meta = {
        nixpkgs = import nixpkgs {
          system = "x86_64-linux";
          config.allowUnfree = true;
        };
        specialArgs = { inherit inputs; };
      };

      homelab = {
        deployment = {
          targetHost = "192.168.1.4";
          targetUser = "rean";
          privilegeEscalationCommand = [ "sudo" "-S" ];
        };

        imports = [
          disko.nixosModules.disko
          inputs.sops-nix.nixosModules.sops
          ./hosts/homelab/configuration.nix
        ];
      };
    };

    nixosConfigurations.homelab = nixpkgs.lib.nixosSystem {
      system = "x86_64-linux";
      specialArgs = { inherit inputs; };
      modules = [
        disko.nixosModules.disko
        sops-nix.nixosModules.sops
        ./hosts/homelab/configuration.nix
        ./modules/common.nix
      ];
    };
  };
}
