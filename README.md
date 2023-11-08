# photo-recovery

1. Make image of corrupted SD card
```
dd if=/dev/sdb of=sd.img
```

2. Get scalpel and pyexiftool
```
sudo apt install scalpel exfiftool # Ubuntu/Debian
pip3 install pyexiftool 
```

3. Check scalpel config for file formats. I just needed jpgs for now:
```
[...]
	jpg	y	5242880		\xff\xd8\xff???Exif		\xff\xd9	REVERSE
	jpg	y	5242880		\xff\xd8\xff???JFIF		\xff\xd9	REVERSE
[...]
```

4. Run scalpel
```
scalpel -c scalpel.conf -o ./scalpel-out sd.img
```

5. Post process
```
./post-process.py --in ./scalpel-out --out ./processed
```
