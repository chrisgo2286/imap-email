from dependencies.settings import (SERVER_IMAP, PORT_IMAP, SENDER_EMAIL, 
	SENDER_PW)
import email, imaplib, os

class IMAPEmail():
	"""
	Interface to downloading attachments from
	an email address and save them to a folder.
	"""

	def __init__(self):
		self.portal = imaplib.IMAP4_SSL(SERVER_IMAP, PORT_IMAP)
		self.login()

	def login(self):
		self.portal.login(SENDER_EMAIL, SENDER_PW)
		self.portal.select(readonly=False) # so we can mark mails as read

	def logout(self):
		self.portal.close()

	def fetch_unread_messages(self):
		emails = []
		result, messages = self.portal.search(None, 'Unseen')
		if result == "OK":
			for message in messages[0].split():
				ret, data = self.portal.fetch(message,'(RFC822)')
				
				msg = email.message_from_string(data[0][1].decode())
				if isinstance(msg, str) == False:
					emails.append(msg)
				response, data = self.portal.store(message, '+FLAGS','\\Seen')

			return emails

		self.error = "Failed to retreive emails."
		return emails

	def save_attachment(self, email, folder):
		for part in email.walk():
			if part.get_content_maintype() == 'multipart':
				continue
			if part.get('Content-Disposition') is None:
				continue

			filename = part.get_filename()
			att_path = os.path.join(folder, filename)

			if not os.path.isfile(att_path):
				fp = open(att_path, 'wb')
				fp.write(part.get_payload(decode=True))
				fp.close()


	# def save_attachment(self, msg, download_folder="/tmp"):
	# 	att_path = "No attachment found."
	# 	for part in msg.walk():
	# 		if part.get_content_maintype() == 'multipart':
	# 			continue
	# 		if part.get('Content-Disposition') is None:
	# 			continue

	# 		filename = part.get_filename()
	# 		att_path = os.path.join(download_folder, filename)

	# 		if not os.path.isfile(att_path):
	# 			fp = open(att_path, 'wb')
	# 			fp.write(part.get_payload(decode=True))
	# 			fp.close()
	# 	return att_path

	# def fetch_unread_messages(self):
	# 	emails = []
	# 	(result, messages) = self.connection.search(None, 'Unseen')
	# 	if result == "OK":
	# 		for message in messages[0].split():
	# 			ret, data = self.connection.fetch(message,'(RFC822)')
				
	# 			msg = email.message_from_string(data[0][1].decode())
	# 			if isinstance(msg, str) == False:
	# 				emails.append(msg)
	# 			response, data = self.connection.store(message, '+FLAGS','\\Seen')

	# 		return emails

	# 	self.error = "Failed to retreive emails."
	# 	return emails

	# def parse_email_address(self, email_address):
	# 	"""
	# 	Helper function to parse out the email address from the message
	# 	return: tuple (name, address). Eg. ('John Doe', 'jdoe@example.com')
	# 	"""
	# 	return email.utils.parseaddr(email_address)

if __name__ == '__main__':
	
	SERVER   = 'imap.mail.yahoo.com'
	EMAIL    = 'automation.cgo@yahoo.com'
	PASSWORD = 'omihpmbumfrohhfm'
	folder   = ("/home/christian/Documents/python_scripts/automation_docs/"
				"BIG/updates/20201210_114300")

	portal_email = PortalEmail(SERVER, EMAIL, PASSWORD)
	emails = portal_email.fetch_unread_messages()
	for m in emails:
		portal_email.save_attachment(m,folder)

