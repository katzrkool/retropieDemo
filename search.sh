#!/bin/bash
grep -rnw "/opt/retropie/libretrocores/" -e $1 | head -1