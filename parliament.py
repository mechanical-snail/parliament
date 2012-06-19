#!/usr/bin/env python3
import re, math, random
from collections import namedtuple
from io import StringIO

PartySpec = namedtuple('PartySpec', ['name', 'seats', 'color'])

def render_svg(partyspecs):
	'''Renders a parliament seat allocation diagram with the given parties' numbers of seats. Parameter: list of (party_name, num_seats) or (party_name, num_seats, color) tuples. If color is unspecified for a particular tuple, a random color will be chosen. Returns the SVG output as a string.'''
	
	# Total number of seats per number of rows in diagram:
	TOTALS = [3, 15, 33, 61, 95, 138, 189, 247, 313, 388, 469, 559, 657, 762, 876, 997, 1126, 1263, 1408, 1560, 1722, 1889, 2066, 2250, 2442, 2641, 2850, 3064, 3289, 3519, 3759, 4005, 4261, 4522, 4794, 5071, 5358, 5652, 5953, 6263, 6581, 6906, 7239, 7581, 7929, 8287, 8650, 9024, 9404]
	
	# Validation
	def normalize_partyspec(party):
		'Validates and normalizes the party information.'
		# check number of fields
		if len(party) not in [2, 3]:
			raise IndexError('Record should contain 2 or 3 fields: {0}'.format(party))
		party_name = party[0]
		
		num_seats = int(party[1])
		if num_seats < 0:
			raise ValueError('Party {0} has negative number of seats'.format(party))
		
		if len(party) == 3:	# color specified
			color = party[2]
			if not re.match('^#[0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F]$', color):
				raise ValueError('Bogus RGB colour: "{0}"'.format(color))
		else:	# pick random color
			color = "#%02x%02x%02x" % (random.randrange(255), random.randrange(255), random.randrange(255))
		
		return PartySpec(party_name, num_seats, color)
	partyspecs = list(map(normalize_partyspec, partyspecs))
	
	# Keep a running total of the number of delegates in the diagram, for use later.
	sumdelegates = sum((party.seats for party in partyspecs))
	if sumdelegates < 1:
		raise ValueError("Must have at least one seat in the legislature.")
	if sumdelegates > TOTALS[-1]:
		raise NotImplementedError("Maximum of {max} seats currently supported. Your parliament contains {n} seats.".format(max=TOTALS[-1], n=sumdelegates))
	
	# Now, actually draw the diagram
	
	#Initialize counters for use in layout
	spotcounter=0
	lines=0
	#Figure out how many rows are needed:
	for i in range(len(TOTALS)):
		if TOTALS[i] >= sumdelegates:
			rows=i+1
			break
	#Maximum radius of spot is 0.5/rows; leave a bit of space.
	radius=0.4/rows
	
	# Open svg file for writing:
	with StringIO() as outfile:
		#Write svg header:
		outfile.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
		outfile.write('<svg xmlns:svg="http://www.w3.org/2000/svg"\n')
		outfile.write('xmlns="http://www.w3.org/2000/svg" version="1.0"\n')
		#Make 350 px wide, 175 px high diagram with a 5 px blank border
		outfile.write('width="360" height="185">\n')
		outfile.write('<g>\n')
		#Print the number of seats in the middle at the bottom.
		outfile.write('<text x="175" y="175" style="font-size:36px;font-weight:bold;text-align:center;text-anchor:middle;font-family:Sans">'+str(sumdelegates)+'</text>\n')
		#Create list of centre spots
		poslist=[]
		for i in range(1,rows):
			#Each row can contain pi/(2asin(2/(3n+4i-2))) spots, where n is the number of rows and i is the number of the current row.
			J=int(float(sumdelegates)/TOTALS[rows-1]*math.pi/(2*math.asin(2.0/(3.0*rows+4.0*i-2.0))))
			#The radius of the ith row in an N-row diagram (Ri) is (3*N+4*i-2)/(4*N)
			R=(3.0*rows+4.0*i-2.0)/(4.0*rows)
			if J==1:
				poslist.append([math.pi/2.0, 1.75*R, R])
			else:
				for j in range(J):
					#The angle to a spot is n.(pi-2sin(r/Ri))/(Ni-1)+sin(r/Ri) where Ni is the number in the arc
					#x=R.cos(theta) + 1.75
					#y=R.sin(theta)
					angle=float(j)*(math.pi-2.0*math.sin(radius/R))/(float(J)-1.0)+math.sin(radius/R)
					poslist.append([angle,R*math.cos(angle)+1.75,R*math.sin(angle)])
		J=sumdelegates-len(poslist)
		R=(7.0*rows-2.0)/(4.0*rows)
		if J==1:
			poslist.append([math.pi/2.0, 1.75*R, R])
		else:
			for j in range(J):
				angle=float(j)*(math.pi-2.0*math.sin(radius/R))/(float(J)-1.0)+math.sin(radius/R)
				poslist.append([angle,R*math.cos(angle)+1.75,R*math.sin(angle)])
		poslist.sort(reverse=True)
		Counter=-1 #How many spots have we drawn?
		for party in partyspecs:
			#Make each party's blocks an svg group
			outfile.write('  <g style="fill:'+party.color+'" id="'+party.name+'">\n')
			for Counter in range(Counter+1, Counter+party.seats+1):
				outfile.write('    <circle cx="%5.2f" cy="%5.2f" r="%5.2f"/>\n' % (poslist[Counter][1]*100.0+5.0, 100.0*(1.75-poslist[Counter][2])+5.0, radius*100.0))
			outfile.write('  </g>\n')
		outfile.write('</g>\n')
		outfile.write('</svg>\n')
		
		return outfile.getvalue()

