I am following the documentation of FALL3D. It contains a section specifically made
for installing FALL3D on EuroHPC. It also mentions BSC MareNostrum5 and CSC LUMI,
two platforms I have access to right now.

<https://fall3d-suite.gitlab.io/fall3d/chapters/installationHPC.html>

## BSC MareNostrum 5

I chose to compile the version without GPU support, and only MPI, no OpenACC.
Looking at the list of modules listed in their documentation for MareNostrum,
I believe these are the modules that I have to load:

```bash
module purge
module load EB/apps
module load CMake
module load netCDF-Fortran/4.6.1-gompi-2023b
```

And then to build it with CMake:

```bash
cmake .. -DDETAIL_BIN=YES -DWITH-MPI=YES -DWITH-ACC=NO -DWITH-R4=NO
make -j8
```

Make fails, however, with this error:

```bash
[me@glogin4 build]$ cat CMakeFiles/Fall3d.GNU.r8.mpi.cpu.x.dir/link.txt /apps/GPP/EASYBUILD/software/OpenMPI/4.1.6-GCC-13.2.0/bin/mpif90 -Wl,-rpath -Wl,/apps/GPP/EASYBUILD/software/OpenMPI/4.1.6-GCC-13.2.0/lib -Wl,/apps/GPP/EASYBUILD/software/hwloc/2.9.2-GCCcore-13.2.0/lib -Wl,/apps/GPP/EASYBUILD/software/libevent/2.1.12-GCCcore-13.2.0/lib -Wl,--enable-new-dtags -L/gpfs/apps/MN5/GPP/EASYBUILD/software/OpenMPI/4.1.6-GCC-13.2.0/lib -L/gpfs/apps/MN5/GPP/EASYBUILD/software/hwloc/2.9.2-GCCcore-13.2.0/lib -L/gpfs/apps/MN5/GPP/EASYBUILD/software/libevent/2.1.12-GCCcore-13.2.0/lib CMakeFiles/Fall3d.GNU.r8.mpi.cpu.x.dir/Sources/main.F90.o CMakeFiles/Fall3d.GNU.r8.mpi.cpu.x.dir/Sources/mod_ADS.F90.o CMakeFiles/Fall3d.GNU.r8.mpi.cpu.x.dir/Sources/mod_Coord.F90.o CMakeFiles/Fall3d.GNU.r8.mpi.cpu.x.dir/Sources/mod_Dbs.F90.o CMakeFiles/Fall3d.GNU.r8.mpi.cpu.x.dir/Sources/mod_Deposit.F90.o CMakeFiles/Fall3d.GNU.r8.mpi.cpu.x.dir/Sources/mod_Domain.F90.o CMakeFiles/Fall3d.GNU.r8.mpi.cpu.x.dir/Sources/mod_Ensemble.F90.o CMakeFiles/Fall3d.GNU.r8.mpi.cpu.x.dir/Sources/mod_F3D.F90.o CMakeFiles/Fall3d.GNU.r8.mpi.cpu.x.dir/Sources/mod_Grid.F90.o CMakeFiles/Fall3d.GNU.r8.mpi.cpu.x.dir/Sources/mod_Grn.F90.o CMakeFiles/Fall3d.GNU.r8.mpi.cpu.x.dir/Sources/mod_InpOut.F90.o CMakeFiles/Fall3d.GNU.r8.mpi.cpu.x.dir/Sources/mod_KindType.F90.o CMakeFiles/Fall3d.GNU.r8.mpi.cpu.x.dir/Sources/mod_Maths.F90.o CMakeFiles/Fall3d.GNU.r8.mpi.cpu.x.dir/Sources/mod_Parallel.F90.o CMakeFiles/Fall3d.GNU.r8.mpi.cpu.x.dir/Sources/mod_Phys.F90.o CMakeFiles/Fall3d.GNU.r8.mpi.cpu.x.dir/Sources/mod_PlumeBPT.F90.o CMakeFiles/Fall3d.GNU.r8.mpi.cpu.x.dir/Sources/mod_Postp.F90.o CMakeFiles/Fall3d.GNU.r8.mpi.cpu.x.dir/Sources/mod_Sat.F90.o CMakeFiles/Fall3d.GNU.r8.mpi.cpu.x.dir/Sources/mod_Shared.F90.o CMakeFiles/Fall3d.GNU.r8.mpi.cpu.x.dir/Sources/mod_Src.F90.o CMakeFiles/Fall3d.GNU.r8.mpi.cpu.x.dir/Sources/mod_StdAtm.F90.o CMakeFiles/Fall3d.GNU.r8.mpi.cpu.x.dir/Sources/mod_Tgsd.F90.o CMakeFiles/Fall3d.GNU.r8.mpi.cpu.x.dir/Sources/mod_Time.F90.o CMakeFiles/Fall3d.GNU.r8.mpi.cpu.x.dir/Sources/mod_Validation.F90.o CMakeFiles/Fall3d.GNU.r8.mpi.cpu.x.dir/Sources/mod_Variables.F90.o CMakeFiles/Fall3d.GNU.r8.mpi.cpu.x.dir/Sources/mod_detect_gpu.F90.o CMakeFiles/Fall3d.GNU.r8.mpi.cpu.x.dir/Sources/mod_json_IO.F90.o CMakeFiles/Fall3d.GNU.r8.mpi.cpu.x.dir/Sources/mod_lsode.F90.o CMakeFiles/Fall3d.GNU.r8.mpi.cpu.x.dir/Sources/mod_ncIO.F90.o CMakeFiles/Fall3d.GNU.r8.mpi.cpu.x.dir/Sources/mod_nc_IO.F90.o CMakeFiles/Fall3d.GNU.r8.mpi.cpu.x.dir/Sources/mod_nc_IO_names.F90.o CMakeFiles/Fall3d.GNU.r8.mpi.cpu.x.dir/Sources/task_Fall3d.F90.o CMakeFiles/Fall3d.GNU.r8.mpi.cpu.x.dir/Sources/task_Manager.F90.o CMakeFiles/Fall3d.GNU.r8.mpi.cpu.x.dir/Sources/task_PosEns.F90.o CMakeFiles/Fall3d.GNU.r8.mpi.cpu.x.dir/Sources/task_PosVal.F90.o CMakeFiles/Fall3d.GNU.r8.mpi.cpu.x.dir/Sources/task_SetDbs.F90.o CMakeFiles/Fall3d.GNU.r8.mpi.cpu.x.dir/Sources/task_SetEns.F90.o CMakeFiles/Fall3d.GNU.r8.mpi.cpu.x.dir/Sources/task_SetSrc.F90.o CMakeFiles/Fall3d.GNU.r8.mpi.cpu.x.dir/Sources/task_SetTgsd.F90.o CMakeFiles/Fall3d.GNU.r8.mpi.cpu.x.dir/mod_Config.f90.o -o bin/Fall3d.GNU.r8.mpi.cpu.x /apps/GPP/EASYBUILD/software/netCDF-Fortran/4.6.1-gompi-2023b/lib/libnetcdff.so /apps/GPP/EASYBUILD/software/netCDF/4.9.2-gompi-2023b/lib/libnetcdf.so
```

