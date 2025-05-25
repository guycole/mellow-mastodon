# plot bin-sample1
set title 'bin-sample1'
set xlabel 'frequency'
set ylabel 'dbm'
set grid
#
set terminal png size 1200,800
set output 'bin-sample1.png'
plot 'bin-sample1.dat'
#
