from risco_session import RiscoSession


def main():
	sess = RiscoSession()
	sess.authenticate("a@b.com", "******", 1234)

	try:
		print(sess.get_cp_state())
	except Exception as ex:
		print(ex)
		pass

	print(sess.arm(2))
	print(sess.disarm(2))


if __name__ == '__main__':
	main()