#!/bin/sh
./scripts/build-docs.sh
scp -r site/* ekiim@ekiim.xyz:/var/www/xyz.ekiim.odeanimate/
