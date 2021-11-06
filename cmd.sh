ffmpeg \
	-framerate 0.75 \
	-f image2 \
	-i ./assets/plots-riemann-sumdump-osc-%04d.png \
	-c:v libvpx-vp9 \
	-pix_fmt yuva420p dumpos2.webm
