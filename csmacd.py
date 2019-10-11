import time
import random
import threading


def binaryExponentialAvoid(k):
	if k == 0:
		return 0.
	k = min(k, 10)
	r = random.randint(0, k)
	return (1 << r) * contentionTime


def send():
	rand_time = random.randint(0, 100) / 1000
	time.sleep(rand_time)


# randomly sleep for a while to simulate


def device(name, all_packages):
	"""
	Simulate a device using the CSMA/CD protocol.
	:param name: name of the device
	:param all_packages: number of packages need to send.
	:return: none
	"""
	print(name)
	global inUse
	for i in range(all_packages):
		rand_time = random.randint(0, 100) / 1000
		time.sleep(rand_time)
		# Sleep randomly between 1ms ~ 1s, to simulate the random  call of upper layers.
		sent = False
		for times in range(16):
			time.sleep(binaryExponentialAvoid(times))
			if inUse == 0:
				# When the bus is free (inUse == 0), send the message.
				time.sleep(contentionTime)
				# sleep a fixed time representing the time the signal traveling on the bus.
				inUse += 1
				if inUse == 1:
					send()
					print("%s: package %2d sent." % (name, i))
					sent = True
				else:
					print("%s: conflict detected when sending package %2d. send a while later." % (name,i))
				inUse -= 1
			if sent: break;
		if not sent:
			print("%s: package %2d failed. consulting the upper level for help." % (name, i))


if __name__ == "__main__":
	contentionTime = 0.1 # 5.12e-4  # contention time, fixed to 51.2us according to the CSMA/CD protocol.
	inUse = 0  # whether the bus is in use, 0 represents not and one or more represents yes.
	
	# print("a started.")
	# print("b started.")
	
	a = threading.Thread(target=device,args=["device A",20])
	b = threading.Thread(target=device,args=["device B",20])
	
	a.start()
	b.start()
	
	try:
		a.join()
		b.join()
	except RuntimeError:
		pass