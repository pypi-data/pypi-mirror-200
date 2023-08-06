setlocal EnableDelayedExpansion
set "cl_cfg_orig=%PREFIX%\Library\lib\cl.cfg"
set "cl_cfg_temp=%PREFIX%\Library\lib\cl.cfg.temp"
set "lib_bin=%PREFIX%\Library\bin"
set "PATH=%PATH%;C:\Windows\System32\WindowsPowerShell\v1.0;C:\Windows\System32"
powershell -Command "(gc '%cl_cfg_orig%') -replace 'CL_CONFIG_TBB_DLL_PATH =.*', 'CL_CONFIG_TBB_DLL_PATH = %lib_bin%' | Out-File -Encoding ASCII -FilePath '%cl_cfg_temp%'"
move /Y "%cl_cfg_temp%" "%cl_cfg_orig%"
