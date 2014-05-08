import re
class PdataMatch(object):

	_instance = None
	allRegExps = ['[A-Z][a-zA-Z.]+', '', '', '', '']

	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super(PdataMatch, cls).__new__(cls, *args, **kwargs)
		return cls._instance

	def addDate(self):
		if self.allRegExps[1] == '':
			self.allRegExps[1] = '\\d{2}[./]\\d{2}[./]\\d{4}'
			# self.allRegExps.append('[a-zA-Z]+ \\d{2}(th|nd)*(, \d{4})*')

	def addSSN(self):
		if self.allRegExps[2] == '':
			self.allRegExps[2] = '\\d{9}|\\d{3}.\\d{2}.\\d{4}'

	def addAddress(self):
		if self.allRegExps[3] == '':
			self.allRegExps[3] = '(?:[Pp](?:.)?[Oo](?:.)?(?: )?[Bb][Oo][Xx](?: )?\\d+(?:, ))|(?:\\d+ [A-Z][a-zA-Z]+ [A-Z][a-zA-Z]+(?:.)?(?: )?(?:[A-Z][^\\s]+)?(?:\\d{5})?)|(?:[A-Z][^\\s]+ [a-zA-Z]+, (?:\\w{2})?(?:\.)?(?: )?)'

	def addPhone(self):
		if self.allRegExps[4] == '':
			self.allRegExps[4] = '(?:\\+)?(?:(?:\\()?\d+(?:\\))?)?(?:[^\\d])?\\d+(?:[^\\d])?\\d+(?:[^\\d])?\\d+'

	def addRegExp(self, regex):
		if len(regex) == 0:
			return True
		try:
			re.compile(str(regex))
		except Exception:
			logging.error('Could not compile regex')
			return False
		self.allRegExps += [str(regex)]
		print 'New regex after adding ', regex, ': ', str(self.allRegExps)
		return True

	def removeRegex(self, name):
		try:
			ind = {
			'Pnoun':0, 
			'Date':1,
			'Phone':4,
			'SSN':2,
			'Address':3
			}[name]
			self.allRegExps[ind] = ''
		except Exception:
			logging.error('Unknown field' + name)