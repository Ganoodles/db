# shell.nix
{ pkgs ? import <nixpkgs> {} }:
let
  packages = ps: with ps; [

    (
      buildPythonPackage rec {
        pname = "tortoise_orm";
        version = "0.19.3";
        src = fetchPypi {
          inherit pname version;
          sha256 = "sha256-yldLylGR9VYI+QEzFLH10cb/1BZaH8wvYPbJAvUps7Y=";
        };
        doCheck = false;
        propagatedBuildInputs = [
          # Specify dependencies
          pkgs.python310Packages.iso8601
          pkgs.python310Packages.pytz
          pkgs.python310Packages.aiosqlite
          pkgs.python310Packages.typing-extensions
          
          (
            buildPythonPackage rec {
              pname = "pypika-tortoise";
              version = "0.1.6";
              src = fetchPypi {
                inherit pname version;
                sha256 = "sha256-2AKGj0eacI4yY3JMe1cZomrXk5mypwzqBl9KTK2+vzY=";
              };
              doCheck = false;
              propagatedBuildInputs = [
                # Specify dependencies
              ];
            }
          )
        ];
      }
    )

  ];
  custom-packages = pkgs.python310Full.withPackages packages;
in 
  pkgs.mkShell {
    nativeBuildInputs = with pkgs.buildPackages; [
      (python310.withPackages(ps: with ps; [ 
        pip
        discordpy
        python-dotenv
        colorama

        # linting
        black
        pylint
        mypy
      ]))

      custom-packages

      hatch
      poetry
    ];
  }