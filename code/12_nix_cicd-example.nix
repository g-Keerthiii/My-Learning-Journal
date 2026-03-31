{
  description = "Reproducible dev shell for the learning journal";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
    in {
      devShells.${system}.default = pkgs.mkShell {
        buildInputs = [
          pkgs.git
          pkgs.python3
          pkgs.nodejs_22
        ];

        shellHook = ''
          echo "nix shell ready"
        '';
      };
    };
}