The linker is receivin a directory in `-Wl,`, and `ld` tried to read it as a file. This
can be fixed with:

```bash
$ sed -i \
-e 's|-Wl,/apps/GPP/EASYBUILD/software/hwloc/2.9.2-GCCcore-13.2.0/lib||g' \
-e 's|-Wl,/apps/GPP/EASYBUILD/software/libevent/2.1.12-GCCcore-13.2.0/lib||g' \
CMakeFiles/Fall3d.GNU.r8.mpi.cpu.x.dir/link.txt
```

And then to test the binary:

```bash
$ ./bin/Fall3d.GNU.r8.mpi.cpu.x 
--------------------------------------------------------------------------
                                                                          
                ______      _      _      ____  _____                     
               |  ____/\   | |    | |    |___ \|  __ \                    
               | |__ /  \  | |    | |      __) | |  | |                   
               |  __/ /\ \ | |    | |     |__ <| |  | |                   
               | | / ____ \| |____| |____ ___) | |__| |                   
               |_|/_/    \_\______|______|____/|_____/                    
                                                                          
                                                                          
       Copyright: 2018 GNU General Public License version 3               
                    (see licence for details)                             
                                                                          
  model version: 9.1.0-19-gdefecae/master                                                    
                                                                          
  usage:                                                                  
   Fall3d.x Task InputFile [NPX] [NPY] [NPZ] [-nens SIZE]                 
                                                                          
  positional arguments:                                                   
   Task (single)   : SetTgsd, SetDbs, SetSrc, Fall3d, PosEns, PosVal      
   Task (multiple) : All (1-4 above)                                      
   InputFile       : Parameter input file                                 
                                                                          
  optional arguments:                                                     
   NPX        : processors (sub-domains) along x (default NPX =1 )        
   NPY        : processors (sub-domains) along y (default NPY =1 )        
   NPZ        : processors (sub-domains) along z (default NPZ =1 )        
   -nens SIZE : ensemble size                    (default SIZE=1 )        
                                                                          
  note:                                                                   
   For parallel runs it is required that  NPROC = NPX * NPY * NPZ * SIZE  
                                                                          
  examples:                                                               
   1. Run SetTgsd utility                                                 
   > Fall3d.x SetTgsd problemname.inp [-nens ENS_SIZE]                    
                                                                          
   2. Run SetDbs utility                                                  
   > Fall3d.x SetDbs problemname.inp [NPX NPY NPZ -nens ENS_SIZE]         
                                                                          
   3. Run SetSrc utility                                                  
   > Fall3d.x SetSrc problemname.inp [NPX NPY NPZ -nens ENS_SIZE]         
                                                                          
   4. Run Fall3d solver                                                   
   > Fall3d.x Fall3d problemname.inp [NPX NPY NPZ -nens ENS_SIZE]         
                                                                          
   5. Run PosEns utility                                                  
   > Fall3d.x PosEns problemname.inp [-nens ENS_SIZE]                     
                                                                          
   6. Run PosVal utility                                                  
   > Fall3d.x PosVal problemname.inp [NPX NPY]                            
                                                                          
   7. Run tasks 1-4 above consecutively                                   
   > Fall3d.x All problemname.inp [NPX NPY NPZ -nens ENS_SIZE]            
                                                                          
--------------------------------------------------------------------------
<ERR> Missing mandatory arguments
```
