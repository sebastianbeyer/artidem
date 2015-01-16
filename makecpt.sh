#!/bin/bash


cpt="./nicetopo.cpt"

# some colors
C1="156 187 169"
C2="169 204 164"
C3="196 212 170"
C4="228 232 202"
#39 14.6 91.4
C5="196 204 187"
C6="187 187 187"
C7="255 255 255"


# header
echo "# nice topo colors" > $cpt
echo "#" >> $cpt
echo "# COLOR_MODEL = RGB" >> $cpt

# colors
echo   "0 "$C1" 100 "$C2 >> $cpt
echo "100 "$C2" 200 "$C3 >> $cpt
echo "200 "$C3" 300 "$C4 >> $cpt
echo "300 "$C4" 400 "$C5 >> $cpt
echo "400 "$C5" 500 "$C6 >> $cpt
echo "500 "$C6" 600 "$C7 >> $cpt

# footer
echo "F 255 255 255" >> $cpt
echo "B 130 160 140" >> $cpt
echo "N 180 0.0 0.5" >> $cpt


