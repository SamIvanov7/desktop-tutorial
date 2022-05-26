import os
import sys
import time
import datetime
import traceback
import threading
import subprocess


daemon_pid = '/var/run/start_and_restart_auction_manager_app.pid'
install_dir = '/usr/local/auction_manager_app'
lock_1 = threading.Lock()

class color_print:
	@staticmethod
	def print_fail(message):
		sys.stderr.write('\x1b[1;31m'+message.strip()+'\x1b[0m'+'\n')

	@staticmethod
	def print_pass(message):
		sys.stdout.write('\x1b[1;32m'+message.strip()+'\x1b[0m'+'\n')

	@staticmethod
	def print_warn(message):
		sys.stderr.write('\x1b[1;33m'+message.strip()+'\x1b[0m'+'\n')

	@staticmethod
	def print_info(message):
		sys.stdout.write('\x1b[1;34m'+message.strip()+'\x1b[0m'+'\n')

	@staticmethod
	def print_bold(message):
		sys.stdout.write('\x1b[1;37m'+message.strip()+'\x1b[0m'+'\n')

try:
	from daemon import daemon
except Exception:
	color_print.print_fail(traceback.format_exc().strip())
	sys.exit(1)

def log_error(mes):

	date = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
	mes = date+' '+mes+'\r\n----------------------------------------------------------------------------------------\r\n'
	
	with open(install_dir+'/errors.log', 'r+', encoding = 'utf-8') as f:
		lines = f.readlines()
		if len(lines) > 99999:
			f.truncate(0)
			
	with open(install_dir+'/errors.log', 'a+', encoding = 'utf-8') as f:
		f.write(mes)
	
	with open(install_dir+'/new_errors', 'w+') as f:
		pass

def check_start_and_restart_service():

	while True:
			
		try:
		
			if os.path.isfile(install_dir+'/start_service'):
				os.remove(install_dir+'/start_service')
				proc = subprocess.Popen('/usr/bin/python3.7 '+install_dir+'/auction_manager_app.py start 2>> '+install_dir+'/errors.log', shell = True, stdout = subprocess.PIPE)
				proc.communicate()
				
			if os.path.isfile(install_dir+'/restart_service'):
				os.remove(install_dir+'/restart_service')
				proc = subprocess.Popen('/usr/bin/python3.7 '+install_dir+'/auction_manager_app.py restart 2>> '+install_dir+'/errors.log', shell = True, stdout = subprocess.PIPE)
				proc.communicate()
			
		except Exception:
			pass
		
		time.sleep(1)

class MyDaemon(daemon):

	def run(self):
			
		try:
			threading.Thread(target = check_start_and_restart_service, args = ()).start()
		except Exception:
		
			lock_1.acquire()
			try:
				log_error(traceback.format_exc().strip())
			finally:
				lock_1.release()


if __name__ == '__main__':
	
	user_run = os.getenv('USER')
	if user_run and user_run != 'root':
		color_print.print_fail('Run application only with root privileges')
		sys.exit(0)
		
	lenn = len(sys.argv)
	if lenn < 2:
		color_print.print_fail('Not enough arguments passed ('+str(lenn)+'). Usage: '+sys.argv[0]+' start|stop|status|restart')
		sys.exit(1)
			
	d = MyDaemon(daemon_pid)

	if sys.argv[1] == 'start':
		d.start()
	elif sys.argv[1] == 'stop':
		d.stop()
	elif sys.argv[1] == 'restart':
		d.restart()
	elif sys.argv[1] == 'status':
		d.status()
	else:
		color_print.print_fail('Unknown command')
		sys.exit(1)