def display(svg):
	'Convenience function to display a string as an SVG image, by piping it to imagemagick.'
	import subprocess as SP
	imagemagick = SP.Popen(['display'], stdin=SP.PIPE)
	imagemagick.communicate(bytes(svg, 'utf8'))

def webpage():
	'''Renders the web page. For use as a CGI script.'''
	import cgi
	print("Content-type: text/html")
	print("""
	<html>
	<head><title>Format parliament diagram</title></head>
	<body>
		<h1>Under construction</h1>
		<h2>Format parliament diagram</h2>
		<h3>See <a href="http://drichfld.freeshell.org/arch.py">the source code</a> and <a href="http://en.wikipedia.org/wiki/User_talk:Slashme/parliament.py">the bug list</a></h3>
		<h3>How to use this script:</h3>
		<ul>
		<li>Type the list of parties in the box marked "List of parties".  Each party
		must have a name and a number of seats (can be 0), and if you like you can also add a colour.
		The parties in the list must be separated by semicolons (";") and the party
		information must be separated by commas (",") (For example, if you type:
		"Party A, 33; Party B, 22, #99FF99" you will have two parties, one labeled "Party A" with 33 seats and
		a random colour, and one labeled "Party B" in light green.)</li>
		<li>The script will create an svg diagram when you press "send".
		<b> - don\'t worry if it doesn\'t render properly in your browser, just save and open!</b></li>
		</ul>
		<form method="post" action="arch.cgi">
			<p>List of parties: <input type="text" name="inputlist"/></p>
			<p><INPUT type="submit" value="Send"></p>
		</form>
	""")
	form = cgi.FieldStorage()
	inputlist = form.getvalue("inputlist", "")
	if inputlist:
		print("[Party, support, colour]<br>")
		#initialize list of parties
		partylist = []
		for i in re.split("\s*;\s*",inputlist):
			partylist.append(re.split('\s*,\s*', i))
		for i in partylist:
			print(str(i)+"<br>")
		
		try:
			with open('arch.svg','w') as outfile:
				outfile.write(render_svg(partylist))
			print('<a href="http://drichfld.freeshell.org/perlcgi/arch.svg">Your SVG diagram</a><b> - don\'t worry if it doesn\'t render correctly in your browser, just save and open!</b>')
		except Exception as e:
			print('Error generating diagram: {e}<br />'.format(e=repr(e)))

	print("""
	<br>
	This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
	<br>
	This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
	<br>
	For the text of the GNU General Public License, please see <a href=http://www.gnu.org/licenses/>http://www.gnu.org/licenses/</a>.
	</body>
	</html>
	""")

# Enable drop-in replacement for original CGI script (hopefully)
if __name__ == '__main__':
	webpage()
