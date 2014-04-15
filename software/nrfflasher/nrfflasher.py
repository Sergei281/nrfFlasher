#! /usr/bin/env python
import serial
from time import sleep
from sys import argv

debug = False
open_port_delay = 1.7

def get_args(): # Small command-line parser. Yep it's squared-wheels bicycle
	if not argv[1:]: return {'filename': argv[0]}
	data = ' '.join(argv[1:])
	data = data.split(' -')
	data[0] = data[0][1:]
	data = dict([element.split(' ', 1) if ' ' in element else [element] + [True] for element in data]) # Magic
	data.update({'filename': argv[0]})
	return data

def device_search():
	for port_num in range(256):
		answer = None
		try:
			serial_port = serial.Serial(port_num, 9600, timeout=0.1)
			sleep(open_port_delay)
			serial_port.write('T')
			answer = serial_port.read(2)
			port_name = serial_port.portstr
			serial_port.close()
		except serial.SerialException:
			pass
		if answer == 'OK':
			return port_num, port_name
	return None

def main():
	print 'Hello nrf24LE1! :)'
	start_args = get_args()
	if ('h' in start_args) or (not (('w' in start_args) or ('e' in start_args) or ('r' in start_args))): # Help
		print "Don't wait help."
		exit(0)
	if ((('w' in start_args) and ('r' in start_args)) or
		(('w' in start_args) and ('e' in start_args)) or
		(('r' in start_args) and ('e' in start_args))):
		print 'What the fuck are you doing?!'
		exit(666)
	device_port = device_search()
	if not device_port:
		print '404 Device Not Found'
		exit(1)
	if debug: print 'Device port:', device_port

	serial_port = serial.Serial(device_port[0], 9600, timeout=0.1) # Open port for random actions
	sleep(open_port_delay)
	serial_port.write('V')
	answer = serial_port.read(15)
	if answer[-2:] <> 'OK':
		print '502 Bad Device'
		exit(2)
	if debug: print 'Device f/w version:', answer[:-2]
	if debug: print start_args	# e - erase; w - write; r - read;

	if 'e' in start_args: # Erase
		print 'Erasing...'
		serial_port.write('E')
		#serial_port.timeout = 5 # Fuck!
		sleep(5)
		answer = serial_port.read(2)
		if answer == 'OK':
			print 'Yahoo!'
			exit(0)
		else:
			print 'Erasing error!'
			exit(3)
		serial_port.timeout = 0.1

	if 'r' in start_args: # Read
		print 'Reading...'

	if 'w' in start_args: # Write
		print 'Writing...'

	serial_port.close()

if __name__ == '__main__':
	main()
