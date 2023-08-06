setlocal EnableDelayedExpansion
set "cl_cfg_orig=%PREFIX%\Library\lib\cl.cfg"
set "cl_cfg_temp=%PREFIX%\Library\lib\cl.cfg.temp"
powershell -Command "(gc '%cl_cfg_orig%') -replace 'CL_CONFIG_TBB_DLL_PATH = .*', 'CL_CONFIG_TBB_DLL_PATH =' | Out-File -encoding ASCII -FilePath '%cl_cfg_temp%'"
move /Y "%cl_cfg_temp%" "%cl_cfg_orig%"
