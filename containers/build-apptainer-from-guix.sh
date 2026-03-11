#!/bin/bash

export squashfs_file=$(guix time-machine --channels=guix/channels.scm -- pack -f squashfs --manifest=guix/theo_opt_lectures-manifest.scm | tail -n 1)

echo "SquashFS file created: ${squashfs_file}"

sed -i "s|From: /gnu/store.*|From: ${squashfs_file}|g" def-files/from-guix-definition.def

CODE_DIR=$(pwd | sed "s,/containers,,g")

sed -i "s|/.*/theo_opt/\*\.py /opt|${CODE_DIR}/*.py /opt|g" def-files/from-guix-definition.def
sed -i "s|/.*/theo_opt/stuff /opt|${CODE_DIR}/stuff /opt|g" def-files/from-guix-definition.def
sed -i "s|/.*/theo_opt/man /opt|${CODE_DIR}/man /opt|g" def-files/from-guix-definition.def
sed -i "s|/.*/theo_opt/EMpy /opt|${CODE_DIR}/EMpy /opt|g" def-files/from-guix-definition.def


apptainer build images/theo_opt_interactive.sif def-files/from-guix-definition.def

echo "Apptainer image built: images/theo_opt_interactive.sif"
echo "You can run the image using:"
echo "    apptainer run images/theo_opt_interactive.sif"
echo "For extensive details on how to use the image, please run"
echo "    apptainer run-help images/theo_opt_interactive.sif"