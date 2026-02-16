## Issue

When using Bluetooth headphones, when I have Netflix or Youtube playing on one
tab in Firefox, closing Twitter, DeviantArt, AliExpress, others, result in a
momentary glitch in the audio.

> ※ `pw-top` will show the streams under `bluez` service, opening the tab and closing it will
> show the new stream created, then destroyed, and when it is destroyed the glitch happens.

This happened with Kernel 5, 6, and Ubuntu LTS 24.10, and Ubuntu 25.04.

This fixed it, creating these two files:

1. `~/.config/pipewire/pipewire.conf.d/99-bluez.conf`

```json
monitor.bluez.properties = {
    bluez5.default.rate = 48000
    bluez5.default.channels = 2
    bluez5.default.format = "S16LE"
}
```

2. `~/.config/pipewire/pipewire.conf.d/99-clock.conf`

```json
context.properties = {
    default.clock.rate          = 48000
    default.clock.quantum       = 1024
    default.clock.min-quantum   = 1024
    default.clock.max-quantum   = 2048
    default.clock.allowed-rates = [ 48000 ]
}
```

And restarting the service with `systemctl --user restart pipewire pipewire-pulse wireplumber`.

The restart will cause the Bluetooth audio to disconnect, and then reconnect.
I noticed no delay on Firefox playing videos.

