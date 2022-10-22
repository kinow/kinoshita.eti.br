---
categories:
- blog
date: "2021-10-17T00:00:00Z"
tags:
- opensource
- blender
title: Blender rendering on NVIDIA Jetson Nano
---

<img src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/jetson.jpg" alt="NVIDIA Jetson Nano computer" class="center-aligned" />

I had used Blender during my graduation at the Mackenzie University and started learning
Blender 2.8+ again a few weeks ago. Unfortunately rendering the basic tutorials like Andrew
Price's donut takes several minutes on my old (but excellent for programming) Thinkpad
T550 i7 16 GB with a simple Samsung SSD. The reason is that my GPU, a
[NVIDIA NVS 5400M](https://www.techpowerup.com/gpu-specs/nvs-5400m.c1742)
with 2 GB memory and 96 cores cannot be used with Blender as it only supports CUDA 2.1.
Blender 2.8+ GPU rendering requires CUDA 3.0 and higher, which means Blender Cycles
render is using my CPU, which is slower than using a decent GPU.

Since I am really happy with my (refurbished) Thinkpad T550 and prefer to avoid buying
a new computer unless I really need to, my first idea was a GPU (egpu). These are simple
kits that allow you to connect a GPU to a notebook like mine using an adapter and some
port like thunderbolt, m.2 (removing wi-fi card), etc. But all these options are expensive
and the bandwidth is not near as good as using a GPU plugged in the motherboard.

<img src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/donut.png" alt="Andrew Price (Blender Guru) donut" class="center-aligned" />

A few months ago I heard about the [NVIDIA Jetson Nano](https://developer.nvidia.com/embedded/jetson-nano)
board computer. They are small board computers for embedded applications. Using an
ARM CPU and equipped with [a GPU](https://www.techpowerup.com/gpu-specs/jetson-nano-gpu.c3643)
with **128 cores**. The computer has **4 GB memory that is shared between the operating
system and the graphics processor**. And the NVIDIA Jetson Nano GPU supports CUDA 5.3,
which means it can be used by Blender to render scenes in the GPU.

<img src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/suzanne.png" alt="A blender scene with Suzanne and modifiers" class="center-aligned" />

After following the Jetson Nano documentation to install it using an SD disk,
and enabling the performance overclock mode, I used `apt-get` to install Blender.
The first thing I noticed is that it installed Blender 2.7. I tried downloading
2.8 since I had a few files created with this version, but then I realized I had
downloaded the x86_64 version. I couldn't find 2.8 build for arm, so instead I
selected two files:

- One with Suzanne, the Blender monkey, configured with smaller tiles and added
a modifier to smooth it (I assumed that way it would use more of the GPU.)
- The other one was the Blender 2.7 [splash screen](https://www.blender.org/download/demo-files/)

I installed the same version of Blender, 2.7, on my Ubuntu Thinkpad, and configured the
tiles size on both files, and selected GPU rendering. Then I `scp`ed it to the NVIDIA
Jetson Nano Ubuntu, and set the render engine back to CPU on my Ubuntu.

<img src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/splashscreen.png" alt="Blender 2.7 splash demo image" class="center-aligned" />

First I rendered Suzanne on my Thinkpad using the CPU. It took **11 seconds to render**
the scene.

```bash
kinow@ranma:~/Downloads/blender$ /opt/blender-2.79-linux-glibc219-x86_64/blender -b b-jetson.blend -o ./ -f 1
found bundled python: /opt/blender-2.79-linux-glibc219-x86_64/2.79/python
Read blend: /home/kinow/Downloads/blender/b-jetson.blend
Fra:1 Mem:260.65M (0.00M, Peak 525.85M) | Time:00:01.68 | Preparing Scene data
Fra:1 Mem:260.67M (0.00M, Peak 525.85M) | Time:00:01.68 | Preparing Scene data
Fra:1 Mem:260.67M (0.00M, Peak 525.85M) | Time:00:01.68 | Creating Shadowbuffers
Fra:1 Mem:260.67M (0.00M, Peak 525.85M) | Time:00:01.68 | Raytree.. preparing
Fra:1 Mem:560.45M (0.00M, Peak 560.45M) | Time:00:01.87 | Raytree.. building
(...)
Fra:1 Mem:545.16M (0.00M, Peak 1012.27M) | Time:00:11.36 | Scene, Part 82-135
Fra:1 Mem:544.70M (0.00M, Peak 1012.27M) | Time:00:11.39 | Scene, Part 86-135
Fra:1 Mem:16.93M (0.00M, Peak 1012.27M) | Time:00:11.43 | Sce: Scene Ve:2016578 Fa:2182948 La:1
Saved: './0001.png'
 Time: 00:11.49 (Saving: 00:00.06)
```

Tried the same command on my NVIDIA Jetson Nano now. It took **48 seconds**. Near 4 times
longer than my old Thinkpad.

```bash
root@kinow-jetson:/home/kinow# blender -b b-jetson.blend -o ./ -f 1
AL lib: (EE) UpdateDeviceParams: Failed to set 44100hz, got 48000hz instead
Read blend: /home/kinow/b-jetson.blend
Fra:1 Mem:260.50M (0.00M, Peak 525.70M) | Time:00:05.27 | Preparing Scene data
Fra:1 Mem:260.51M (0.00M, Peak 525.70M) | Time:00:05.27 | Preparing Scene data
(...)
Fra:1 Mem:594.15M (0.00M, Peak 727.22M) | Time:00:48.26 | Scene, Part 86-135
Fra:1 Mem:16.78M (0.00M, Peak 727.22M) | Time:00:48.36 | Sce: Scene Ve:2016578 Fa:2183144 La:1
Saved: './0001.png'
 Time: 00:48.53 (Saving: 00:00.17)
```

I thought it could be because my scene was too simple for the CPU to render,
so the GPU was being slower maybe due to the tile sizes or CPU<->memory context
switching.

So I tried the Splash screen now. **01 hour and 53 minutes** on my Thinkpad.

```bash
Fra:1 Mem:2088.19M (0.00M, Peak 4612.16M) | Time:01:53:53.18 | Sce: Scene Ve:0 Fa:0 La:0
Saved: './0001.png'
 Time: 01:53:54.08 (Saving: 00:00.90)
```

And on the NVIDIA Jetson Nano, **22 hours and 38 minutes**.

```bash
Fra:1 Mem:2088.40M (0.00M, Peak 4612.39M) | Time:22:38.00 | Sce: Scene Ve:0 Fa:0 La:0
Saved: './0001.png'
 Time: 22:38.22 (Saving: 00:00.21)
```

I did a few more experiments using the Suzanne file. Tried different command line
arguments, specifying the engine, number of threads, debug GPU to see if I could
see any warnings. But alas I could not find a setup that could speed up the process.

Even tried a Python script I found in a forum to see this way the NVIDIA Jetson
Nano board would perform better.

```python
import bpy


def enable_gpus(device_type, use_cpus=False):
    preferences = bpy.context.preferences
    cycles_preferences = preferences.addons["cycles"].preferences
    cuda_devices, opencl_devices = cycles_preferences.get_devices()

    if device_type == "CUDA":
        devices = cuda_devices
    elif device_type == "OPENCL":
        devices = opencl_devices
    else:
        raise RuntimeError("Unsupported device type")

    activated_gpus = []

    for device in devices:
        if device.type == "CPU":
            device.use = use_cpus
        else:
            device.use = True
            activated_gpus.append(device.name)

    cycles_preferences.compute_device_type = device_type
    bpy.context.scene.cycles.device = "GPU"

    return activated_gpus


enable_gpus("CUDA")
```

The render was about the same time, a little slower, probably because Blender
needs to load and execute the Python script. After reading about users with
slow render times (not necessarily because of egpu or board computer GPU's),
some users mentioned the kind of scene or file, and also the system memory.

My old Thinkpad has 16 GB memory, where normally about 14 GB are free for Blender
to use while rendering. And even my old GPU, with its 2 GB dedicated memory would
probably perform about the same I guess with Blender, if it supported newer CUDA
versions (which means, if it also had a newer processor.)

```bash
kinow@ranma:~$ nvidia-smi 
Tue Sep 28 23:44:54 2021       
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 390.144                Driver Version: 390.144                   |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  NVS 5400M           Off  | 00000000:01:00.0 N/A |                  N/A |
| N/A   56C    P0    N/A /  N/A |    294MiB /   964MiB |     N/A      Default |
+-------------------------------+----------------------+----------------------+
                                                                               
+-----------------------------------------------------------------------------+
| Processes:                                                       GPU Memory |
|  GPU       PID   Type   Process name                             Usage      |
|=============================================================================|
|    0                    Not Supported                                       |
+-----------------------------------------------------------------------------+
```

The NVIDIA Jetson Nano, with no GUI (I uninstalled `ubuntu-desktop`, `mousepad`,
and disabled firewall and any other service that I considered unnecessary for Blender)
starts with ~600 MB of used memory, leaving 3.2 GB for Blender and for the GPU.

```bash
kinow@kinow-jetson:~$ ./mem
  mem free 3295.226562 MB mem total 3964.101562 MB mem used 668.875000 MB
```

My guess is that while the NVIDIA Jetson Nano board works well for AI and IoT
applications that need the GPU for calculations that are not affected by the
shared memory, rendering 3D scenes in Blender would still perform better in
an egpu or in an environment with a new GPU.

But at least I confirmed that you can render files in these board computers, and
it was a fun project. Things I am still thinking in trying someday:

- Compile and try Blender 3.x for arm
- Learn more about the Blender Python API and try to write some sort of debug function
- Investigate if AI/machine learning applications have the same kind of problems (e.g.
[see this tensorflow issue](https://github.com/tensorflow/tensorflow/issues/39486))

These boards are really fun, and support plugging cameras like the Raspberry Pi camera.
So it could be used for things like [counting number of bees](https://techcrunch.com/2018/06/01/count-your-bees-with-this-raspberry-pi-project/),
or estimate the [pose of a body](https://www.youtube.com/watch?v=nUjGLjOmF7o&list=WL&index=14).

With dedicated memory for the graphics processor, it could probably perform a lot
better, but the CPU would also have to be improved a little, as well as the power
unit… and I suspect the cost would increase too. So not sure if at that point it
would not make more sense to buy an egpu or a dedicated workstation for Blender.

For now, I am keeping my Thinkpad and will keep thinking how to improve my rendering
time.

>Special thanks to Luke Reid for donating his NVIDIA Jetson Nano so I could test it
>with Blender
