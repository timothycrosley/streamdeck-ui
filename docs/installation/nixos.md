# Installing on NixOS

See also the [Stream Deck](https://nixos.wiki/wiki/Stream_Deck) page on the NixOS Wiki.

## NixOS module

This is the preferred method so that udev rules are automatically set up.

```nix
{
  programs.streamdeck-ui = {
    enable = true;
    autoStart = true; # optional
  };
}
```

## Nix package

If you are using Nix on a distribution other than NixOS, you can use the `streamdeck-ui` package from `nixpkgs`.

The package contains udev rules at `/nix/store/<package-path>/etc/udev/rules.d/70-streamdeck.rules`. These rules must be enabled for your user to access Elgato USB devices.
