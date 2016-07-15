#!/bin/bash

PORT=8777
if [ "${use_port}" != "" ]; then
   PORT=${use_port}
   echo $PORT
fi

if [ "$dataset_hid" != "" ]; then
  echo $dataset_hid
  pvpython /usr/local/lib/paraview-5.1/site-packages/paraview/web/pv_web_visualizer.py \
         --content /usr/local/share/paraview-5.1/www \
         --data-dir /import \
         --save-data-dir /export \
	 --load-file $dataset_hid \
         --port ${PORT}
else
  pvpython /usr/local/lib/paraview-5.1/site-packages/paraview/web/pv_web_visualizer.py \
         --content /usr/local/share/paraview-5.1/www \
         --data-dir /import \
         --save-data-dir /export \
         --port ${PORT}
fi
